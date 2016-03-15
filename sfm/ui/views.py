from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Count
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from braces.views import LoginRequiredMixin

from .forms import CollectionForm, SeedSetForm, SeedForm, CredentialForm
from .models import Collection, SeedSet, Seed, Credential
from .sched import next_run_time
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


class SeedSetListView(ListView):
    model = SeedSet
    template_name = 'ui/seedset_list.html'
    paginate_by = 20
    allow_empty = True
    paginate_orphans = 0


class SeedSetDetailView(DetailView):
    model = SeedSet
    template_name = 'ui/seedset_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SeedSetDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        # context['book_list'] = Book.objects.all()
        context["next_run_time"] = next_run_time(kwargs["object"].id)
        return context


class SeedSetCreateView(LoginRequiredMixin, CreateView):
    model = SeedSet
    form_class = SeedSetForm
    template_name = 'ui/seedset_create.html'

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(SeedSetCreateView, self).get_initial()
        initial["collection"] = Collection.objects.get(
           pk=self.kwargs["collection_pk"])
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


class SeedSetUpdateView(UpdateView):
    model = SeedSet
    form_class = SeedSetForm
    template_name = 'ui/seedset_update.html'

    def get_success_url(self):
        return reverse("seedset_detail", args=(self.object.pk,))


class SeedSetDeleteView(DeleteView):
    model = SeedSet
    template_name = 'ui/seedset_delete.html'
    success_url = reverse_lazy('seedset_list')


class SeedListView(ListView):
    model = Seed
    template_name = 'ui/seed_list.html'
    paginate_by = 20
    allow_empty = True
    paginate_orphans = 0


class SeedDetailView(DetailView):
    model = Seed
    template_name = 'ui/seed_detail.html'


class SeedCreateView(CreateView):
    model = Seed
    form_class = SeedForm
    template_name = 'ui/seed_create.html'
    success_url = reverse_lazy('seed_list')


class SeedUpdateView(UpdateView):
    model = Seed
    form_class = SeedForm
    template_name = 'ui/seed_update.html'

    def get_success_url(self):
        return reverse("seed_detail", args=(self.object.pk,))


class SeedDeleteView(DeleteView):
    model = Seed
    template_name = 'ui/seed_delete.html'
    success_url = reverse_lazy('seed_list')


class CredentialDetailView(LoginRequiredMixin, DetailView):
    model = Credential
    template_name = 'ui/credential_detail.html'


class CredentialCreateView(LoginRequiredMixin, CreateView):
    model = Credential
    form_class = CredentialForm
    template_name = 'ui/credential_create.html'
    success_url = reverse_lazy('credential_detail')


class CredentialListView(LoginRequiredMixin, ListView):
    model = Credential
    template_name = 'ui/credential_list.html'
    allow_empty = True
