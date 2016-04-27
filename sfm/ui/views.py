from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Count
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.http import StreamingHttpResponse, Http404
from django.core.exceptions import PermissionDenied
from braces.views import LoginRequiredMixin

from .forms import CollectionForm, SeedSetForm, SeedForm, CredentialForm
from .forms import CredentialFlickrForm, CredentialTwitterForm, CredentialWeiboForm, ExportForm
from .models import Collection, SeedSet, Seed, Credential, Harvest, Export
from .sched import next_run_time
from .utils import diff_object_history

import os
import logging

log = logging.getLogger(__name__)


class CollectionListView(LoginRequiredMixin, ListView):
    model = Collection
    template_name = 'ui/collection_list.html'
    paginate_by = 20
    allow_empty = True
    paginate_orphans = 0

    def get_context_data(self, **kwargs):
        context = super(CollectionListView, self).get_context_data(**kwargs)
        context['collection_list'] = Collection.objects.filter(
            group__in=self.request.user.groups.all()).annotate(
            num_seedsets=Count('seed_sets')).order_by(
            'date_updated')
        return context


class CollectionDetailView(LoginRequiredMixin, DetailView):
    model = Collection
    template_name = 'ui/collection_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CollectionDetailView, self).get_context_data(**kwargs)
        context['seedset_list'] = SeedSet.objects.filter(
            collection=self.object.pk).annotate(num_seeds=Count('seeds'))
        context["diffs"] = diff_object_history(self.object)
        return context


