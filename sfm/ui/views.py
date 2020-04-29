from django.urls import reverse
from django.db.models import Count
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.http import StreamingHttpResponse, Http404, HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.generic import TemplateView
from django.core.exceptions import PermissionDenied
from django.views.generic.base import RedirectView, View
from django.shortcuts import get_object_or_404, render
from django.apps import apps
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from braces.views import LoginRequiredMixin
from allauth.socialaccount.models import SocialApp
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import mark_safe

from .notifications import get_free_space, get_queue_data
from .forms import CollectionSetForm, ExportForm
from . import forms
from .models import CollectionSet, Collection, Seed, Credential, Harvest, Export, User, Warc
from .sched import next_run_time
from .utils import CollectionHistoryIter, clean_token, clean_blogname, diff_historical_object
from .monitoring import monitor_harvests, monitor_queues, monitor_exports
from .auth import CollectionSetOrSuperuserPermissionMixin, \
    check_collection_set_based_permission, UserOrSuperuserOrStaffPermissionMixin, UserOrSuperuserPermissionMixin, \
    has_collection_set_based_permission, CollectionSetOrCollectionVisibilityOrSuperuserOrStaffPermissionMixin
from .templatetags import ui_extras

import os
import logging
import csv

log = logging.getLogger(__name__)


class CollectionSetListView(LoginRequiredMixin, ListView):
    model = CollectionSet
    template_name = 'ui/collection_set_list.html'
    paginate_by = 20
    allow_empty = True
    paginate_orphans = 0

    def get_context_data(self, **kwargs):
        context = super(CollectionSetListView, self).get_context_data(**kwargs)
        # collection set identity, collection set type Name, collection set data
        collection_sets_lists = []
        active_collection_sets, inactive_collection_sets = split_collection_sets(
            CollectionSet.objects.filter(group__in=self.request.user.groups.all()).annotate(
                num_collections=Count('collections')).order_by('name'))
        collection_sets_lists.append(('acs', "Active", active_collection_sets))
        collection_sets_lists.append(('iacs', "Inactive", inactive_collection_sets))
        collection_sets_lists.append(('scs', "Shared", list(
            CollectionSet.objects.filter(collections__visibility=Collection.LOCAL_VISIBILITY).annotate(
                num_collections=Count('collections')).order_by('name'))))
        if self.request.user.is_superuser or self.request.user.is_staff:
            other_active_collection_sets, other_inactive_collection_sets = split_collection_sets(
                CollectionSet.objects.exclude(group__in=self.request.user.groups.all()).annotate(
                    num_collections=Count('collections')).order_by('name'))
            collection_sets_lists.append(('oacs', "Other Active", other_active_collection_sets))
            collection_sets_lists.append(('oics', "Other Inactive", other_inactive_collection_sets))
        context['collection_sets_lists'] = collection_sets_lists
        return context


def split_collection_sets(collection_sets):
    active_collection_sets = []
    inactive_collection_sets = []
    for collection_set in collection_sets:
        # Treating collection sets with no collections as active.
        if collection_set.is_active() or len(collection_set.collections.all()) == 0:
            active_collection_sets.append(collection_set)
        else:
            inactive_collection_sets.append(collection_set)
    return active_collection_sets, inactive_collection_sets


class CollectionSetDetailView(LoginRequiredMixin, CollectionSetOrCollectionVisibilityOrSuperuserOrStaffPermissionMixin,
                              DetailView):
    model = CollectionSet
    template_name = 'ui/collection_set_detail.html'
    context_object_name = 'collection_set'

    def get_context_data(self, **kwargs):
        context = super(CollectionSetDetailView, self).get_context_data(**kwargs)
        collections = []
        for collection in self.object.collections.all():
            if has_collection_set_based_permission(collection, self.request.user, allow_superuser=True,
                                                   allow_staff=True,
                                                   allow_collection_visibility=True):
                collections.append(collection)
        context['collection_list'] = collections
        context["diffs"], context["diffs_len"] = top_object_diffs(self.object)
        context["harvest_types"] = Collection.HARVEST_CHOICES
        context["harvest_description"] = Collection.HARVEST_DESCRIPTION
        context["item_id"] = self.object.id
        context["model_name"] = "collection_set"
        context["can_edit"] = has_collection_set_based_permission(self.object, self.request.user)
        return context


class CollectionSetCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = CollectionSet
    form_class = CollectionSetForm
    template_name = 'ui/collection_set_create.html'
    success_message = "New collection set added. You can now add collections. A collection retrieves data from a " \
                      "particular social media platform."

    def get_form_kwargs(self):
        kwargs = super(CollectionSetCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return reverse('collection_set_detail', args=(self.object.pk,))


class CollectionSetUpdateView(LoginRequiredMixin, CollectionSetOrSuperuserPermissionMixin, UpdateView):
    model = CollectionSet
    form_class = CollectionSetForm
    template_name = 'ui/collection_set_update.html'
    initial = {'history_note': ''}
    context_object_name = 'collection_set'

    def get_context_data(self, **kwargs):
        context = super(CollectionSetUpdateView, self).get_context_data(**kwargs)
        context['collection_list'] = Collection.objects.filter(
            collection_set=self.object.pk).annotate(num_seeds=Count('seeds')).order_by('name')
        return context

    def get_form_kwargs(self):
        kwargs = super(CollectionSetUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return reverse("collection_set_detail", args=(self.object.pk,))


class CollectionSetAddNoteView(LoginRequiredMixin, RedirectView):
    permanent = False
    pattern_name = "collection_set_detail"
    http_method_names = ['post', 'put']

    def get_redirect_url(self, *args, **kwargs):
        collection_set = get_object_or_404(CollectionSet, pk=kwargs['pk'])
        # Check permissions to add note
        check_collection_set_based_permission(collection_set, self.request.user)
        collection_set.history_note = self.request.POST.get("history_note", "")
        if collection_set.history_note:
            log.debug("Adding note %s to %s", collection_set.history_note, collection_set)
            collection_set.save()
            messages.info(self.request, "Note added.")
        return super(CollectionSetAddNoteView, self).get_redirect_url(*args, **kwargs)


class SeedsJSONAPIView(LoginRequiredMixin, BaseDatatableView):
    columns = ['link', 'token', 'uid', 'messages']
    # need to define the order columns, also need to match the Datatables setting in columnDefs
    order_columns = ['', 'token', 'uid', '']
    seed_infos = {}
    seed_warnings = {}
    seed_errors = {}
    last_harvest = None
    collection = None
    status = None

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    # max_display_length = 1200

    def get_initial_queryset(self):
        # return queryset used as base for futher sorting/filtering
        # these are simply objects displayed in datatable
        # You should not filter data returned here by any filter values entered by user. This is because
        # we need some base queryset to count total number of records.
        self.collection = get_object_or_404(Collection, pk=self.kwargs['pk'])
        # Check permissions to download
        check_collection_set_based_permission(self.collection, self.request.user, allow_staff=True,
                                              allow_collection_visibility=True)
        self.status = self.kwargs['status']
        self.last_harvest = self.collection.last_harvest()
        self.seed_infos = _get_seed_msg_map(self.last_harvest.infos) if self.last_harvest else {}
        seed_warnings = _get_seed_msg_map(self.last_harvest.warnings) if self.last_harvest else {}
        _add_duplicate_seed_warnings(self.collection, self.seed_warnings)
        self.seed_warnings = seed_warnings
        self.seed_errors = _get_seed_msg_map(self.last_harvest.errors) if self.last_harvest else {}

        # get rid of the exclude field
        self.columns = ['link', 'token', 'uid', 'messages']
        exclude_fields = []
        if not Collection.HARVEST_FIELDS[self.collection.harvest_type]['link']:
            exclude_fields.append('link')
        if not Collection.HARVEST_FIELDS[self.collection.harvest_type]['uid']:
            exclude_fields.append('uid')
        if not Collection.HARVEST_FIELDS[self.collection.harvest_type]['token']:
            exclude_fields.append('token')

        for exclusion in exclude_fields:
            if exclusion in self.columns:
                self.columns.remove(exclusion)

        return Seed.objects.filter(collection=self.kwargs['pk'], is_active=self.status == 'active').order_by('token',
                                                                                                             'uid')

    def filter_queryset(self, qs):
        # use request parameters to filter queryset
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(Q(token__icontains=search) | Q(uid__icontains=search))
        return qs

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'link':
            platform_type = self.collection.harvest_type.split('_')[0]
            return mark_safe(u'<a target="_blank" href="{0}"> <img src="{1}" alt="Link to {2} account for {3}" height="35" width="35"/></a>'.format(
                row.social_url(), static('ui/img/{}_logo.png'.format(platform_type)), platform_type, row.token))
        elif column == 'messages':
            msg_seed = ""
            for msg in self.seed_infos.get(row.seed_id, []):
                msg_seed += u'<li><p>{}</p></li>'.format(msg)
            for msg in self.seed_warnings.get(row.seed_id, []):
                msg_seed += u'<li><p>{}</p></li>'.format(msg)
            for msg in self.seed_errors.get(row.seed_id, []):
                msg_seed += u'<li><p>{}</p></li>'.format(msg)
            return mark_safe(u'<ul>{}</ul>'.format(msg_seed)) if msg_seed else ""

        elif column == 'uid':
            return mark_safe(u'<a href="{}">{}</a>'.format(reverse('seed_detail', args=[row.pk]),
                                                           row.uid)) if row.uid else ""
        elif column == 'token':
            return mark_safe(u'<a href="{}">{}</a>'.format(reverse('seed_detail', args=[row.pk]),
                                                           ui_extras.json_list(row.token))) if row.token else ""


class CollectionDetailView(LoginRequiredMixin, CollectionSetOrCollectionVisibilityOrSuperuserOrStaffPermissionMixin,
                           DetailView):
    model = Collection
    template_name = 'ui/collection_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CollectionDetailView, self).get_context_data(**kwargs)

        context["next_run_time"] = next_run_time(self.object.id)
        # Last 5 harvests
        context["harvests"] = self.object.harvests.all().order_by('-date_requested')[:5]
        context["harvest_count"] = self.object.harvests.all().count()
        last_harvest = self.object.last_harvest()
        context["last_harvest"] = last_harvest
        context["seed_infos"] = _get_seed_msg_map(last_harvest.infos) if last_harvest else {}
        seed_warnings = _get_seed_msg_map(last_harvest.warnings) if last_harvest else {}
        _add_duplicate_seed_warnings(self.object, seed_warnings)
        context["seed_warnings"] = seed_warnings
        context["seed_errors"] = _get_seed_msg_map(last_harvest.errors) if last_harvest else {}
        diffs = []
        collection_history_iter = CollectionHistoryIter(self.object.history.all(),
                                                        Seed.history.filter(collection=self.object).order_by(
                                                            "-history_date"))
        for historical_obj in collection_history_iter[0:3]:
            diffs.append(diff_historical_object(historical_obj))
        context["diffs"] = diffs
        context["diffs_len"] = len(collection_history_iter)
        context["has_seeds_list"] = self.object.required_seed_count() != 0
        has_perms = has_collection_set_based_permission(self.object, self.request.user)
        # Edit button should be enabled.
        can_edit = not self.object.is_on and self.object.is_active and has_perms
        context["can_edit"] = can_edit
        # Seed add buttons should be enabled.
        context["can_edit_seeds"] = can_edit if self.object.is_streaming() else self.object.is_active and has_perms
        context["can_toggle_on"] = has_perms
        context["can_toggle_active"] = not self.object.is_on and has_perms
        # If last harvest is stopping
        context["stream_stopping"] = self.object.last_harvest().status == Harvest.STOP_REQUESTED \
            if self.object.last_harvest() else False
        # For not enough seeds
        seed_warning_message = None
        # For too many seeds
        seed_error_message = None
        # No active seeds.
        if self.object.required_seed_count() == 0 and self.object.active_seed_count() != 0:
            seed_error_message = "All seeds must be deactivated before harvesting can be turned on."
        # Specific number of active seeds.
        elif self.object.required_seed_count() == 1:
            if self.object.active_seed_count() == 0:
                seed_warning_message = "1 active seed must be added before harvesting can be turned on."
            elif self.object.active_seed_count() > 1:
                seed_error_message = "Deactivate all seeds except 1 before harvesting can be turned on."
        elif self.object.required_seed_count() is not None and self.object.required_seed_count() > 1:
            if self.object.active_seed_count() < self.object.required_seed_count():
                seed_warning_message = "{} active seeds must be added before harvesting can be turned on.".format(
                    self.object.required_seed_count())
            elif self.object.active_seed_count > self.object.required_seed_count():
                seed_error_message = "Deactivate all seeds except {} before harvesting can be turned on.".format(
                    self.object.required_seed_count())
        # At least one active seeds
        elif self.object.required_seed_count() is None and self.object.active_seed_count() == 0:
            seed_warning_message = "At least 1 active seed must be added before harvesting can be turned on."
        context["seed_error_message"] = seed_error_message
        context["seed_warning_message"] = seed_warning_message

        # Adding credential active message, only one filter can occupy the credential
        credential_used_col = None
        if self.object.harvest_type in Collection.STREAMING_HARVEST_TYPES:
            credential_used_col_object = Collection.objects.filter(credential=self.object.credential.pk,
                                                                   harvest_type__in=Collection.STREAMING_HARVEST_TYPES,
                                                                   is_on=True)
            if credential_used_col_object.count() != 0:
                credential_used_col = credential_used_col_object[0]
        context["credential_used_col"] = credential_used_col
        # Harvest types that are not limited support bulk add
        context["can_add_bulk_seeds"] = self.object.required_seed_count() is None
        # Can export if there is a WARC
        context["can_export"] = Warc.objects.filter(harvest__harvest_type=self.object.harvest_type,
                                                    harvest__historical_collection__id=self.object.id).exists()
        context["item_id"] = self.object.id
        context["model_name"] = "collection"
        context["status_choices"] = Harvest.STATUS_CHOICES
        context["harvest_fields"] = Collection.HARVEST_FIELDS
        return context


def download_seed_list(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    # Check permissions to download
    check_collection_set_based_permission(collection, request.user, allow_staff=True, allow_collection_visibility=True)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="seedlist.csv"'
    writer = csv.writer(response, delimiter=',')
    writer.writerow([
        "Token",
        "Uid",
        "Link",
    ])
    for seed in collection.seeds.all():
        if seed.is_active:
            writer.writerow([
                seed.token,
                seed.uid,
                (seed.social_url() or "")
            ])
    return response


def _add_duplicate_seed_warnings(collection, seed_warnings):
    for result in collection.seeds.exclude(token__exact="").values("token").annotate(count=Count("id")).filter(
            count__gt=1):
        for seed in Seed.objects.filter(token=result["token"]):
            if seed.seed_id not in seed_warnings:
                seed_warnings[seed.seed_id] = []
            seed_warnings[seed.seed_id].append("Duplicate seeds exist with this token.")
    for result in collection.seeds.exclude(uid__exact="").values("uid").annotate(count=Count("id")).filter(count__gt=1):
        for seed in Seed.objects.filter(token=result["uid"]):
            if seed.seed_id not in seed_warnings:
                seed_warnings[seed.seed_id] = []
            seed_warnings[seed.seed_id].append("Duplicate seeds exist with this uid.")


def _get_seed_msg_map(msgs):
    seed_msg_map = {}
    for msg in msgs:
        if "seed_id" in msg:
            seed_id = msg["seed_id"]
            if seed_id not in seed_msg_map:
                seed_msg_map[seed_id] = []
            seed_msg_map[seed_id].append(msg["message"])
    return seed_msg_map


def _get_collection_form_class(harvest_type):
    return "Collection{}Form".format(harvest_type.replace("_", " ").title().replace(" ", ""))


def _get_harvest_type_name(harvest_type):
    for harvest_type_choice, harvest_type_name in Collection.HARVEST_CHOICES:
        if harvest_type_choice == harvest_type:
            return harvest_type_name


def _get_credential_list(collection_set_pk, harvest_type, extra_credential=None):
    collection_set = CollectionSet.objects.get(pk=collection_set_pk)
    platform = Collection.HARVEST_TYPES_TO_PLATFORM[harvest_type]
    q = Q(platform=platform, user__in=User.objects.filter(groups=collection_set.group))
    if extra_credential:
        q = q | Q(pk=extra_credential.pk)
    return Credential.objects.filter(q).filter(is_active=True).order_by('name')


def _get_credential_use_map(credentials, harvest_type):
    credential_use_map = {}
    if harvest_type in Collection.RATE_LIMITED_HARVEST_TYPES:
        for credential in credentials:
            active_collections = 0
            inactive_collections = 0
            for collection in credential.collections.all():
                if collection.is_on:
                    active_collections += 1
                else:
                    inactive_collections += 1
            if active_collections == 0 and inactive_collections == 0:
                credential_use_map[credential.id] = ("", "")
            else:
                credential_use_map[credential.id] = ("warning",
                                                     "Credential is in use by {0} collections that are turned on and "
                                                     "{1} collections that are turned off. Be mindful that over-using "
                                                     "credentials may result in collecting being rate limited by the "
                                                     "social media API.".format(active_collections,
                                                                                inactive_collections))
        return credential_use_map


class CollectionCreateView(LoginRequiredMixin, CollectionSetOrSuperuserPermissionMixin, SuccessMessageMixin,
                           CreateView):
    model = Collection
    template_name = 'ui/collection_create.html'

    def get_initial(self):
        initial = super(CollectionCreateView, self).get_initial()
        initial["collection_set"] = CollectionSet.objects.get(pk=self.kwargs["collection_set_pk"])
        return initial

    def get_context_data(self, **kwargs):
        context = super(CollectionCreateView, self).get_context_data(**kwargs)
        context["collection_set"] = CollectionSet.objects.get(pk=self.kwargs["collection_set_pk"])
        harvest_type = self.kwargs["harvest_type"]
        context["harvest_type_name"] = _get_harvest_type_name(harvest_type)
        credentials = _get_credential_list(self.kwargs["collection_set_pk"], harvest_type)
        context["credentials"] = credentials
        context["credential_use_map"] = _get_credential_use_map(credentials, harvest_type)
        context["platform"] = Collection.HARVEST_TYPES_TO_PLATFORM[self.kwargs["harvest_type"]]
        return context

    def get_form_kwargs(self):
        kwargs = super(CollectionCreateView, self).get_form_kwargs()
        kwargs["coll"] = self.kwargs["collection_set_pk"]
        kwargs['credential_list'] = _get_credential_list(self.kwargs["collection_set_pk"], self.kwargs["harvest_type"])
        return kwargs

    def get_form_class(self):
        return getattr(forms, _get_collection_form_class(self.kwargs["harvest_type"]))

    def get_success_url(self):
        return reverse('collection_detail', args=(self.object.pk,))

    def get_success_message(self, cleaned_data):
        if self.object.required_seed_count() != 0:
            return "New collection added. You can now add seeds."
        return "New collection added."


class CollectionUpdateView(LoginRequiredMixin, CollectionSetOrSuperuserPermissionMixin, UpdateView):
    model = Collection
    template_name = 'ui/collection_update.html'
    initial = {'history_note': ''}

    def get_context_data(self, **kwargs):
        context = super(CollectionUpdateView, self).get_context_data(**kwargs)
        context["collection_set"] = self.object.collection_set
        context["seed_list"] = Seed.objects.filter(collection=self.object.pk).order_by('token', 'uid')
        context["has_seeds_list"] = self.object.required_seed_count() != 0
        credentials = _get_credential_list(self.object.collection_set.pk, self.object.harvest_type,
                                           self.object.credential)
        context["credential_use_map"] = _get_credential_use_map(credentials, self.object.harvest_type)
        return context

    def get_form_kwargs(self):
        kwargs = super(CollectionUpdateView, self).get_form_kwargs()
        kwargs["coll"] = self.object.collection_set.pk
        kwargs['credential_list'] = _get_credential_list(self.object.collection_set.pk, self.object.harvest_type,
                                                         self.object.credential)
        return kwargs

    def get_form_class(self):
        return getattr(forms, _get_collection_form_class(self.object.harvest_type))

    def get_success_url(self):
        return reverse("collection_detail", args=(self.object.pk,))


class CollectionToggleOnView(LoginRequiredMixin, RedirectView):
    permanent = False
    pattern_name = "collection_detail"
    http_method_names = ['post', 'put']

    def get_redirect_url(self, *args, **kwargs):
        collection = get_object_or_404(Collection, pk=kwargs['pk'])
        # Check permissions to toggle
        check_collection_set_based_permission(collection, self.request.user)
        collection.is_on = not collection.is_on
        collection.history_note = self.request.POST.get("history_note", "")
        if collection.is_on:
            messages.info(self.request, "Harvesting is turned on.")
        else:
            messages.info(self.request, "Harvesting is turned off.")
        collection.save()
        return super(CollectionToggleOnView, self).get_redirect_url(*args, **kwargs)


class CollectionToggleActiveView(LoginRequiredMixin, RedirectView):
    permanent = False
    pattern_name = "collection_detail"
    http_method_names = ['post', 'put']

    def get_redirect_url(self, *args, **kwargs):
        collection = get_object_or_404(Collection, pk=kwargs['pk'])
        # Check permissions to toggle
        check_collection_set_based_permission(collection, self.request.user)
        collection.is_active = not collection.is_active
        collection.history_note = self.request.POST.get("history_note", "")
        if collection.is_active:
            messages.info(self.request, "Collection is turned active.")
        else:
            messages.info(self.request, "Collection is turned inactive.")
        collection.save()
        return super(CollectionToggleActiveView, self).get_redirect_url(*args, **kwargs)


class CollectionAddNoteView(LoginRequiredMixin, RedirectView):
    permanent = False
    pattern_name = "collection_detail"
    http_method_names = ['post', 'put']

    def get_redirect_url(self, *args, **kwargs):
        collection = get_object_or_404(Collection, pk=kwargs['pk'])
        # Check permissions to add note
        check_collection_set_based_permission(collection, self.request.user)
        collection.history_note = self.request.POST.get("history_note", "")
        if collection.history_note:
            log.debug("Adding note %s to %s", collection.history_note, collection)
            collection.save()
            messages.info(self.request, "Note added.")
        return super(CollectionAddNoteView, self).get_redirect_url(*args, **kwargs)


class SeedDetailView(LoginRequiredMixin, CollectionSetOrCollectionVisibilityOrSuperuserOrStaffPermissionMixin,
                     DetailView):
    model = Seed
    template_name = 'ui/seed_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SeedDetailView, self).get_context_data(**kwargs)
        context["diffs"], context["diffs_len"] = top_object_diffs(self.object)
        context["collection_set"] = CollectionSet.objects.get(id=self.object.collection.collection_set.id)
        context["item_id"] = self.object.id
        context["model_name"] = "seed"
        can_edit = has_collection_set_based_permission(self.object,
                                                       self.request.user) and self.object.collection.is_active
        if self.object.collection.is_streaming():
            can_edit = can_edit and not self.object.collection.is_on
        context["can_edit"] = can_edit
        return context


def _get_seed_form_class(harvest_type):
    return "Seed{}Form".format(harvest_type.replace("_", " ").title().replace(" ", ""))


def top_object_diffs(obj):
    diffs = []
    for historical_obj in obj.history.all()[0:3]:
        diffs.append(diff_historical_object(historical_obj))
    return diffs, obj.history.all().count()


class SeedCreateView(LoginRequiredMixin, CollectionSetOrSuperuserPermissionMixin, SuccessMessageMixin, CreateView):
    model = Seed
    template_name = 'ui/seed_create.html'

    def get_initial(self):
        initial = super(SeedCreateView, self).get_initial()
        collection = Collection.objects.get(pk=self.kwargs["collection_pk"])
        initial["collection"] = collection
        initial["collection_set"] = collection.collection_set
        return initial

    def get_context_data(self, **kwargs):
        context = super(SeedCreateView, self).get_context_data(**kwargs)
        collection = Collection.objects.get(pk=self.kwargs["collection_pk"])
        context["collection"] = collection
        context["collection_set"] = context["collection"].collection_set
        context["harvest_type_name"] = _get_harvest_type_name(collection.harvest_type)
        return context

    def get_form_kwargs(self):
        kwargs = super(SeedCreateView, self).get_form_kwargs()
        kwargs["collection"] = self.kwargs["collection_pk"]
        kwargs["view_type"] = Seed.CREATE_VIEW
        return kwargs

    def get_form_class(self):
        return getattr(forms,
                       _get_seed_form_class(Collection.objects.get(pk=self.kwargs["collection_pk"]).harvest_type))

    def get_success_url(self):
        return reverse("collection_detail", args=(self.kwargs["collection_pk"],))

    def get_success_message(self, cleaned_data):
        if self.object.collection.required_seed_count() == 1:
            return "New seed added."
        return "New seed added."


class SeedUpdateView(LoginRequiredMixin, CollectionSetOrSuperuserPermissionMixin, UpdateView):
    model = Seed
    template_name = 'ui/seed_update.html'
    initial = {'history_note': ''}

    def get_form_kwargs(self):
        kwargs = super(SeedUpdateView, self).get_form_kwargs()
        kwargs["collection"] = self.object.collection.pk
        kwargs["view_type"] = Seed.UPDATE_VIEW
        kwargs["entry"] = self.get_object()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(SeedUpdateView, self).get_context_data(**kwargs)
        context["collection_set"] = CollectionSet.objects.get(id=self.object.collection.collection_set.id)
        return context

    def get_form_class(self):
        return getattr(forms, _get_seed_form_class(self.object.collection.harvest_type))

    def get_success_url(self):
        return reverse("seed_detail", args=(self.object.pk,))

class BulkSeedCreateView(LoginRequiredMixin, View):
    template_name = 'ui/bulk_seed_create.html'

    def get(self, request, *args, **kwargs):
        collection = Collection.objects.get(pk=kwargs["collection_pk"])
        # Check permissions
        check_collection_set_based_permission(collection, request.user)
        form = self._form_class(collection)(initial={}, collection=kwargs["collection_pk"])
        return self._render(request, form, collection)

    def post(self, request, *args, **kwargs):
        collection = Collection.objects.get(pk=kwargs["collection_pk"])
        # Check permissions
        check_collection_set_based_permission(collection, request.user)
        form = self._form_class(collection)(request.POST, collection=kwargs["collection_pk"])
        if form.is_valid():
            tokens = form.cleaned_data['tokens'].splitlines()
            seeds_type = form.cleaned_data['seeds_type']
            seed_count = 0
            if collection.harvest_type == collection.TUMBLR_BLOG_POSTS:
                cleaned_data = [clean_blogname(t) for t in tokens]
            else:
                cleaned_data = [clean_token(t) for t in tokens]

            for token in cleaned_data:
                # Can't save a token called "null". It causes problems.
                if token and token.lower() != "null":
                    param = {'uid': token} if seeds_type == 'uid' else {'token__iexact': token}
                    if not Seed.objects.filter(collection=collection, **param).exists():
                        log.debug("Creating seed %s for collection %s", token, collection.pk)
                        param = {'uid': token} if seeds_type == 'uid' else {'token': token}
                        Seed.objects.create(collection=collection,
                                            history_note=form.cleaned_data['history_note'], **param)
                        seed_count += 1
                    else:
                        log.debug("Skipping creating seed %s for collection %s since it exists", token,
                                  collection.pk)
            # <process form cleaned data>
            messages.info(request, "{} seeds added.".format(seed_count))
            return HttpResponseRedirect(reverse("collection_detail", args=(self.kwargs["collection_pk"],)))

        return self._render(request, form, collection)

    @staticmethod
    def _form_class(collection):
        return getattr(forms,
                       "BulkSeed{}Form".format(collection.harvest_type.replace("_", " ").title().replace(" ", "")))

    def _render(self, request, form, collection):
        return render(request, self.template_name,
                      {'form': form, 'collection': collection, 'collection_set': collection.collection_set,
                       'harvest_type_name': _get_harvest_type_name(collection.harvest_type)})


class SeedToggleActiveView(LoginRequiredMixin, RedirectView):
    permanent = False
    pattern_name = "seed_detail"
    http_method_names = ['post', 'put']

    def get_redirect_url(self, *args, **kwargs):
        seed = get_object_or_404(Seed, pk=kwargs['pk'])
        # Check permissions to toggle
        check_collection_set_based_permission(seed.collection, self.request.user)
        seed.is_active = not seed.is_active
        seed.history_note = self.request.POST.get("history_note", "")
        if seed.is_active:
            messages.info(self.request, "Seed undeleted.")
        else:
            messages.info(self.request, "Seed deleted.")
        seed.save()
        return super(SeedToggleActiveView, self).get_redirect_url(*args, **kwargs)


class SeedAddNoteView(LoginRequiredMixin, RedirectView):
    permanent = False
    pattern_name = "seed_detail"
    http_method_names = ['post', 'put']

    def get_redirect_url(self, *args, **kwargs):
        seed = get_object_or_404(Seed, pk=kwargs['pk'])
        # Check permissions to add note
        check_collection_set_based_permission(seed, self.request.user)
        seed.history_note = self.request.POST.get("history_note", "")
        if seed.history_note:
            log.debug("Adding note %s to %s", seed.history_note, seed)
            seed.save()
            messages.info(self.request, "Note added.")
        return super(SeedAddNoteView, self).get_redirect_url(*args, **kwargs)


class CredentialDetailView(LoginRequiredMixin, UserOrSuperuserOrStaffPermissionMixin, DetailView):
    model = Credential
    template_name = 'ui/credential_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CredentialDetailView, self).get_context_data(**kwargs)
        context["diffs"], context["diffs_len"] = top_object_diffs(self.object)
        context["can_edit"] = self.request.user.is_superuser or self.object.user == self.request.user
        context["item_id"] = self.object.id
        context["model_name"] = "credential"
        context['collection_list'] = Collection.objects.filter(credential=self.object.pk).order_by('name')
        return context


class CredentialCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Credential
    template_name = 'ui/credential_create.html'
    success_message = "New credential added."

    def get_form_kwargs(self):
        kwargs = super(CredentialCreateView, self).get_form_kwargs()
        kwargs["view_type"] = Credential.CREATE_VIEW
        return kwargs

    def get_form_class(self):
        class_name = "Credential{}Form".format(self.kwargs["platform"].title())
        return getattr(forms, class_name)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CredentialCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("credential_detail", args=(self.object.pk,))

    def get_initial(self):
        initial = super(CredentialCreateView, self).get_initial()
        credential_name = "{}'s {} credential".format(self.request.user.username, self.kwargs["platform"])
        if not Credential.objects.filter(name=credential_name).exists():
            initial['name'] = credential_name
        return initial


class CredentialListView(LoginRequiredMixin, ListView):
    model = Credential
    template_name = 'ui/credential_list.html'
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super(CredentialListView, self).get_context_data(**kwargs)
        # (type, credential_list, can_connect_app)
        credentials = []
        for social_type, _ in Credential.PLATFORM_CHOICES:
            credential_objs = Credential.objects.filter(user=self.request.user,
                                                        platform=social_type).order_by('name')
            credentials.append((social_type, credential_objs, self._can_connect_credential(social_type)))

        context["credentials_lists"] = credentials
        return context

    @staticmethod
    def _can_connect_credential(platform):
        """
        Returns True if a Social App is configured for this platform.
        """
        return SocialApp.objects.filter(provider=platform).exists()


class CredentialUpdateView(LoginRequiredMixin, UserOrSuperuserPermissionMixin, UpdateView):
    model = Credential
    template_name = 'ui/credential_update.html'
    initial = {'history_note': ''}

    def get_form_kwargs(self):
        kwargs = super(CredentialUpdateView, self).get_form_kwargs()
        kwargs["view_type"] = Credential.UPDATE_VIEW
        kwargs["entry"] = self.get_object()
        return kwargs

    def get_form_class(self):
        class_name = "Credential{}Form".format(self.object.platform.title())
        return getattr(forms, class_name)

    def get_success_url(self):
        return reverse("credential_detail", args=(self.object.pk,))


class CredentialToggleActiveView(LoginRequiredMixin, UserOrSuperuserPermissionMixin, RedirectView):
    permanent = False
    pattern_name = "credential_detail"
    http_method_names = ['post', 'put']

    def get_redirect_url(self, *args, **kwargs):
        credential = get_object_or_404(Credential, pk=kwargs['pk'])
        credential.is_active = not credential.is_active
        credential.history_note = self.request.POST.get("history_note", "")
        if credential.is_active:
            messages.info(self.request, "Credential undeleted.")
        else:
            messages.info(self.request, "Credential deleted.")
        credential.save()
        return super(CredentialToggleActiveView, self).get_redirect_url(*args, **kwargs)


class ExportListView(LoginRequiredMixin, ListView):
    model = Export
    template_name = 'ui/export_list.html'
    paginate_by = 20
    allow_empty = True
    paginate_orphans = 0

    def get_context_data(self, **kwargs):
        context = super(ExportListView, self).get_context_data(**kwargs)
        exports = Export.objects.filter(
            user=self.request.user).order_by(
            '-date_requested')
        export_list = []
        for export in exports:
            seeds = list(export.seeds.all())
            collection = seeds[0].collection if seeds else export.collection
            if collection:
                export_list.append((collection.collection_set, collection, export))
        context['export_list'] = export_list
        return context


class ExportCreateView(LoginRequiredMixin, CollectionSetOrCollectionVisibilityOrSuperuserOrStaffPermissionMixin,
                       SuccessMessageMixin, CreateView):
    model = Export
    form_class = ExportForm
    template_name = 'ui/export_create.html'
    success_message = "Export requested. Check the Exports section for the status of your export. Large datasets may " \
                      "take a substantial amount of time. You will receive an email when your export is ready."

    def get_initial(self):
        initial = super(ExportCreateView, self).get_initial()
        collection = Collection.objects.get(pk=self.kwargs["collection_pk"])
        initial["collection"] = collection
        initial["collection_set"] = collection.collection_set
        return initial

    def get_context_data(self, **kwargs):
        context = super(ExportCreateView, self).get_context_data(**kwargs)
        context["collection"] = Collection.objects.get(pk=self.kwargs["collection_pk"])
        return context

    def get_form_kwargs(self):
        kwargs = super(ExportCreateView, self).get_form_kwargs()
        kwargs["collection"] = self.kwargs["collection_pk"]
        return kwargs

    def form_valid(self, form):
        # This will set user
        form.instance.user = self.request.user
        return super(ExportCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('export_detail', args=(self.object.pk,))


def _get_fileinfos(path):
    """
    Returns list of file names, bytes within directory
    """
    fileinfos = list()
    if os.path.exists(path):
        contents = os.listdir(path)
        for item in contents:
            p = os.path.join(path, item)
            if os.path.isfile(p):
                fileinfos.append((item, os.path.getsize(p)))
    return sorted(fileinfos)


class ExportDetailView(LoginRequiredMixin, CollectionSetOrCollectionVisibilityOrSuperuserOrStaffPermissionMixin,
                       DetailView):
    model = Export
    template_name = 'ui/export_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ExportDetailView, self).get_context_data(**kwargs)
        seeds = list(self.object.seeds.all())
        collection = seeds[0].collection if seeds else self.object.collection
        context["collection_set"] = collection.collection_set
        context["collection"] = collection
        context["fileinfos"] = _get_fileinfos(self.object.path) if self.object.status == Export.SUCCESS else ()
        return context


class HarvestListView(LoginRequiredMixin, ListView):
    context_object_name = "harvest_list"
    template_name = "ui/harvest_list.html"
    paginate_by = 15

    def get_queryset(self):
        self.collection = get_object_or_404(Collection, pk=self.kwargs["pk"])
        # Check permissions
        check_collection_set_based_permission(self.collection, self.request.user, allow_staff=True)
        return self.collection.harvests.all().order_by('-date_requested')

    def get_context_data(self, **kwargs):
        context = super(HarvestListView, self).get_context_data(**kwargs)
        context["collection_set"] = self.collection.collection_set
        context['collection'] = self.collection
        return context


class HarvestDetailView(LoginRequiredMixin, CollectionSetOrCollectionVisibilityOrSuperuserOrStaffPermissionMixin,
                        DetailView):
    model = Harvest
    template_name = 'ui/harvest_detail.html'

    def get_context_data(self, **kwargs):
        context = super(HarvestDetailView, self).get_context_data(**kwargs)
        context["collection_set"] = self.object.collection.collection_set
        context["collection"] = self.object.collection
        # If status is running or requested and not a streaming and if this is the most recent harvest
        context["can_void"] = False
        if self.object.status in (Harvest.RUNNING, Harvest.REQUESTED, Harvest.STOP_REQUESTED, Harvest.PAUSED) \
                and self.object == self.object.collection.last_harvest() \
                and has_collection_set_based_permission(self.object, self.request.user):
            context["can_void"] = True
        return context


class HarvestVoidView(LoginRequiredMixin, RedirectView):
    permanent = False
    pattern_name = "harvest_detail"
    http_method_names = ['post', 'put']

    def get_redirect_url(self, *args, **kwargs):
        harvest = get_object_or_404(Harvest, pk=kwargs['pk'])

        # Check permissions to void
        check_collection_set_based_permission(harvest, self.request.user)

        if harvest.status in (Harvest.RUNNING, Harvest.REQUESTED, Harvest.STOP_REQUESTED, Harvest.PAUSED):
            log.debug("Voiding %s", harvest)
            harvest.status = Harvest.VOIDED
            harvest.save()
        else:
            log.debug("Not voiding %s since status is %s", harvest, harvest.status)
        return super(HarvestVoidView, self).get_redirect_url(*args, **kwargs)


def _read_file_chunkwise(file_obj):
    """
    Reads file in 32Kb chunks
    """
    while True:
        data = file_obj.read(32768)
        if not data:
            break
        yield data


def export_file(request, pk, file_name):
    """
    Allows authorized user to export a file.

    Adapted from https://github.com/ASKBOT/django-directory
    """
    export = get_object_or_404(Export, pk=pk)
    if (request.user == export.user) or request.user.is_superuser:
        filepath = os.path.join(export.path, file_name)
        log.debug("Exporting %s", filepath)
        if os.path.exists(filepath):
            response = StreamingHttpResponse()
            response['Content-Disposition'] = 'attachment; filename=%s' % file_name
            response['Content-Type'] = 'application/octet-stream'
            file_obj = open(filepath, 'rb')
            response.streaming_content = _read_file_chunkwise(file_obj)
            return response
        else:
            raise Http404
    else:
        raise PermissionDenied


class CollectionChangeLogView(LoginRequiredMixin, TemplateView):
    template_name = "ui/change_log.html"

    def get_context_data(self, **kwargs):
        context = super(CollectionChangeLogView, self).get_context_data(**kwargs)
        collection_id = self.kwargs["item_id"]
        collection = Collection.objects.get(pk=collection_id)

        # Check permissions to view
        check_collection_set_based_permission(collection, self.request.user, allow_staff=True,
                                              allow_collection_visibility=True)

        context["item"] = collection

        paginator = Paginator(CollectionHistoryIter(collection.history.all(),
                                                    Seed.history.filter(collection=collection).order_by(
                                                        "-history_date")), 15)
        # if no page in URL, show first
        page = self.request.GET.get("page", 1)
        diffs_page = paginator.page(page)
        context["paginator"] = paginator
        context["page_obj"] = diffs_page
        diff_list = list()
        for historical_obj in diffs_page:
            diff_list.append(diff_historical_object(historical_obj))
        context['diff_list'] = diff_list

        context["model_name"] = "collection"
        context["name"] = collection.name
        return context


class ChangeLogView(LoginRequiredMixin, ListView):
    context_object_name = "history_list"
    template_name = "ui/change_log.html"
    paginate_by = 15

    def get_queryset(self):
        item_id = self.kwargs["item_id"]
        model_name = self.kwargs["model"].replace("_", "")
        ModelName = apps.get_model(app_label="ui", model_name=model_name)
        item = ModelName.objects.get(pk=item_id)
        # Check permissions
        check_collection_set_based_permission(item, self.request.user, allow_staff=True)
        return item.history.all()

    def get_context_data(self, **kwargs):
        context = super(ChangeLogView, self).get_context_data(**kwargs)

        item_id = self.kwargs["item_id"]
        model_name = self.kwargs["model"].replace("_", "")
        ModelName = apps.get_model(app_label="ui", model_name=model_name)
        item = ModelName.objects.get(pk=item_id)

        context["item"] = item
        context["model_name"] = self.kwargs["model"].replace("_", " ")
        try:
            context["name"] = item.name
        except Exception:
            context["name"] = item.token

        diff_list = list()
        for historical_obj in context['history_list']:
            diff_list.append(diff_historical_object(historical_obj))
        context['diff_list'] = diff_list
        return context


def collection_set_stats(_, pk, item, period):
    collection_set = get_object_or_404(CollectionSet, pk=pk)
    return JsonResponse(collection_set.item_stats(item,
                                                  days={
                                                      "week": 7,
                                                      "month": 30,
                                                      "year": 365
                                                  }.get(period, 0)), safe=False)


class HomeView(TemplateView):
    template_name = "ui/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['collection_set_list'] = CollectionSet.objects.filter(
            group__in=self.request.user.groups.all(), collections__is_active=True).distinct().order_by('name')
        context['space_data'] = get_free_space()
        context['queue_data'] = get_queue_data()
        return context


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'ui/profile_details.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileDetailView, self).get_context_data(**kwargs)
        context["user_groups"] = ','.join([g.name for g in self.request.user.groups.all()])
        superusers = User.objects.filter(is_superuser=True)
        # get the first super user email information
        context["email_info"] = 'mailto:' + superusers[0].email if superusers else ''
        return context

    def get_object(self, queryset=None):
        return self.request.user


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'ui/profile_update.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_class(self):
        class_name = "UserProfileForm"
        return getattr(forms, class_name)

    def get_success_url(self):
        return reverse("user_profile_detail")


class MonitorView(LoginRequiredMixin, TemplateView):
    template_name = "ui/monitor.html"

    def get_context_data(self, **kwargs):
        context = super(MonitorView, self).get_context_data(**kwargs)
        allharvests = monitor_harvests()
        harvests = [harvest for harvest in allharvests if
                    has_collection_set_based_permission(harvest,
                                                        self.request.user,
                                                        allow_superuser=True,
                                                        allow_staff=True,
                                                        allow_collection_visibility=True)]
        allexports = monitor_exports()
        exports = [export for export in allexports if
                   has_collection_set_based_permission(export,
                                                       self.request.user,
                                                       allow_superuser=True,
                                                       allow_collection_visibility=True)]
        context['harvests'] = harvests
        context['exports'] = exports
        context["harvester_queues"], context["exporter_queues"], context["ui_queues"] = monitor_queues()
        return context
