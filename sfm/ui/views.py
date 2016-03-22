from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Count
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from braces.views import LoginRequiredMixin

from .forms import CollectionForm, SeedSetForm, SeedForm, CredentialForm
from .forms import CredentialFlickrForm, CredentialTwitterForm, CredentialWeiboForm
from .models import Collection, SeedSet, Seed, Credential, Harvest
from .sched import next_run_time
from .utils import diff_object_history
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
        collection = kwargs["object"]
        context["diffs"] = diff_object_history(collection)
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
        seed_set = kwargs["object"]
        context["next_run_time"] = next_run_time(seed_set.id)
        context["harvests"] = Harvest.objects.filter(historical_seed_set__id=seed_set.id)
        context["diffs"] = diff_object_history(seed_set)
        return context


class SeedSetCreateView(LoginRequiredMixin, CreateView):
    model = SeedSet
    form_class = SeedSetForm
    template_name = 'ui/seedset_create.html'

    def get_initial(self):
        initial = super(SeedSetCreateView, self).get_initial()
        initial["collection"] = Collection.objects.get(
           pk=self.kwargs["collection_pk"])
        return initial

    def get_context_data(self, **kwargs):
        context = super(SeedSetCreateView, self).get_context_data(**kwargs)
        context["collection"] = Collection.objects.get(
                                    pk=self.kwargs["collection_pk"])
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
        initial["collection"] = Collection.objects.get(
                                    pk=self.kwargs["collection_pk"])
        return initial

    def get_context_data(self, **kwargs):
        context = super(SeedSetUpdateView, self).get_context_data(**kwargs)
        context["collection"] = Collection.objects.get(
                                    pk=self.kwargs["collection_pk"])
        return context

    def get_form_kwargs(self):
        kwargs = super(SeedSetUpdateView, self).get_form_kwargs()
        kwargs["coll"] = self.kwargs["collection_pk"]
        return kwargs

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

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SeedDetailView, self).get_context_data(**kwargs)
        seed = kwargs["object"]
        context["diffs"] = diff_object_history(seed)
        return context


class SeedCreateView(CreateView):
    model = Seed
    form_class = SeedForm
    template_name = 'ui/seed_create.html'
    success_url = reverse_lazy('seed_list')


class SeedUpdateView(UpdateView):
    model = Seed
    form_class = SeedForm
    template_name = 'ui/seed_update.html'
    initial = {'history_note': ''}

    def get_success_url(self):
        return reverse("seed_detail", args=(self.object.pk,))


class SeedDeleteView(DeleteView):
    model = Seed
    template_name = 'ui/seed_delete.html'
    success_url = reverse_lazy('seed_list')


class CredentialDetailView(LoginRequiredMixin, DetailView):
    model = Credential
    template_name = 'ui/credential_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CredentialDetailView, self).get_context_data(**kwargs)
        credential = kwargs["object"]
        context["diffs"] = diff_object_history(credential)
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


class CredentialDeleteView(DeleteView):
    model = Credential
    form_class = CredentialForm
    success_url = reverse_lazy('credential_list')
