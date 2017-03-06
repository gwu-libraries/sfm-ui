from django.core.urlresolvers import reverse
from django.db.models import Count
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.http import StreamingHttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView
from django.core.exceptions import PermissionDenied
from django.views.generic.base import RedirectView, View
from django.shortcuts import get_object_or_404, render
from django.apps import apps
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from braces.views import LoginRequiredMixin
from allauth.socialaccount.models import SocialApp

from notifications import get_free_space, get_queue_data
from .forms import CollectionSetForm, ExportForm
import forms
from .models import CollectionSet, Collection, Seed, Credential, Harvest, Export, User, Warc
from .sched import next_run_time
from .utils import diff_object_history, diff_collection_and_seeds_history, clean_token, clean_blogname
from .monitoring import monitor_harvests, monitor_queues, monitor_exports
from .auth import CollectionSetOrSuperuserOrStaffPermissionMixin, CollectionSetOrSuperuserPermissionMixin, \
    check_collection_set_based_permission, UserOrSuperuserOrStaffPermissionMixin, UserOrSuperuserPermissionMixin, \
    has_collection_set_based_permission

import os
import logging

log = logging.getLogger(__name__)


class CollectionSetListView(LoginRequiredMixin, ListView):
    model = CollectionSet
    template_name = 'ui/collection_set_list.html'
    paginate_by = 20
    allow_empty = True
    paginate_orphans = 0

    def get_context_data(self, **kwargs):
        context = super(CollectionSetListView, self).get_context_data(**kwargs)
        if self.request.user.is_superuser or self.request.user.is_staff:
            context['collection_set_list_n'] = CollectionSet.objects.exclude(
                group__in=self.request.user.groups.all()).annotate(
                num_collections=Count('collections')).order_by('name')

        context['collection_set_list'] = CollectionSet.objects.filter(
            group__in=self.request.user.groups.all()).annotate(
            num_collections=Count('collections')).order_by('name')
        return context


class CollectionSetDetailView(LoginRequiredMixin, CollectionSetOrSuperuserOrStaffPermissionMixin, DetailView):
    model = CollectionSet
    template_name = 'ui/collection_set_detail.html'
    context_object_name = 'collection_set'

    def get_context_data(self, **kwargs):
        context = super(CollectionSetDetailView, self).get_context_data(**kwargs)
        context['collection_list'] = Collection.objects.filter(
            collection_set=self.object.pk).annotate(num_seeds=Count('seeds')).order_by('name')
        context["diffs"] = diff_object_history(self.object)
        context["harvest_types"] = sorted(Collection.HARVEST_CHOICES)
        context["item_id"] = self.object.id
        context["model_name"] = "collection_set"
        context["can_edit"] = has_collection_set_based_permission(self.object, self.request.user)
        return context


class CollectionSetCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = CollectionSet
    form_class = CollectionSetForm
    template_name = 'ui/collection_set_create.html'
    success_message = "New collection set added. You can now add collections. A collection retrieves data from a particular social media platform."

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


class CollectionDetailView(LoginRequiredMixin, CollectionSetOrSuperuserOrStaffPermissionMixin, DetailView):
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
        context["diffs"] = diff_collection_and_seeds_history(self.object)
        context["seed_list"] = Seed.objects.filter(collection=self.object.pk).order_by('token', 'uid')
        context["has_seeds_list"] = self.object.required_seed_count() != 0
        has_perms = has_collection_set_based_permission(self.object, self.request.user)
        context["can_edit"] = not self.object.is_active and has_perms
        context["can_toggle"] = has_perms
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
        elif self.object.required_seed_count() > 1:
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
                                                                   is_active=True)
            if len(credential_used_col_object) != 0:
                credential_used_col = credential_used_col_object[0]
        context["credential_used_col"] = credential_used_col
        # Harvest types that are not limited support bulk add
        context["can_add_bulk_seeds"] = self.object.required_seed_count() is None
        harvest_list = Harvest.objects.filter(harvest_type=self.object.harvest_type,
                                              historical_collection__id=self.object.id)
        # Can export if there is a WARC
        context["can_export"] = Warc.objects.filter(harvest__harvest_type=self.object.harvest_type,
                                                    harvest__historical_collection__id=self.object.id).exists()
        context["item_id"] = self.object.id
        context["model_name"] = "collection"
        return context


