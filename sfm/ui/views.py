from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Collection, SeedSet, Seed
from .forms import CollectionForm, SeedSetForm, SeedForm
from django.core.urlresolvers import reverse_lazy, reverse
import pika
import json
# from django.shortcuts import render
# from django.template import RequestContext
import os
# import sys
# from HttpRequest import request


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


def rabbit_worker(message):
    # Create a connection
    credentials = pika.PlainCredentials(
        username=os.environ['MQ_ENV_RABBITMQ_DEFAULT_USER'],
        password=os.environ['MQ_ENV_RABBITMQ_DEFAULT_PASS'])
    parameters = pika.ConnectionParameters(host='mq', credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    # Create a channel
    channel = connection.channel()
    # Declare sfm_exchange
    channel.exchange_declare(exchange="sfm_exchange", type="topic",
                             durable=True)
    channel.basic_publish(exchange='sfm_exchange', routing_key='sfm_exchange',
                          body=message)
    print " [x] Sent %r" % (message,)
    channel.close()


def rabbit_consumer(self):
    # Create a connection
    credentials = pika.PlainCredentials(
        username=os.environ['MQ_ENV_RABBITMQ_DEFAULT_USER'],
        password=os.environ['MQ_ENV_RABBITMQ_DEFAULT_PASS'])
    parameters = pika.ConnectionParameters(host='mq', credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    # Create a channel
    channel = connection.channel()
    # Declare sfm_exchange
    channel.exchange_declare(exchange="sfm_exchange", type="topic",
                             durable=True)
    # Declare harvester queue
    channel.queue_declare(queue="sfm_exchange", durable=True)
    # Bind
    channel.queue_bind(exchange="sfm_exchange", queue="sfm_exchange",
                       routing_key="sfm_exchange")
    print ' [*] Waiting for logs. To exit press CTRL+C'

    def callback(ch, method, properties, body):
        print " [x] Recieved %r" % (body,)

    channel.basic_consume(callback, queue="sfm_exchange", no_ack=True)
    channel.start_consuming()


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

    """def get(self, request, *args, **kwargs):
        # Handles GET requests and instantiates a blank version of the form.
        form = self.get_form()
        message = {
            'UID': form['platform_uid'].value(),
            'token': form['platform_token'].value()
        }
        rabbit_worker(json.dumps(message))
        return render(request, '/ui/seeds/1',
                      context_instance=RequestContext(request))"""

    message = {'1': 'test', '2': 'json'}
    rabbit_worker(json.dumps(message))

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
