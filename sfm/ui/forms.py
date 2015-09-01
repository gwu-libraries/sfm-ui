from django import forms
from .models import Collection


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

    def clean_user_group(self):
        user_group = self.cleaned_data.get('user_group', None)
        return user_group

    def clean_name(self):
        name = self.cleaned_data.get('name', None)
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description', None)
        return description

    def clean_date_created(self):
        date_created = self.cleaned_data.get('date_created', None)
        return date_created

    def clean_date_updated(self):
        date_updated = self.cleaned_data.get('date_updated', None)
        return date_updated

    def clean_date_added(self):
        date_added = self.cleaned_data.get('date_added', None)
        return date_added

    def clean_is_visible(self):
        is_visible = self.cleaned_data.get('is_visible', None)
        return is_visible

    def clean_is_active(self):
        is_active = self.cleaned_data.get('is_active', None)
        return is_active

    def clean_stats(self):
        stats = self.cleaned_data.get('stats', None)
        return stats

    def clean(self):
        return super(CollectionForm, self).clean()

    def validate_unique(self):
        return super(CollectionForm, self).validate_unique()

    def save(self, commit=True):
        return super(CollectionForm, self).save(commit)