def _add_duplicate_seed_warnings(collection, seed_warnings):
    for result in collection.seeds.exclude(token__exact="").values("token").annotate(count=Count("id")).filter(count__gt=1):
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


def _get_credential_list(collection_set_pk, harvest_type):
    collection_set = CollectionSet.objects.get(pk=collection_set_pk)
    platform = Collection.HARVEST_TYPES_TO_PLATFORM[harvest_type]
    return Credential.objects.filter(platform=platform, user=User.objects.filter(
        groups=collection_set.group)).order_by('name')


def _get_credential_use_map(credentials, harvest_type):
    credential_use_map = {}
    if harvest_type in Collection.RATE_LIMITED_HARVEST_TYPES:
        for credential in credentials:
            active_collections = 0
            inactive_collections = 0
            for collection in credential.collections.all():
                if collection.is_active:
                    active_collections += 1
                else:
                    inactive_collections += 1
            if active_collections == 0 and inactive_collections == 0:
                credential_use_map[credential.id] = ("","")
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
        credentials = _get_credential_list(self.object.collection_set.pk, self.object.harvest_type)
        context["credential_use_map"] = _get_credential_use_map(credentials, self.object.harvest_type)
        return context

    def get_form_kwargs(self):
        kwargs = super(CollectionUpdateView, self).get_form_kwargs()
        kwargs["coll"] = self.object.collection_set.pk
        kwargs['credential_list'] = _get_credential_list(self.object.collection_set.pk, self.object.harvest_type)
        return kwargs

    def get_form_class(self):
        return getattr(forms, _get_collection_form_class(self.object.harvest_type))

    def get_success_url(self):
        return reverse("collection_detail", args=(self.object.pk,))


class CollectionToggleActiveView(LoginRequiredMixin, RedirectView):
    permanent = False
    pattern_name = "collection_detail"
    http_method_names = ['post', 'put']

    def get_redirect_url(self, *args, **kwargs):
        collection = get_object_or_404(Collection, pk=kwargs['pk'])
        # Check permissions to toggle
        check_collection_set_based_permission(collection, self.request.user)
        collection.is_active = not collection.is_active
        collection.history_note = ""
        if collection.is_active:
            messages.info(self.request, "Harvesting is turned on.")
        else:
            messages.info(self.request, "Harvesting is turned off.")
        collection.save()
        return super(CollectionToggleActiveView, self).get_redirect_url(*args, **kwargs)


class SeedDetailView(LoginRequiredMixin, CollectionSetOrSuperuserOrStaffPermissionMixin, DetailView):
    model = Seed
    template_name = 'ui/seed_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SeedDetailView, self).get_context_data(**kwargs)
        context["diffs"] = diff_object_history(self.object)
        context["collection_set"] = CollectionSet.objects.get(id=self.object.collection.collection_set.id)
        context["item_id"] = self.object.id
        context["model_name"] = "seed"
        context["can_edit"] = not self.object.collection.is_active \
                              and has_collection_set_based_permission(self.object, self.request.user)
        return context


def _get_seed_form_class(harvest_type):
    return "Seed{}Form".format(harvest_type.replace("_", " ").title().replace(" ", ""))


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
                if token:
                    param = {'uid': token} if seeds_type == 'uid' else {'token': token}
                    if not Seed.objects.filter(collection=collection, **param).exists():
                        log.debug("Creating seed %s for collection %s", token, collection.pk)
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