class CollectionCreateView(LoginRequiredMixin, CreateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'ui/collection_create.html'
    success_url = reverse_lazy('collection_list')

    def get_form_kwargs(self):
        kwargs = super(CollectionCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class CollectionUpdateView(LoginRequiredMixin, UpdateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'ui/collection_update.html'
    initial = {'history_note': ''}

    def get_context_data(self, **kwargs):
        context = super(CollectionUpdateView, self).get_context_data(**kwargs)
        context['seedset_list'] = SeedSet.objects.filter(
            collection=self.object.pk).annotate(num_seeds=Count('seeds'))
        return context

    def get_form_kwargs(self):
        kwargs = super(CollectionUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return reverse("collection_detail", args=(self.object.pk,))


class CollectionDeleteView(DeleteView):
    model = Collection
    template_name = 'ui/collection_delete.html'
    success_url = reverse_lazy('collection_list')


class SeedSetDetailView(LoginRequiredMixin, DetailView):
    model = SeedSet
    template_name = 'ui/seedset_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SeedSetDetailView, self).get_context_data(**kwargs)
        context["next_run_time"] = next_run_time(self.object.id)
        context["harvests"] = Harvest.objects.filter(historical_seed_set__id=self.object.id)
        context["diffs"] = diff_object_history(self.object)
        context["seed_list"] = Seed.objects.filter(seed_set=self.object.pk)
        return context


class SeedSetCreateView(LoginRequiredMixin, CreateView):
    model = SeedSet
    form_class = SeedSetForm
    template_name = 'ui/seedset_create.html'

    def get_initial(self):
        initial = super(SeedSetCreateView, self).get_initial()
        initial["collection"] = Collection.objects.get(pk=self.kwargs["collection_pk"])
        return initial

    def get_context_data(self, **kwargs):
        context = super(SeedSetCreateView, self).get_context_data(**kwargs)
        context["collection"] = Collection.objects.get(pk=self.kwargs["collection_pk"])
        return context

    def get_form_kwargs(self):
        kwargs = super(SeedSetCreateView, self).get_form_kwargs()
        kwargs["coll"] = self.kwargs["collection_pk"]
        return kwargs

    def get_success_url(self):
        return reverse('seedset_detail', args=(self.object.pk,))


class SeedSetUpdateView(LoginRequiredMixin, UpdateView):
    model = SeedSet
    form_class = SeedSetForm
    template_name = 'ui/seedset_update.html'
    initial = {'history_note': ''}

    def get_initial(self):
        initial = super(SeedSetUpdateView, self).get_initial()
        initial["collection"] = Collection.objects.get(pk=self.kwargs["collection_pk"])
        return initial

    def get_context_data(self, **kwargs):
        context = super(SeedSetUpdateView, self).get_context_data(**kwargs)
        context["collection"] = Collection.objects.get(pk=self.kwargs["collection_pk"])
        context["seeds_list"] = Seed.objects.filter(seed_set=self.object.pk)
        return context

    def get_form_kwargs(self):
        kwargs = super(SeedSetUpdateView, self).get_form_kwargs()
        kwargs["coll"] = self.kwargs["collection_pk"]
        return kwargs

    def get_success_url(self):
        return reverse("seedset_detail", args=(self.object.pk,))


class SeedSetDeleteView(LoginRequiredMixin, DeleteView):
    model = SeedSet
    template_name = 'ui/seedset_delete.html'
    success_url = reverse_lazy('seedset_list')


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
        # seed = self.object
        context["diffs"] = diff_object_history(self.object)
        context["collection"] = Collection.objects.get(id=self.object.seed_set.pk)
        return context


class SeedCreateView(LoginRequiredMixin, CreateView):
    model = Seed
    form_class = SeedForm
    template_name = 'ui/seed_create.html'

    def get_initial(self):
        initial = super(SeedCreateView, self).get_initial()
        initial["seed_set"] = SeedSet.objects.get(pk=self.kwargs["seed_set_pk"])
        return initial

    def get_context_data(self, **kwargs):
        context = super(SeedCreateView, self).get_context_data(**kwargs)
        context["seed_set"] = SeedSet.objects.get(pk=self.kwargs["seed_set_pk"])
        context["collection"] = context["seed_set"].collection
        return context

    def get_form_kwargs(self):
        kwargs = super(SeedCreateView, self).get_form_kwargs()
        kwargs["seedset"] = self.kwargs["seed_set_pk"]
        return kwargs

    def get_success_url(self):
        return reverse("seedset_detail", args=(self.kwargs["seed_set_pk"],))


class SeedUpdateView(LoginRequiredMixin, UpdateView):
    model = Seed
    form_class = SeedForm
    template_name = 'ui/seed_update.html'
    initial = {'history_note': ''}

    def get_form_kwargs(self):
        kwargs = super(SeedUpdateView, self).get_form_kwargs()
        kwargs["seedset"] = self.object.seed_set.pk
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(SeedUpdateView, self).get_context_data(**kwargs)
        context["collection"] = Collection.objects.get(id=self.object.seed_set.pk)
        return context

    def get_success_url(self):
        return reverse("seed_detail", args=(self.object.pk,))


class SeedDeleteView(LoginRequiredMixin, DeleteView):
    model = Seed
    template_name = 'ui/seed_delete.html'
    success_url = reverse_lazy('seed_list')


class CredentialDetailView(LoginRequiredMixin, DetailView):
    model = Credential
    template_name = 'ui/credential_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CredentialDetailView, self).get_context_data(**kwargs)
        context["diffs"] = diff_object_history(self.object)
        return context


class CredentialTwitterCreateView(LoginRequiredMixin, CreateView):
    model = Credential
    form_class = CredentialTwitterForm
    template_name = 'ui/credential_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CredentialTwitterCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("credential_detail", args=(self.object.pk,))


class CredentialWeiboCreateView(LoginRequiredMixin, CreateView):
    model = Credential
    form_class = CredentialWeiboForm
    template_name = 'ui/credential_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CredentialWeiboCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("credential_detail", args=(self.object.pk,))


class CredentialFlickrCreateView(LoginRequiredMixin, CreateView):
    model = Credential
    form_class = CredentialFlickrForm
    template_name = 'ui/credential_create.html'

    def form_valid(self, form):
        # This will set user
        form.instance.user = self.request.user
        return super(CredentialFlickrCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("credential_detail", args=(self.object.pk,))

class CredentialListView(LoginRequiredMixin, ListView):
    model = Credential
    template_name = 'ui/credential_list.html'
    allow_empty = True


class CredentialUpdateView(UpdateView):
    model = Credential
    form_class = CredentialForm
    template_name = 'ui/credential_update.html'

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
            seedset = seeds[0].seed_set if seeds else export.seed_set
            export_list.append((seedset.collection, seedset, export))
        context['export_list'] = export_list
        return context


class ExportCreateView(LoginRequiredMixin, CreateView):
    model = Export
    form_class = ExportForm
    template_name = 'ui/export_create.html'

    def get_initial(self):
        initial = super(ExportCreateView, self).get_initial()
        initial["seedset"] = SeedSet.objects.get(pk=self.kwargs["seedset_pk"])
        return initial

    def get_context_data(self, **kwargs):
        context = super(ExportCreateView, self).get_context_data(**kwargs)
        context["seedset"] = SeedSet.objects.get(pk=self.kwargs["seedset_pk"])
        return context

    def get_form_kwargs(self):
        kwargs = super(ExportCreateView, self).get_form_kwargs()
        kwargs["seedset"] = self.kwargs["seedset_pk"]
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
        seedset = seeds[0].seed_set if seeds else self.object.seed_set
        context["collection"] = seedset.collection
        context["seedset"] = seedset
        context["fileinfos"] = _get_fileinfos(self.object.path) if self.object.status == Export.SUCCESS else ()
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
