from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Count
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.http import StreamingHttpResponse, Http404, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from braces.views import LoginRequiredMixin
from django.views.generic.base import RedirectView, View
from django.shortcuts import get_object_or_404, render


from .forms import CollectionForm, ExportForm
import forms
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
        if self.request.user.is_superuser:
            context['collection_list_n'] = Collection.objects.exclude(
                group__in=self.request.user.groups.all()).annotate(
                num_seedsets=Count('seed_sets')).order_by('date_updated')

        context['collection_list'] = Collection.objects.filter(
            group__in=self.request.user.groups.all()).annotate(
            num_seedsets=Count('seed_sets')).order_by('date_updated')
        return context


class CollectionDetailView(LoginRequiredMixin, DetailView):
    model = Collection
    template_name = 'ui/collection_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CollectionDetailView, self).get_context_data(**kwargs)
        context['seedset_list'] = SeedSet.objects.filter(
            collection=self.object.pk).annotate(num_seeds=Count('seeds'))
        context["diffs"] = diff_object_history(self.object)
        context["harvest_types"] = SeedSet.HARVEST_CHOICES
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
        context["has_seeds_list"] = self.object.required_seed_count() != 0
        seed_count_message = None
        # No active seeds.
        if self.object.required_seed_count() == 0 and self.object.active_seed_count() != 0:
            seed_count_message = "To enable harvesting, deactivate all seeds."
        # Specific number of active seeds.
        elif self.object.required_seed_count() > 0 and self.object.active_seed_count() != self.object.required_seed_count():
            seed_count_message = "To enable harvesting, make sure there are {} active seeds.".format(
                self.object.required_seed_count())
        # At least one active seeds
        elif self.object.required_seed_count() is None and self.object.active_seed_count() == 0:
            seed_count_message = "To enable harvesting, make sure there is at least 1 active seed."
        context["seed_count_message"] = seed_count_message
        # Harvest types that are not limited support bulk add
        context["can_add_bulk_seeds"] = self.object.required_seed_count() is None
        return context


def _get_seedset_form_class(harvest_type):
    return "SeedSet{}Form".format(harvest_type.replace("_", " ").title().replace(" ", ""))


def _get_harvest_type_name(harvest_type):
    for harvest_type_choice, harvest_type_name in SeedSet.HARVEST_CHOICES:
        if harvest_type_choice == harvest_type:
            return harvest_type_name


class SeedSetCreateView(LoginRequiredMixin, CreateView):
    model = SeedSet
    template_name = 'ui/seedset_create.html'

    def get_initial(self):
        initial = super(SeedSetCreateView, self).get_initial()
        initial["collection"] = Collection.objects.get(pk=self.kwargs["collection_pk"])
        return initial

    def get_context_data(self, **kwargs):
        context = super(SeedSetCreateView, self).get_context_data(**kwargs)
        context["collection"] = Collection.objects.get(pk=self.kwargs["collection_pk"])
        context["harvest_type_name"] = _get_harvest_type_name(self.kwargs["harvest_type"])
        return context

    def get_form_kwargs(self):
        kwargs = super(SeedSetCreateView, self).get_form_kwargs()
        kwargs["coll"] = self.kwargs["collection_pk"]
        return kwargs

    def get_form_class(self):
        return getattr(forms, _get_seedset_form_class(self.kwargs["harvest_type"]))

    def get_success_url(self):
        return reverse('seedset_detail', args=(self.object.pk,))


class SeedSetUpdateView(LoginRequiredMixin, UpdateView):
    model = SeedSet
    template_name = 'ui/seedset_update.html'
    initial = {'history_note': ''}

    def get_context_data(self, **kwargs):
        context = super(SeedSetUpdateView, self).get_context_data(**kwargs)
        context["collection"] = Collection.objects.get(pk=self.kwargs["collection_pk"])
        context["seed_list"] = Seed.objects.filter(seed_set=self.object.pk)
        context["has_seeds_list"] = self.object.required_seed_count() != 0
        return context

    def get_form_kwargs(self):
        kwargs = super(SeedSetUpdateView, self).get_form_kwargs()
        kwargs["coll"] = self.object.collection.pk
        return kwargs

    def get_form_class(self):
        return getattr(forms, _get_seedset_form_class(self.object.harvest_type))

    def get_success_url(self):
        return reverse("seedset_detail", args=(self.object.pk,))


class SeedSetToggleActiveView(LoginRequiredMixin, RedirectView):
    permanent = False
    pattern_name = "seedset_detail"
    http_method_names = ['post', 'put']

    def get_redirect_url(self, *args, **kwargs):
        seedset = get_object_or_404(SeedSet, pk=kwargs['pk'])
        seedset.is_active = not seedset.is_active
        seedset.save()
        return super(SeedSetToggleActiveView, self).get_redirect_url(*args, **kwargs)


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
        context["diffs"] = diff_object_history(self.object)
        context["collection"] = Collection.objects.get(id=self.object.seed_set.collection.pk)
        return context


def _get_seed_form_class(harvest_type):
    return "Seed{}Form".format(harvest_type.replace("_", " ").title().replace(" ", ""))