class CredentialDetailView(LoginRequiredMixin, UserOrSuperuserOrStaffPermissionMixin, DetailView):
    model = Credential
    template_name = 'ui/credential_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CredentialDetailView, self).get_context_data(**kwargs)
        context["diffs"] = diff_object_history(self.object)
        context["can_edit"] = self.request.user.is_superuser or self.object.user == self.request.user
        context["item_id"] = self.object.id
        context["model_name"] = "credential"
        context['collection_list'] = Collection.objects.filter(credential=self.object.pk).order_by('name')
        return context


class CredentialCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Credential
    template_name = 'ui/credential_create.html'
    success_message = "New credential added."

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
        context['credential_list'] = Credential.objects.filter(user=self.request.user).order_by('name')
        context["can_connect_twitter"] = self._can_connect_credential(Credential.TWITTER)
        context["can_connect_weibo"] = self._can_connect_credential(Credential.WEIBO)
        context["can_connect_tumblr"] = self._can_connect_credential(Credential.TUMBLR)
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

    def get_form_class(self):
        class_name = "Credential{}Form".format(self.object.platform.title())
        return getattr(forms, class_name)

    def get_success_url(self):
        return reverse("credential_detail", args=(self.object.pk,))


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
            export_list.append((collection.collection_set, collection, export))
        context['export_list'] = export_list
        return context


class ExportCreateView(LoginRequiredMixin, CollectionSetOrSuperuserOrStaffPermissionMixin, SuccessMessageMixin,
                       CreateView):
    model = Export
    form_class = ExportForm
    template_name = 'ui/export_create.html'
    success_message = "Export requested. Check back for the status or wait for an email."

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


class ExportDetailView(LoginRequiredMixin, CollectionSetOrSuperuserOrStaffPermissionMixin, DetailView):
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


class HarvestDetailView(LoginRequiredMixin, CollectionSetOrSuperuserOrStaffPermissionMixin, DetailView):
    model = Harvest
    template_name = 'ui/harvest_detail.html'

    def get_context_data(self, **kwargs):
        context = super(HarvestDetailView, self).get_context_data(**kwargs)
        context["collection_set"] = self.object.collection.collection_set
        context["collection"] = self.object.collection
        # If status is running or requested and not a streaming and if this is the most recent harvest
        context["can_void"] = False
        if self.object.status in (Harvest.RUNNING, Harvest.REQUESTED) \
                and not self.object.collection.is_streaming() \
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

        if harvest.status in (Harvest.RUNNING, Harvest.REQUESTED):
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
            file_obj = open(filepath)
            response.streaming_content = _read_file_chunkwise(file_obj)
            return response
        else:
            raise Http404
    else:
        raise PermissionDenied


class ChangeLogView(LoginRequiredMixin, TemplateView):
    template_name = "ui/change_log.html"

    def get_context_data(self, **kwargs):
        context = super(ChangeLogView, self).get_context_data(**kwargs)
        item_id = self.kwargs["item_id"]
        model_name = self.kwargs["model"].replace("_", "")
        ModelName = apps.get_model(app_label="ui", model_name=model_name)
        item = ModelName.objects.get(pk=item_id)

        # Check permissions to view
        check_collection_set_based_permission(item, self.request.user, allow_staff=True)

        context["item"] = item
        if model_name == 'collection':
            diffs = diff_collection_and_seeds_history(item)
        else:
            diffs = diff_object_history(item)
        paginator = Paginator(diffs, 15)
        # if no page in URL, show first
        page = self.request.GET.get("page", 1)
        diffs_page = paginator.page(page)
        context["paginator"] = paginator
        context["diffs_page"] = diffs_page
        context["model_name"] = self.kwargs["model"].replace("_", " ")
        try:
            context["name"] = item.name
        except:
            context["name"] = item.token
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
            group__in=self.request.user.groups.all()).order_by('name')
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
        context['harvests'] = monitor_harvests()
        context['exports'] = monitor_exports()
        context["harvester_queues"], context["exporter_queues"], context["ui_queues"] = monitor_queues()
        return context
