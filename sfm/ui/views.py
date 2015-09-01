from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Collection
from .forms import CollectionForm
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import Http404
# from django.shortcuts import render

# Create your views here.


class CollectionListView(ListView):
    model = Collection
    template_name = 'ui/collection_list.html'
    paginate_by = 20
    context_object_name = 'collection_list'
    allow_empty = True
    page_kwarg = 'page'
    paginate_orphans = 0

    def __init__(self, **kwargs):
        return super(CollectionListView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(CollectionListView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(CollectionListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return super(CollectionListView, self).get_queryset()

    def get_allow_empty(self):
        return super(CollectionListView, self).get_allow_empty()

    def get_context_data(self, *args, **kwargs):
        ret = super(CollectionListView, self).get_context_data(*args, **kwargs)
        return ret

    def get_paginate_by(self, queryset):
        return super(CollectionListView, self).get_paginate_by(queryset)

    def get_context_object_name(self, object_list):
        return super(CollectionListView, self).get_context_object_name(object_list)

    def paginate_queryset(self, queryset, page_size):
        return super(CollectionListView, self).paginate_queryset(queryset, page_size)

    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True):
        return super(CollectionListView, self).get_paginator(queryset, per_page, orphans=0, allow_empty_first_page=True)

    def render_to_response(self, context, **response_kwargs):
        return super(CollectionListView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(CollectionListView, self).get_template_names()


class CollectionDetailView(DetailView):
    model = Collection
    template_name = 'ui/collection_detail.html'
    context_object_name = 'collection'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'

    def __init__(self, **kwargs):
        return super(CollectionDetailView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(CollectionDetailView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(CollectionDetailView, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(CollectionDetailView, self).get_object(queryset)

    def get_queryset(self):
        return super(CollectionDetailView, self).get_queryset()

    def get_slug_field(self):
        return super(CollectionDetailView, self).get_slug_field()

    def get_context_data(self, **kwargs):
        ret = super(CollectionDetailView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(CollectionDetailView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(CollectionDetailView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(CollectionDetailView, self).get_template_names()


class CollectionCreateView(CreateView):
    model = Collection
    form_class = CollectionForm
    # fields = ['name1', 'name2', 'name3', 'name4', 'name5', 'name6', 'name7']
    template_name = 'ui/collection_create.html'
    success_url = reverse_lazy('collection_list')

    def __init__(self, **kwargs):
        return super(CollectionCreateView, self).__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        return super(CollectionCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(CollectionCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(CollectionCreateView, self).post(request, *args, **kwargs)

    def get_form_class(self):
        return super(CollectionCreateView, self).get_form_class()

    def get_form(self, form_class):
        return super(CollectionCreateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(CollectionCreateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(CollectionCreateView, self).get_initial()

    def form_invalid(self, form):
        return super(CollectionCreateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(CollectionCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(CollectionCreateView, self).get_context_data(**kwargs)
        return ret

    def render_to_response(self, context, **response_kwargs):
        return super(CollectionCreateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(CollectionCreateView, self).get_template_names()

    def get_success_url(self):
        return reverse("collection_detail", args=(self.object.pk,))


class CollectionUpdateView(UpdateView):
    model = Collection
    form_class = CollectionForm
    # fields = ['name1', 'name2', 'name3', 'name4', 'name5', 'name6', 'name7']
    template_name = 'ui/collection_update.html'
    initial = {}
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = 'collection'

    def __init__(self, **kwargs):
        return super(CollectionUpdateView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(CollectionUpdateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(CollectionUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(CollectionUpdateView, self).post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(CollectionUpdateView, self).get_object(queryset)

    def get_queryset(self):
        return super(CollectionUpdateView, self).get_queryset()

    def get_slug_field(self):
        return super(CollectionUpdateView, self).get_slug_field()

    def get_form_class(self):
        return super(CollectionUpdateView, self).get_form_class()

    def get_form(self, form_class):
        return super(CollectionUpdateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(CollectionUpdateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(CollectionUpdateView, self).get_initial()

    def form_invalid(self, form):
        return super(CollectionUpdateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(CollectionUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(CollectionUpdateView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(CollectionUpdateView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(CollectionUpdateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(CollectionUpdateView, self).get_template_names()

    def get_success_url(self):
        return reverse("collection_detail", args=(self.object.pk,))


class CollectionDeleteView(DeleteView):
    model = Collection
    template_name = 'ui/collection_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = 'collection'

    def __init__(self, **kwargs):
        return super(CollectionDeleteView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(CollectionDeleteView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        return super(CollectionDeleteView, self).post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super(CollectionDeleteView, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(CollectionDeleteView, self).get_object(queryset)

    def get_queryset(self):
        return super(CollectionDeleteView, self).get_queryset()

    def get_slug_field(self):
        return super(CollectionDeleteView, self).get_slug_field()

    def get_context_data(self, **kwargs):
        ret = super(CollectionDeleteView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(CollectionDeleteView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(CollectionDeleteView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(CollectionDeleteView, self).get_template_names()

    def get_success_url(self):
        return reverse('collection_list')
