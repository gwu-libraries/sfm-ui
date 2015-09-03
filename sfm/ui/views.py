from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Collection, SeedSet, Seed
from .forms import CollectionForm, SeedSetForm, SeedForm
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import Http404

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


class SeedSetListView(ListView):
    model = SeedSet
    template_name = 'ui/seedset_list.html'
    paginate_by = 20
    context_object_name = 'seedset_list'
    allow_empty = True
    page_kwarg = 'page'
    paginate_orphans = 0

    def __init__(self, **kwargs):
        return super(SeedSetListView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(SeedSetListView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(SeedSetListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return super(SeedSetListView, self).get_queryset()

    def get_allow_empty(self):
        return super(SeedSetListView, self).get_allow_empty()

    def get_context_data(self, *args, **kwargs):
        ret = super(SeedSetListView, self).get_context_data(*args, **kwargs)
        return ret

    def get_paginate_by(self, queryset):
        return super(SeedSetListView, self).get_paginate_by(queryset)

    def get_context_object_name(self, object_list):
        return super(SeedSetListView, self).get_context_object_name(object_list)

    def paginate_queryset(self, queryset, page_size):
        return super(SeedSetListView, self).paginate_queryset(queryset, page_size)

    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True):
        return super(SeedSetListView, self).get_paginator(queryset, per_page, orphans=0, allow_empty_first_page=True)

    def render_to_response(self, context, **response_kwargs):
        return super(SeedSetListView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(SeedSetListView, self).get_template_names()


class SeedSetDetailView(DetailView):
    model = SeedSet
    template_name = 'ui/seedset_detail.html'
    context_object_name = 'seedset'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'

    def __init__(self, **kwargs):
        return super(SeedSetDetailView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(SeedSetDetailView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(SeedSetDetailView, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(SeedSetDetailView, self).get_object(queryset)

    def get_queryset(self):
        return super(SeedSetDetailView, self).get_queryset()

    def get_slug_field(self):
        return super(SeedSetDetailView, self).get_slug_field()

    def get_context_data(self, **kwargs):
        ret = super(SeedSetDetailView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(SeedSetDetailView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(SeedSetDetailView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(SeedSetDetailView, self).get_template_names()


class SeedSetCreateView(CreateView):
    model = SeedSet
    form_class = SeedSetForm
    template_name = 'ui/seedset_create.html'
    success_url = reverse_lazy('seedset_list')

    def __init__(self, **kwargs):
        return super(SeedSetCreateView, self).__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        return super(SeedSetCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(SeedSetCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(SeedSetCreateView, self).post(request, *args, **kwargs)

    def get_form_class(self):
        return super(SeedSetCreateView, self).get_form_class()

    def get_form(self, form_class):
        return super(SeedSetCreateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(SeedSetCreateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(SeedSetCreateView, self).get_initial()

    def form_invalid(self, form):
        return super(SeedSetCreateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(SeedSetCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(SeedSetCreateView, self).get_context_data(**kwargs)
        return ret

    def render_to_response(self, context, **response_kwargs):
        return super(SeedSetCreateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(SeedSetCreateView, self).get_template_names()

    def get_success_url(self):
        return reverse("seedset_detail", args=(self.object.pk,))


class SeedSetUpdateView(UpdateView):
    model = SeedSet
    form_class = SeedSetForm
    template_name = 'ui/seedset_update.html'
    initial = {}
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = 'seedset'

    def __init__(self, **kwargs):
        return super(SeedSetUpdateView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(SeedSetUpdateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(SeedSetUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(SeedSetUpdateView, self).post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(SeedSetUpdateView, self).get_object(queryset)

    def get_queryset(self):
        return super(SeedSetUpdateView, self).get_queryset()

    def get_slug_field(self):
        return super(SeedSetUpdateView, self).get_slug_field()

    def get_form_class(self):
        return super(SeedSetUpdateView, self).get_form_class()

    def get_form(self, form_class):
        return super(SeedSetUpdateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(SeedSetUpdateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(SeedSetUpdateView, self).get_initial()

    def form_invalid(self, form):
        return super(SeedSetUpdateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(SeedSetUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(SeedSetUpdateView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(SeedSetUpdateView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(SeedSetUpdateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(SeedSetUpdateView, self).get_template_names()

    def get_success_url(self):
        return reverse("seedset_detail", args=(self.object.pk,))


class SeedSetDeleteView(DeleteView):
    model = SeedSet
    template_name = 'ui/seedset_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = 'seedset'

    def __init__(self, **kwargs):
        return super(SeedSetDeleteView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(SeedSetDeleteView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        return super(SeedSedDeleteView, self).post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super(SeedSetDeleteView, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(SeedSetDeleteView, self).get_object(queryset)

    def get_queryset(self):
        return super(SeedSetDeleteView, self).get_queryset()

    def get_slug_field(self):
        return super(SeedSetDeleteView, self).get_slug_field()

    def get_context_data(self, **kwargs):
        ret = super(SeedSetDeleteView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(SeedSetDeleteView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(SeedSetDeleteView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(SeedSetDeleteView, self).get_template_names()

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

    def __init__(self, **kwargs):
        return super(SeedListView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(SeedListView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(SeedListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return super(SeedListView, self).get_queryset()

    def get_allow_empty(self):
        return super(SeedListView, self).get_allow_empty()

    def get_context_data(self, *args, **kwargs):
        ret = super(SeedListView, self).get_context_data(*args, **kwargs)
        return ret

    def get_paginate_by(self, queryset):
        return super(SeedListView, self).get_paginate_by(queryset)

    def get_context_object_name(self, object_list):
        return super(SeedListView, self).get_context_object_name(object_list)

    def paginate_queryset(self, queryset, page_size):
        return super(SeedListView, self).paginate_queryset(queryset, page_size)

    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True):
        return super(SeedListView, self).get_paginator(queryset, per_page, orphans=0, allow_empty_first_page=True)

    def render_to_response(self, context, **response_kwargs):
        return super(SeedListView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(SeedListView, self).get_template_names()


class SeedDetailView(DetailView):
    model = Seed
    template_name = 'ui/seed_detail.html'
    context_object_name = 'seed'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'

    def __init__(self, **kwargs):
        return super(SeedDetailView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(SeedDetailView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(SeedDetailView, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(SeedDetailView, self).get_object(queryset)

    def get_queryset(self):
        return super(SeedDetailView, self).get_queryset()

    def get_slug_field(self):
        return super(SeedDetailView, self).get_slug_field()

    def get_context_data(self, **kwargs):
        ret = super(SeedDetailView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(SeedDetailView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(SeedDetailView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(SeedDetailView, self).get_template_names()


class SeedCreateView(CreateView):
    model = Seed
    form_class = SeedForm
    template_name = 'ui/seed_create.html'
    success_url = reverse_lazy('seed_list')

    def __init__(self, **kwargs):
        return super(SeedCreateView, self).__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        return super(SeedCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(SeedCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(SeedCreateView, self).post(request, *args, **kwargs)

    def get_form_class(self):
        return super(SeedCreateView, self).get_form_class()

    def get_form(self, form_class):
        return super(SeedCreateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(SeedCreateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(SeedCreateView, self).get_initial()

    def form_invalid(self, form):
        return super(SeedCreateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(SeedCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(SeedCreateView, self).get_context_data(**kwargs)
        return ret

    def render_to_response(self, context, **response_kwargs):
        return super(SeedCreateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(SeedCreateView, self).get_template_names()

    def get_success_url(self):
        return reverse("seed_detail", args=(self.object.pk,))


class SeedUpdateView(UpdateView):
    model = Seed
    form_class = SeedForm
    template_name = 'ui/seed_update.html'
    initial = {}
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = 'seed'

    def __init__(self, **kwargs):
        return super(SeedUpdateView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(SeedUpdateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(SeedUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(SeedUpdateView, self).post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(SeedUpdateView, self).get_object(queryset)

    def get_queryset(self):
        return super(SeedUpdateView, self).get_queryset()

    def get_slug_field(self):
        return super(SeedUpdateView, self).get_slug_field()

    def get_form_class(self):
        return super(SeedUpdateView, self).get_form_class()

    def get_form(self, form_class):
        return super(SeedUpdateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(SeedUpdateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(SeedUpdateView, self).get_initial()

    def form_invalid(self, form):
        return super(SeedUpdateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(SeedUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(SeedUpdateView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(SeedUpdateView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(SeedUpdateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(SeedUpdateView, self).get_template_names()

    def get_success_url(self):
        return reverse("seed_detail", args=(self.object.pk,))


class SeedDeleteView(DeleteView):
    model = Seed
    template_name = 'ui/seed_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = 'seed'

    def __init__(self, **kwargs):
        return super(SeedDeleteView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(SeedDeleteView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        return super(SeedDeleteView, self).post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super(SeedDeleteView, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(SeedDeleteView, self).get_object(queryset)

    def get_queryset(self):
        return super(SeedDeleteView, self).get_queryset()

    def get_slug_field(self):
        return super(SeedDeleteView, self).get_slug_field()

    def get_context_data(self, **kwargs):
        ret = super(SeedDeleteView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(SeedDeleteView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(SeedDeleteView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(SeedDeleteView, self).get_template_names()

    def get_success_url(self):
        return reverse('seed_list')
