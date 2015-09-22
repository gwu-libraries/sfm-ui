from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Collection, SeedSet, Seed
from .forms import CollectionForm, SeedSetForm, SeedForm
from django.core.urlresolvers import reverse_lazy, reverse

# Create your views here.


class CollectionListView(ListView):
    model = Collection
    template_name = 'ui/collection_list.html'
    paginate_by = 20
    context_object_name = 'collection_list'
    allow_empty = True
    page_kwarg = 'page'
    paginate_orphans = 0


class CollectionDetailView(DetailView):
    model = Collection
    template_name = 'ui/collection_detail.html'
    context_object_name = 'collection'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'


class CollectionCreateView(CreateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'ui/collection_create.html'
    success_url = reverse_lazy('collection_list')


class CollectionUpdateView(UpdateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'ui/collection_update.html'
    initial = {}
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = 'collection'

    def get_success_url(self):
        return reverse("collection_detail", args=(self.object.pk,))


class CollectionDeleteView(DeleteView):
    model = Collection
    template_name = 'ui/collection_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = 'collection'

    def get_success_url(self):
        return reverse('collection_list')


class SeedSetListView(ListView):
    model = SeedSet
    template_name = 'ui/seedset_list.html'
    paginate_by = 20
    context_object_name = 'seedset_list'
    allow_empty = True
    page_kwarg = 'page'
    paginate_orphans = 0


class SeedSetDetailView(DetailView):
    model = SeedSet
    template_name = 'ui/seedset_detail.html'
    context_object_name = 'seedset'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'


class SeedSetCreateView(CreateView):
    model = SeedSet
    form_class = SeedSetForm
    template_name = 'ui/seedset_create.html'
    success_url = reverse_lazy('seedset_list')


class SeedSetUpdateView(UpdateView):
    model = SeedSet
    form_class = SeedSetForm
    template_name = 'ui/seedset_update.html'
    initial = {}
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = 'seedset'

    def get_success_url(self):
        return reverse("seedset_detail", args=(self.object.pk,))


class SeedSetDeleteView(DeleteView):
    model = SeedSet
    template_name = 'ui/seedset_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = 'seedset'

    def get_success_url(self):
        return reverse('seedset_list')


class SeedListView(ListView):
    model = Seed
    template_name = 'ui/seed_list.html'
    paginate_by = 20
    context_object_name = 'seed_list'
    allow_empty = True
    page_kwarg = 'page'
    paginate_orphans = 0


class SeedDetailView(DetailView):
    model = Seed
    template_name = 'ui/seed_detail.html'
    context_object_name = 'seed'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'


class SeedCreateView(CreateView):
    model = Seed
    form_class = SeedForm
    template_name = 'ui/seed_create.html'
    success_url = reverse_lazy('seed_list')


class SeedUpdateView(UpdateView):
    model = Seed
    form_class = SeedForm
    template_name = 'ui/seed_update.html'
    initial = {}
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = 'seed'

    def get_success_url(self):
        return reverse("seed_detail", args=(self.object.pk,))


class SeedDeleteView(DeleteView):
    model = Seed
    template_name = 'ui/seed_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = 'seed'

    def get_success_url(self):
        return reverse('seed_list')