class SeedCreateView(LoginRequiredMixin, CreateView):
    model = Seed
    template_name = 'ui/seed_create.html'

    def get_initial(self):
        initial = super(SeedCreateView, self).get_initial()
        initial["seed_set"] = SeedSet.objects.get(pk=self.kwargs["seed_set_pk"])
        return initial

    def get_context_data(self, **kwargs):
        context = super(SeedCreateView, self).get_context_data(**kwargs)
        seed_set = SeedSet.objects.get(pk=self.kwargs["seed_set_pk"])
        context["seed_set"] = seed_set
        context["collection"] = context["seed_set"].collection
        context["harvest_type_name"] = _get_harvest_type_name(seed_set.harvest_type)
        return context

    def get_form_kwargs(self):
        kwargs = super(SeedCreateView, self).get_form_kwargs()
        kwargs["seedset"] = self.kwargs["seed_set_pk"]
        return kwargs

    def get_form_class(self):
        return getattr(forms, _get_seed_form_class(SeedSet.objects.get(pk=self.kwargs["seed_set_pk"]).harvest_type))

    def get_success_url(self):
        return reverse("seedset_detail", args=(self.kwargs["seed_set_pk"],))


class SeedUpdateView(LoginRequiredMixin, UpdateView):
    model = Seed
    template_name = 'ui/seed_update.html'
    initial = {'history_note': ''}

    def get_form_kwargs(self):
        kwargs = super(SeedUpdateView, self).get_form_kwargs()
        kwargs["seedset"] = self.object.seed_set.pk
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(SeedUpdateView, self).get_context_data(**kwargs)
        context["collection"] = Collection.objects.get(id=self.object.seed_set.collection.pk)
        return context

    def get_form_class(self):
        return getattr(forms, _get_seed_form_class(self.object.seed_set.harvest_type))

    def get_success_url(self):
        return reverse("seed_detail", args=(self.object.pk,))


class SeedDeleteView(LoginRequiredMixin, DeleteView):
    model = Seed
    template_name = 'ui/seed_delete.html'
    success_url = reverse_lazy('seed_list')


class BulkSeedCreateView(LoginRequiredMixin, View):
    template_name = 'ui/bulk_seed_create.html'

    def get(self, request, *args, **kwargs):
        seed_set = SeedSet.objects.get(pk=kwargs["seed_set_pk"])
        form = self._form_class(seed_set)(initial={}, seedset=kwargs["seed_set_pk"])
        return self._render(request, form, seed_set)

    def post(self, request, *args, **kwargs):
        seed_set = SeedSet.objects.get(pk=kwargs["seed_set_pk"])
        form = self._form_class(seed_set)(request.POST, seedset=kwargs["seed_set_pk"])
        if form.is_valid():
            log.info(form.cleaned_data['history_note'] is None)
            tokens = form.cleaned_data['tokens'].splitlines()
            for token in (t.strip() for t in tokens):
                if token:
                    if not Seed.objects.filter(seed_set=seed_set, token=token).exists():
                        log.debug("Creating seed %s for seedset %s", token, seed_set.pk)
                        Seed.objects.create(token=token,
                                            seed_set=seed_set,
                                            history_note=form.cleaned_data['history_note'])
                    else:
                        log.debug("Skipping creating seed %s for seedset %s since it exists", token, seed_set.pk)
            # <process form cleaned data>
            return HttpResponseRedirect(reverse("seedset_detail", args=(self.kwargs["seed_set_pk"],)))

        return self._render(request, form, seed_set)

    @staticmethod
    def _form_class(seed_set):
        return getattr(forms, "BulkSeed{}Form".format(seed_set.harvest_type.replace("_", " ").title().replace(" ", "")))

    def _render(self, request, form, seed_set):
        return render(request, self.template_name,
                      {'form': form, 'seed_set': seed_set, 'collection': seed_set.collection,
                       'harvest_type_name': _get_harvest_type_name(seed_set.harvest_type)})


class CredentialDetailView(LoginRequiredMixin, DetailView):
    model = Credential
    template_name = 'ui/credential_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CredentialDetailView, self).get_context_data(**kwargs)
        context["diffs"] = diff_object_history(self.object)
        return context


class CredentialCreateView(LoginRequiredMixin, CreateView):
    model = Credential
    template_name = 'ui/credential_create.html'

    def get_form_class(self):
        class_name = "Credential{}Form".format(self.kwargs["platform"].title())
        return getattr(forms, class_name)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CredentialCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("credential_detail", args=(self.object.pk,))


class CredentialListView(LoginRequiredMixin, ListView):
    model = Credential
    template_name = 'ui/credential_list.html'
    allow_empty = True


class CredentialUpdateView(LoginRequiredMixin, UpdateView):
    model = Credential
    # form_class = CredentialForm
    template_name = 'ui/credential_update.html'

    def get_form_class(self):
        class_name = "Credential{}Form".format(self.object.platform.title())
        return getattr(forms, class_name)

    def get_success_url(self):
        log.info("Foo")
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
