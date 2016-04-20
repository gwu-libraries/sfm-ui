from django import forms
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Button, Submit
from crispy_forms.bootstrap import FormActions
from .models import Collection, SeedSet, Seed, Credential, Export
from datetimewidget.widgets import DateTimeWidget

import json
import logging

log = logging.getLogger(__name__)

HISTORY_NOTE_LABEL = "Change Note"
HISTORY_NOTE_HELP = "Optional note describing the reason for this change."
HISTORY_NOTE_WIDGET = forms.Textarea(attrs={'rows': 4})

DATETIME_WIDGET = DateTimeWidget(
    usel10n=True,
    bootstrap_version=3,
    attrs={'data-readonly': 'false'},
    options={
        'showMeridian': True
    }
)


class CollectionForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = Collection
        fields = ['name', 'description', 'group', 'history_note']
        exclude = []
        widgets = {
            'history_note': HISTORY_NOTE_WIDGET
        }
        localized_fields = None
        labels = {
            'history_note': HISTORY_NOTE_LABEL
        }
        help_texts = {
            'history_note': HISTORY_NOTE_HELP
        }
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
                'group',
                'history_note'
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
                  'schedule_minutes', 'credential',
                  'harvest_options', 'date_added', 'end_date',
                  'history_note']
        exclude = []
        widgets = {'collection': forms.HiddenInput,
                   'date_added': forms.HiddenInput,
                   'end_date': DATETIME_WIDGET,
                   'history_note': HISTORY_NOTE_WIDGET}
        localized_fields = None
        labels = {
            'history_note': HISTORY_NOTE_LABEL
        }
        help_texts = {
            'history_note': HISTORY_NOTE_HELP
        }
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
                'harvest_type',
                'credential',
                'harvest_options',
                'schedule_minutes',
                'end_date',
                'description',
                'collection',
                'date_added',
                'history_note'
            ),
            FormActions(
                Submit('submit', 'Save'),
                Button('cancel', 'Cancel',
                       onclick="window.location.href='{0}'".format(cancel_url))
            )
        )

    def clean_end_date(self):
        data = self.cleaned_data.get('end_date', None)
        if data:
            if data < timezone.now():
                raise forms.ValidationError(
                    'End date must be later than current date and time.')
            return data


class SeedForm(forms.ModelForm):

    class Meta:
        model = Seed
        fields = ['seed_set', 'token', 'uid', 'is_active', 'is_valid',
                  'date_added', 'history_note']
        exclude = []
        widgets = {
            'token': forms.TextInput(attrs={'size': '40'}),
            'uid': forms.TextInput(attrs={'size': '40'}),
            'seed_set': forms.HiddenInput,
            'date_added': forms.HiddenInput,
            'is_active': forms.HiddenInput,
            'is_valid': forms.HiddenInput,
            'history_note': HISTORY_NOTE_WIDGET
        }
        localized_fields = None
        labels = {
            'history_note': HISTORY_NOTE_LABEL
        }
        help_texts = {
            'history_note': HISTORY_NOTE_HELP
        }
        error_messages = {}

    def __init__(self, *args, **kwargs):
        self.seedset = kwargs.pop("seedset", None)
        super(SeedForm, self).__init__(*args, **kwargs)
        cancel_url = reverse('seedset_detail', args=[self.seedset])
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',
                'token',
                'uid',
                'history_note'
            ),
            FormActions(
                Submit('submit', 'Save'),
                Button('cancel', 'Cancel',
                       onclick="window.location.href='{0}'".format(cancel_url))
            )
        )

        return super(SeedForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        return super(SeedForm, self).is_valid()


class CredentialFlickrForm(forms.ModelForm):

    key = forms.CharField()
    secret = forms.CharField()
    platform = forms.CharField(widget=forms.HiddenInput(), initial='flickr')

    class Meta:
        model = Credential
        fields = ['name', 'platform', 'key', 'secret', 'history_note']
        exclude = []
        widgets = {
            'token': forms.HiddenInput(),
            'date_added': forms.HiddenInput(),
            'history_note': HISTORY_NOTE_WIDGET
        }
        localized_fields = None
        labels = {
            'history_note': HISTORY_NOTE_LABEL
        }
        help_texts = {
            'history_note': HISTORY_NOTE_HELP
        }
        error_messages = {}

    def __init__(self, *args, **kwargs):
        super(CredentialFlickrForm, self).__init__(*args, **kwargs)
        # set up crispy forms helper
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'key',
                'secret',
                'history_note'
            ),
            FormActions(
                Submit('submit', 'Save'),
                Button('cancel', 'Cancel', onclick="window.history.back()")
            )
        )

    def save(self, commit=True):
        m = super(CredentialFlickrForm, self).save(commit=False)
        m.token = {
            "key": self.cleaned_data["key"],
            "secret": self.cleaned_data["secret"]
        }
        m.token = json.dumps(m.token)
        m.save()
        return m


