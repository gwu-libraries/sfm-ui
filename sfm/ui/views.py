from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Count
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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

from .forms import CollectionSetForm, ExportForm
import forms
from .models import CollectionSet, Collection, Seed, Credential, Harvest, Export, User
from .sched import next_run_time
from .utils import diff_object_history, clean_token

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
        if self.request.user.is_superuser:
            context['collection_set_list_n'] = CollectionSet.objects.exclude(
                group__in=self.request.user.groups.all()).annotate(
                num_collections=Count('collections')).order_by('date_updated')

        context['collection_set_list'] = CollectionSet.objects.filter(
            group__in=self.request.user.groups.all()).annotate(
            num_collections=Count('collections')).order_by('date_updated')
        return context


class CollectionSetDetailView(LoginRequiredMixin, DetailView):
    model = CollectionSet
    template_name = 'ui/collection_set_detail.html'
    context_object_name = 'collection_set'

    def get_context_data(self, **kwargs):
        context = super(CollectionSetDetailView, self).get_context_data(**kwargs)
        context['collection_list'] = Collection.objects.filter(
            collection_set=self.object.pk).annotate(num_seeds=Count('seeds'))
        context["diffs"] = diff_object_history(self.object)
        context["harvest_types"] = Collection.HARVEST_CHOICES
        context["item_id"] = self.object.id
        context["model_name"] = "collection_set"
        return context


class CollectionSetCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = CollectionSet
    form_class = CollectionSetForm
    template_name = 'ui/collection_set_create.html'
    success_message = "New collection set added. You can now add collections."

    def get_form_kwargs(self):
        kwargs = super(CollectionSetCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return reverse('collection_set_detail', args=(self.object.pk,))


class CollectionSetUpdateView(LoginRequiredMixin, UpdateView):
    model = CollectionSet
    form_class = CollectionSetForm
    template_name = 'ui/collection_set_update.html'
    initial = {'history_note': ''}
    context_object_name = 'collection_set'

    def get_context_data(self, **kwargs):
        context = super(CollectionSetUpdateView, self).get_context_data(**kwargs)
        context['collection_list'] = Collection.objects.filter(
            collection_set=self.object.pk).annotate(num_seeds=Count('seeds'))
        return context

    def get_form_kwargs(self):
        kwargs = super(CollectionSetUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return reverse("collection_set_detail", args=(self.object.pk,))


class CollectionDetailView(LoginRequiredMixin, DetailView):
    model = Collection
    template_name = 'ui/collection_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CollectionDetailView, self).get_context_data(**kwargs)
        context["next_run_time"] = next_run_time(self.object.id)
        # Last 5 harvests
        context["harvests"] = self.object.harvests.all().order_by('-date_requested')[:5]
        context["harvest_count"] = self.object.harvests.all().count()
        context["last_harvest"] = self.object.last_harvest()
        context["diffs"] = diff_object_history(self.object)
        context["seed_list"] = Seed.objects.filter(collection=self.object.pk)
        context["has_seeds_list"] = self.object.required_seed_count() != 0
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
        if not harvest_list or "completed success" not in [str(item.status) for item in harvest_list]:
            context["can_export"] = False
        else:
            context["can_export"] = True
        context["item_id"] = self.object.id
        context["model_name"] = "collection"
        return context


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


class CollectionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Collection
    template_name = 'ui/collection_create.html'

    def get_initial(self):
        initial = super(CollectionCreateView, self).get_initial()
        initial["collection_set"] = CollectionSet.objects.get(pk=self.kwargs["collection_set_pk"])
        return initial

    def get_context_data(self, **kwargs):
        context = super(CollectionCreateView, self).get_context_data(**kwargs)
        context["collection_set"] = CollectionSet.objects.get(pk=self.kwargs["collection_set_pk"])
        context["harvest_type_name"] = _get_harvest_type_name(self.kwargs["harvest_type"])
        context["credentials"] = _get_credential_list(self.kwargs["collection_set_pk"], self.kwargs["harvest_type"])
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


class CollectionUpdateView(LoginRequiredMixin, UpdateView):
    model = Collection
    template_name = 'ui/collection_update.html'
    initial = {'history_note': ''}

    def get_context_data(self, **kwargs):
        context = super(CollectionUpdateView, self).get_context_data(**kwargs)
        context["collection_set"] = self.object.collection_set
        context["seed_list"] = Seed.objects.filter(collection=self.object.pk)
        context["has_seeds_list"] = self.object.required_seed_count() != 0
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
        collection.is_active = not collection.is_active
        if collection.is_active:
            messages.info(self.request, "Harvesting is turned on.")
        else:
            messages.info(self.request, "Harvesting is turned off.")
        collection.save()
        return super(CollectionToggleActiveView, self).get_redirect_url(*args, **kwargs)


class SeedListView(LoginRequiredMixin, ListView):
    model = Seed
    template_name = 'ui/seed_list.html'
    paginate_by = 20
    allow_empty = True
    paginate_orphans = 0


class SeedDetailView(LoginRequiredMixin, DetailView):
    model = Seed
    template_name = 'ui/seed_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SeedDetailView, self).get_context_data(**kwargs)
        context["diffs"] = diff_object_history(self.object)
        context["collection_set"] = CollectionSet.objects.get(id=self.object.collection.collection_set.id)
        context["item_id"] = self.object.id
        context["model_name"] = "seed"
        return context


def _get_seed_form_class(harvest_type):
    return "Seed{}Form".format(harvest_type.replace("_", " ").title().replace(" ", ""))


class SeedCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Seed
    template_name = 'ui/seed_create.html'

    def get_initial(self):
        initial = super(SeedCreateView, self).get_initial()
        initial["collection"] = Collection.objects.get(pk=self.kwargs["collection_pk"])
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


class SeedUpdateView(LoginRequiredMixin, UpdateView):
    model = Seed
    template_name = 'ui/seed_update.html'
    initial = {'history_note': ''}

    def get_form_kwargs(self):
        kwargs = super(SeedUpdateView, self).get_form_kwargs()
        kwargs["collection"] = self.object.collection.pk
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
        form = self._form_class(collection)(initial={}, collection=kwargs["collection_pk"])
        return self._render(request, form, collection)

    def post(self, request, *args, **kwargs):
        collection = Collection.objects.get(pk=kwargs["collection_pk"])
        form = self._form_class(collection)(request.POST, collection=kwargs["collection_pk"])
        if form.is_valid():
            tokens = form.cleaned_data['tokens'].splitlines()
            seed_count = 0
            for token in (clean_token(t) for t in tokens):
                if token:
                    if not Seed.objects.filter(collection=collection, token=token).exists():
                        log.debug("Creating seed %s for collection %s", token, collection.pk)
                        Seed.objects.create(token=token,
                                            collection=collection,
                                            history_note=form.cleaned_data['history_note'])
                        seed_count += 1
                    else:
                        log.debug("Skipping creating seed %s for collection %s since it exists", token, collection.pk)
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


class CredentialDetailView(LoginRequiredMixin, DetailView):
    model = Credential
    template_name = 'ui/credential_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CredentialDetailView, self).get_context_data(**kwargs)
        context["diffs"] = diff_object_history(self.object)
        context["can_edit"] = self.request.user.is_superuser or self.object.user == self.request.user
        context["item_id"] = self.object.id
        context["model_name"] = "credential"
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
        context['credential_list'] = Credential.objects.filter(user=self.request.user)
        context["can_connect_twitter"] = self._can_connect_credential(Credential.TWITTER)
        context["can_connect_weibo"] = self._can_connect_credential(Credential.WEIBO)
        return context

    def _can_connect_credential(self, platform):
        """
        Returns True if a Social App is configured for this platform.
        """
        return SocialApp.objects.filter(provider=platform).exists()


class CredentialUpdateView(LoginRequiredMixin, UpdateView):
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


class ExportCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Export
    form_class = ExportForm
    template_name = 'ui/export_create.html'
    success_message = "Export requested. Check back for the status or wait for an email."

    def get_initial(self):
        initial = super(ExportCreateView, self).get_initial()
        initial["collection"] = Collection.objects.get(pk=self.kwargs["collection_pk"])
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
            path = os.path.join(path, item)
            if os.path.isfile(path):
                fileinfos.append((item, os.path.getsize(path)))
    return fileinfos


class ExportDetailView(LoginRequiredMixin, DetailView):
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
        return self.collection.harvests.all()

    def get_context_data(self, **kwargs):
        context = super(HarvestListView, self).get_context_data(**kwargs)
        context["collection_set"] = self.collection.collection_set
        context['collection'] = self.collection
        return context


class HarvestDetailView(LoginRequiredMixin, DetailView):
    model = Harvest
    template_name = 'ui/harvest_detail.html'

    def get_context_data(self, **kwargs):
        context = super(HarvestDetailView, self).get_context_data(**kwargs)
        context["collection_set"] = self.object.collection.collection_set
        context["collection"] = self.object.collection
        return context


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
        context["item"] = item
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
            group__in=self.request.user.groups.all())
        return context
