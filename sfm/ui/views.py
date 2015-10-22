from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Collection, SeedSet, Seed
from .models import Credential
from .forms import CollectionForm, SeedSetForm, SeedForm
from django.core.urlresolvers import reverse_lazy, reverse
import json
from .rabbit import RabbitWorker


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

    def post(self, request, *args, **kwargs):
        # To get value of collection id
        for idval in list(Collection.objects.filter(
            id=self.request.POST.get('collection')).values('id')):
            if 'id' in idval:
                value = idval['id']
        # To get value of token in credentials. Where we pass our secret and key
        for token in list(Credential.objects.filter(
            id=self.request.POST.get('credential')).values('token')):
            if 'token' in token:
                credential = token['token']
        # To get value of platform, which is used in routing key later
        for platform in list(Credential.objects.filter(
            id=self.request.POST.get('credential')).values('platform')):
            if 'platform' in platform:
                media = platform['platform']
        # To get list of seeds
        seeds = list(Seed.objects.filter(
            seed_set=self.get_object().id).select_related('seeds').values(
                'token', 'uid'))
        # To Remove empty token values from the list of seeds
        for item in seeds:
            if item['token'] == '':
                item.pop('token', None)
        # To get value of seedset id
        seedset = self.get_object()
        # To be updated later
        credential = json.loads(str(credential))
        options = json.loads(str(self.request.POST.get('harvest_options')))
        # Routing key
        key = ''.join(['harvest.start.',str(media),'.',
                       self.request.POST.get('harvest_type')])
        m = {
            'id': str(seedset.id),
            'type': self.request.POST.get('harvest_type'),
            'options': options,
            'credentials': credential,
            'collection': {
                'id': str(value),
                'path': '/tmp/collection/'+str(value)
            },
            'seeds': seeds
        }
        RabbitWorker.channel.basic_publish(exchange='sfm_exchange',
                                           routing_key=key,
                                           body=json.dumps(m))
        self.object = self.get_object()
        return super(UpdateView, self).post(request, *args, **kwargs)

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
