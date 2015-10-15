from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Collection, SeedSet, Seed
from .forms import CollectionForm, SeedSetForm, SeedForm
from django.core.urlresolvers import reverse_lazy, reverse
import json
from .rabbit import RabbitWorker
# from django.http import HttpResponseRedirect


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
    reverse_lazy('collection_list')


class CollectionUpdateView(UpdateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'ui/collection_update.html'

    def get_success_url(self):
        return reverse("collection_detail", args=(self.object.pk,))


class CollectionDeleteView(DeleteView):
    model = Collection
    template_name = 'ui/collection_delete.html'

    def get_success_url(self):
        return reverse_lazy('collection_list')


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
    reverse_lazy('seedset_list')


class SeedSetUpdateView(UpdateView):
    model = SeedSet
    form_class = SeedSetForm
    template_name = 'ui/seedset_update.html'

    def get_success_url(self):
        return reverse("seedset_detail", args=(self.object.pk,))


class SeedSetDeleteView(DeleteView):
    model = SeedSet
    template_name = 'ui/seedset_delete.html'

    def get_success_url(self):
        return reverse_lazy('seedset_list')


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

    def post(self, request, *args, **kwargs):
        m = {
            'Action': 'Create Seed',
            'SeedSet Object': self.request.POST.get('seed_set'),
            'Token': self.request.POST.get('token'),
            'UID': self.request.POST.get('uid')
        }
        RabbitWorker.channel.basic_publish(exchange='sfm_exchange',
                                           routing_key='sfm_exchange',
                                           body=json.dumps(m))
        self.object = None
        return super(CreateView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('seed_list')


class SeedUpdateView(UpdateView, RabbitWorker):
    model = Seed
    form_class = SeedForm
    template_name = 'ui/seed_update.html'

    def post(self, request, *args, **kwargs):
        m = {
            'Action': 'Update Seed',
            'SeedSet Object': self.request.POST.get('seed_set'),
            'Token': self.request.POST.get('token'),
            'UID': self.request.POST.get('uid')
        }
        RabbitWorker.channel.basic_publish(exchange='sfm_exchange',
                                           routing_key='sfm_exchange',
                                           body=json.dumps(m))
        self.object = self.get_object()
        return super(UpdateView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("seed_detail", args=(self.object.pk,))


class SeedDeleteView(DeleteView):
    model = Seed
    template_name = 'ui/seed_delete.html'

    def post(self, request, *args, **kwargs):
        seed = self.get_object()
        m = {
            'Action': 'Delete Seed',
            'ID': seed.id
        }
        RabbitWorker.channel.basic_publish(exchange='sfm_exchange',
                                           routing_key='sfm_exchange',
                                           body=json.dumps(m))
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('seed_list')