class CredentialTwitterForm(forms.ModelForm):

    consumer_key = forms.CharField()
    consumer_secret = forms.CharField()
    access_token = forms.CharField()
    access_token_secret = forms.CharField()
    platform = forms.CharField(widget=forms.HiddenInput(), initial='twitter')

    class Meta:
        model = Credential
        fields = ['name', 'platform', 'consumer_key', 'consumer_secret',
                  'access_token', 'access_token_secret', 'history_note']
        exclude = []
        widgets = {
            'token': forms.HiddenInput(),
            'date_added': forms.HiddenInput(),
            'history_note': HISTORY_NOTE_WIDGET
        }
        localized_fields = None
        labels = {
            'history_note': HISTORY_NOTE_LABEL
        }
        help_texts = {
            'history_note': HISTORY_NOTE_HELP
        }
        error_messages = {}

    def __init__(self, *args, **kwargs):
        super(CredentialTwitterForm, self).__init__(*args, **kwargs)
        # set up crispy forms helper
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'consumer_key',
                'consumer_secret',
                'access_token',
                'access_token_secret',
                'history_note'
            ),
            FormActions(
                Submit('submit', 'Save'),
                Button('cancel', 'Cancel', onclick="window.history.back()")
            )
        )

    def save(self, commit=True):
        m = super(CredentialTwitterForm, self).save(commit=False)
        m.token = {
            "consumer_key": self.cleaned_data["consumer_key"],
            "consumer_secret": self.cleaned_data["consumer_secret"],
            "access_token": self.cleaned_data["access_token"],
            "access_token_secret": self.cleaned_data["access_token_secret"],
        }
        m.token = json.dumps(m.token)
        m.save()
        return m


class CredentialWeiboForm(forms.ModelForm):

    api_key = forms.CharField()
    api_secret = forms.CharField()
    redirect_uri = forms.CharField()
    access_token = forms.CharField()
    platform = forms.CharField(widget=forms.HiddenInput(), initial='weibo')

    class Meta:
        model = Credential
        fields = ['name', 'platform', 'api_key', 'api_secret', 'redirect_uri',
                  'access_token', 'history_note']
        exclude = []
        widgets = {
            'token': forms.HiddenInput(),
            'date_added': forms.HiddenInput(),
            'history_note': HISTORY_NOTE_WIDGET
        }
        localized_fields = None
        labels = {
            'history_note': HISTORY_NOTE_LABEL
        }
        help_texts = {
            'history_note': HISTORY_NOTE_HELP
        }
        error_messages = {}

    def __init__(self, *args, **kwargs):
        super(CredentialWeiboForm, self).__init__(*args, **kwargs)
        self.fields['redirect_uri'].label = "Redirect URI"
        # set up crispy forms helper
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'api_key',
                'api_secret',
                'redirect_uri',
                'access_token',
                'history_note'
            ),
            FormActions(
                Submit('submit', 'Save'),
                Button('cancel', 'Cancel', onclick="window.history.back()")
            )
        )

    def save(self, commit=True):
        m = super(CredentialWeiboForm, self).save(commit=False)
        m.token = {
            "api_key": self.cleaned_data["api_key"],
            "api_secret": self.cleaned_data["api_secret"],
            "redirect_uri": self.cleaned_data["redirect_uri"],
            "access_token": self.cleaned_data["access_token"],
        }
        m.token = json.dumps(m.token)
        m.save()
        return m


class CredentialForm(forms.ModelForm):

    class Meta:
        model = Credential
        fields = ['name', 'platform', 'token', 'is_active', 'history_note']
        exclude = []
        widgets = {
            'platform': forms.TextInput(attrs={'readonly': 'readonly'}),
            'date_added': forms.HiddenInput(),
            'history_note': HISTORY_NOTE_WIDGET
        }
        localized_fields = None
        labels = {
            'history_note': HISTORY_NOTE_LABEL
        }
        help_texts = {
            'history_note': HISTORY_NOTE_HELP
        }
        error_messages = {}

    def __init__(self, *args, **kwargs):
        super(CredentialForm, self).__init__(*args, **kwargs)
        # set up crispy forms helper
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'platform',
                'token',
                'is_active',
                'history_note'
            ),
            FormActions(
                Submit('submit', 'Save'),
                Button('cancel', 'Cancel', onclick="window.history.back()")
            )
        )

    def save(self, commit=True):
        return super(CredentialForm, self).save(commit)


class ExportForm(forms.ModelForm):

    class Meta:
        model = Export
        fields = ['seeds', 'export_format', 'dedupe',
                  'item_date_start', 'item_date_end',
                  'harvest_date_start', 'harvest_date_end']
        localized_fields = None
        error_messages = {}
        help_texts = {
            'seeds': "If no seeds are selected, all seeds will be exported."
        }
        widgets = {
            'item_date_start': DATETIME_WIDGET,
            'item_date_end': DATETIME_WIDGET,
            'harvest_date_start': DATETIME_WIDGET,
            'harvest_date_end': DATETIME_WIDGET,
        }

    def __init__(self, *args, **kwargs):
        self.seedset = SeedSet.objects.get(pk=kwargs.pop("seedset"))
        super(ExportForm, self).__init__(*args, **kwargs)
        self.fields["seeds"].queryset = self.seedset.seeds.all()
        cancel_url = reverse('export_detail', args=[self.seedset.id])
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',
                'seeds',
                'export_format',
                'dedupe',
                'item_date_start',
                'item_date_end',
                'harvest_date_start',
                'harvest_date_end'
            ),
            FormActions(
                Submit('submit', 'Save'),
                Button('cancel', 'Cancel',
                       onclick="window.location.href='{0}'".format(cancel_url))
            )
        )

    def save(self, commit=True):
        m = super(ExportForm, self).save(commit=False)
        # This may need to change.
        m.export_type = self.seedset.harvest_type
        if not self.cleaned_data.get("seeds"):
            m.seed_set = self.seedset
        m.save()
        self.save_m2m()
        return m
