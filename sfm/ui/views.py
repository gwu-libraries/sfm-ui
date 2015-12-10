from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin
from django.views.generic.list import ListView
from .models import Collection, SeedSet, Seed
from .models import Credential
from .forms import CollectionForm, SeedSetForm, SeedForm
from django.core.urlresolvers import reverse_lazy, reverse
from utils import schedule_harvest
from jobs import seedset_harvest


class CollectionListView(ListView):
    model = Collection
    template_name = 'ui/collection_list.html'
    paginate_by = 20
    allow_empty = True
    paginate_orphans = 0


class CollectionDetailView(DetailView):
    model = Collection
    template_name = 'ui/collection_detail.html'


class CollectionCreateView(CreateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'ui/collection_create.html'
    success_url = reverse_lazy('collection_list')


class CollectionUpdateView(UpdateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'ui/collection_update.html'

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


class SeedSetCreateView(CreateView):
    model = SeedSet
    form_class = SeedSetForm
    template_name = 'ui/seedset_create.html'
    success_url = reverse_lazy('seedset_list')


class SeedSetUpdateView(UpdateView):
    model = SeedSet
    form_class = SeedSetForm
    template_name = 'ui/seedset_update.html'

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        # To save data to database
        self.object = form.save()
        # To schedule harvest message for the current id
        d = self.get_object().id
        schedule = SeedSet.objects.filter(id=d).values(
            'schedule')[0]["schedule"]
        start_date = SeedSet.objects.filter(id=d).values(
            'start_date')[0]["start_date"]
        if start_date:
            # s = start_date.strftime('%Y-%m-%d')
            s = start_date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            s = '2000-01-01'
        end_date = SeedSet.objects.filter(id=d).values(
            'end_date')[0]["end_date"]
        if end_date:
            # e = end_date.strftime('%Y-%m-%d')
            e = end_date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            e = '2050-01-01'
        schedule_harvest(d, schedule, s, e)

        return super(ModelFormMixin, self).form_valid(form)

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
