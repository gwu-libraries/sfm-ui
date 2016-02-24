from django import forms
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Button, Submit
from crispy_forms.bootstrap import FormActions

from .models import Collection, SeedSet, Seed, Credential


class CollectionForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = Collection
        fields = ['name', 'description', 'group']
        exclude = []
        widgets = None
        localized_fields = None
        labels = {}
        help_texts = {}
        error_messages = {}

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')

        super(CollectionForm, self).__init__(*args, **kwargs)
        # limiting groups in dropdown to user's
        self.fields['group'].queryset = Group.objects.filter(
            pk__in=request.user.groups.all())

        # set up crispy forms helper
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'description',
                'group'
            ),
            FormActions(
                Submit('submit', 'Save'),
                Button('cancel', 'Cancel', onclick="window.history.back()")
            )
        )


class SeedSetForm(forms.ModelForm):

    class Meta:
        model = SeedSet
        fields = ['name', 'harvest_type', 'description', 'collection',
                  'is_active', 'schedule_minutes', 'credential',
                  'harvest_options', 'date_added', 'start_date', 'end_date']
        exclude = []
        widgets = {'collection': forms.HiddenInput,
                   'date_added': forms.HiddenInput,
                   'is_active': forms.HiddenInput}
        localized_fields = None
        labels = {}
        help_texts = {}
        error_messages = {}

    def __init__(self, *args, **kwargs):
        self.coll = kwargs.pop("coll", None)
        super(SeedSetForm, self).__init__(*args, **kwargs)
        cancel_url = reverse('collection_detail', args=[self.coll])
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'description',
                'harvest_type',
                'harvest_options',
                'schedule_minutes',
                'start_date',
                'end_date',
                'credential',
                'is_active',
                'collection',
                'date_added',
            ),
            FormActions(
                Submit('submit', 'Save'),
                Button('cancel', 'Cancel',
                       onclick="window.location.href='{0}'".format(cancel_url))
            )
        )

    def clean_start_date(self):
        data = self.cleaned_data.get('start_date', None)
        if data:
            if data < timezone.now():
                raise forms.ValidationError(
                      'Start date must be later than current date and time.')
            return data

    def clean_end_date(self):
        data = self.cleaned_data.get('end_date', None)
        if data:
            if data < timezone.now():
                raise forms.ValidationError(
                      'End date must be later than current date and time.')
            return data

    def clean(self):
        cleaned_data = super(SeedSetForm, self).clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError(
                      'End date must be later than start date.')


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


class CredentialForm(forms.ModelForm):

    class Meta:
        model = Credential
        fields = '__all__'
        exclude = []
        widgets = None
        localized_fields = None
        labels = {}
        help_texts = {}
        error_messages = {}

    def __init__(self, *args, **kwargs):
        return super(CredentialForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        return super(CredentialForm, self).is_valid()

    def full_clean(self):
        return super(CredentialForm, self).full_clean()

    def save(self, commit=True):
        return super(CredentialForm, self).save(commit)
