from django import forms
from .models import Collection, SeedSet, Seed


class CollectionForm(forms.ModelForm):

    class Meta:
        model = Collection
        fields = '__all__'
        exclude = []
        widgets = None
        localized_fields = None
        labels = {}
        help_texts = {}
        error_messages = {}

    def __init__(self, *args, **kwargs):
        return super(CollectionForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        return super(CollectionForm, self).is_valid()

    def full_clean(self):
        return super(CollectionForm, self).full_clean()

    def save(self, commit=True):
        return super(CollectionForm, self).save(commit)


class SeedSetForm(forms.ModelForm):

    class Meta:
        model = SeedSet
        fields = '__all__'
        exclude = []
        widgets = None
        localized_fields = None
        labels = {}
        help_texts = {}
        error_messages = {}

    def __init__(self, *args, **kwargs):
        return super(SeedSetForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        return super(SeedSetForm, self).is_valid()

    def full_clean(self):
        return super(SeedSetForm, self).full_clean()

    def save(self, commit=True):
        return super(SeedSetForm, self).save(commit)


class SeedForm(forms.ModelForm):

    class Meta:
        model = Seed
        fields = '__all__'
        exclude = []
        widgets = None
        localized_fields = None
        labels = {}
        help_texts = {}
        error_messages = {}

    def __init__(self, *args, **kwargs):
        return super(SeedForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        return super(SeedForm, self).is_valid()

    def full_clean(self):
        return super(SeedForm, self).full_clean()

    def save(self, commit=True):
        return super(SeedForm, self).save(commit)
