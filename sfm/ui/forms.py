from django import forms
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Button, Submit, Div
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


class BaseSeedSetForm(forms.ModelForm):

    class Meta:
        model = SeedSet
        fields = ['name', 'description', 'collection',
                  'schedule_minutes', 'credential', 'end_date',
                  'history_note']
        exclude = []
        widgets = {'collection': forms.HiddenInput,
                   'history_note': HISTORY_NOTE_WIDGET}
        labels = {
            'history_note': HISTORY_NOTE_LABEL
        }
        help_texts = {
            'history_note': HISTORY_NOTE_HELP
        }
        error_messages = {}

    def __init__(self, *args, **kwargs):
        self.coll = kwargs.pop("coll", None)
        super(BaseSeedSetForm, self).__init__(*args, **kwargs)
        cancel_url = reverse('collection_detail', args=[self.coll])
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'credential',
                Div(),
                'schedule_minutes',
                'end_date',
                'description',
                'collection',
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


class TwitterUserTimelineForm(BaseSeedSetForm):
    incremental = forms.BooleanField(initial=True, required=False)

    def __init__(self, *args, **kwargs):
        super(TwitterUserTimelineForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][2].append('incremental')

        if self.instance and self.instance.harvest_options:
            harvest_options = json.loads(self.instance.harvest_options)
            if "incremental" in harvest_options:
                self.fields['incremental'].initial = harvest_options["incremental"]

    def save(self, commit=True):
        m = super(TwitterUserTimelineForm, self).save(commit=False)
        m.harvest_type = SeedSet.TWITTER_USER_TIMELINE
        harvest_options = {
            "incremental": self.cleaned_data["incremental"]
        }
        m.harvest_options = json.dumps(harvest_options)
        m.save()
        return m


class TwitterSearchForm(BaseSeedSetForm):
    incremental = forms.BooleanField(initial=True, required=False)

    def __init__(self, *args, **kwargs):
        super(TwitterSearchForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][2].append('incremental')

        if self.instance and self.instance.harvest_options:
            harvest_options = json.loads(self.instance.harvest_options)
            if "incremental" in harvest_options:
                self.fields['incremental'].initial = harvest_options["incremental"]

    def save(self, commit=True):
        m = super(TwitterSearchForm, self).save(commit=False)
        m.harvest_type = SeedSet.TWITTER_SEARCH
        harvest_options = {
            "incremental": self.cleaned_data["incremental"]
        }
        m.harvest_options = json.dumps(harvest_options)
        m.save()
        return m


class TwitterSampleForm(BaseSeedSetForm):
    incremental = forms.BooleanField(initial=True, required=False)

    class Meta(BaseSeedSetForm.Meta):
        exclude = ('schedule_minutes',)

    def __init__(self, *args, **kwargs):
        super(TwitterSampleForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][2].append('incremental')

        if self.instance and self.instance.harvest_options:
            harvest_options = json.loads(self.instance.harvest_options)
            if "incremental" in harvest_options:
                self.fields['incremental'].initial = harvest_options["incremental"]

    def save(self, commit=True):
        m = super(TwitterSampleForm, self).save(commit=False)
        m.harvest_type = SeedSet.TWITTER_SAMPLE
        harvest_options = {
            "incremental": self.cleaned_data["incremental"]
        }
        m.harvest_options = json.dumps(harvest_options)
        m.schedule_minutes = None
        m.save()
        return m


class TwitterFilterForm(BaseSeedSetForm):
    incremental = forms.BooleanField(initial=True, required=False)

    class Meta(BaseSeedSetForm.Meta):
        exclude = ('schedule_minutes',)

    def __init__(self, *args, **kwargs):
        super(TwitterFilterForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][2].append('incremental')

        if self.instance and self.instance.harvest_options:
            harvest_options = json.loads(self.instance.harvest_options)
            if "incremental" in harvest_options:
                self.fields['incremental'].initial = harvest_options["incremental"]

    def save(self, commit=True):
        m = super(TwitterFilterForm, self).save(commit=False)
        m.harvest_type = SeedSet.TWITTER_FILTER
        harvest_options = {
            "incremental": self.cleaned_data["incremental"]
        }
        m.harvest_options = json.dumps(harvest_options)
        m.schedule_minutes = None
        m.save()
        return m


class FlickrUserForm(BaseSeedSetForm):
    #TODO Get correct sizes from https://www.flickr.com/services/api/flickr.photos.getSizes.html
    SIZE_OPTIONS = (
        ("Thumbnail", "Thumbnail"),
        ("Large", "Large"),
        ("Original", "Original")
    )
    sizes = forms.MultipleChoiceField(choices=SIZE_OPTIONS, initial=("Thumbnail", "Large", "Original"))
    incremental = forms.BooleanField(initial=True, required=False)

    def __init__(self, *args, **kwargs):
        super(FlickrUserForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][2].extend(('sizes','incremental'))

        if self.instance and self.instance.harvest_options:
            harvest_options = json.loads(self.instance.harvest_options)
            if "incremental" in harvest_options:
                self.fields['incremental'].initial = harvest_options["incremental"]
                self.fields['sizes'].initial = harvest_options["sizes"]

    def save(self, commit=True):
        m = super(FlickrUserForm, self).save(commit=False)
        m.harvest_type = SeedSet.FLICKR_USER
        log.info("")
        harvest_options = {
            "incremental": self.cleaned_data["incremental"],
            "sizes": self.cleaned_data["sizes"]
        }
        m.harvest_options = json.dumps(harvest_options)
        m.save()
        return m


class WeiboTimelineForm(BaseSeedSetForm):
    incremental = forms.BooleanField(initial=True, required=False)

    def __init__(self, *args, **kwargs):
        super(WeiboTimelineForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][2].append('incremental')

        if self.instance and self.instance.harvest_options:
            harvest_options = json.loads(self.instance.harvest_options)
            if "incremental" in harvest_options:
                self.fields['incremental'].initial = harvest_options["incremental"]

    def save(self, commit=True):
        m = super(WeiboTimelineForm, self).save(commit=False)
        m.harvest_type = SeedSet.WEIBO_TIMELINE
        harvest_options = {
            "incremental": self.cleaned_data["incremental"]
        }
        m.harvest_options = json.dumps(harvest_options)
        m.save()
        return m



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
                'is_active',
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


class BaseCredentialForm(forms.ModelForm):

    class Meta:
        model = Credential
        fields = ['name', 'history_note']
        exclude = []
        widgets = {
            # 'platform': forms.HiddenInput(),
            #TODO: Is this necessary?
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
        super(BaseCredentialForm, self).__init__(*args, **kwargs)
        # set up crispy forms helper
        self.helper = FormHelper(self)
        # set up crispy forms helper
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                Div(),
                'history_note'
            ),
            FormActions(
                Submit('submit', 'Save'),
                Button('cancel', 'Cancel', onclick="window.history.back()")
            )
        )


class CredentialFlickrForm(BaseCredentialForm):
    key = forms.CharField(required=True)
    secret = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(CredentialFlickrForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][1].extend(['key', 'secret'])

        if self.instance and self.instance.token:
            token = json.loads(self.instance.token)
            self.fields['key'].initial = token.get('key')
            self.fields['secret'].initial = token.get('secret')

    def save(self, commit=True):
        m = super(CredentialFlickrForm, self).save(commit=False)
        m.platform = Credential.FLICKR
        m.token = {
            "key": self.cleaned_data["key"],
            "secret": self.cleaned_data["secret"]
        }
        m.token = json.dumps(m.token)
        m.save()
        return m


class CredentialTwitterForm(BaseCredentialForm):
    consumer_key = forms.CharField(required=True)
    consumer_secret = forms.CharField(required=True)
    access_token = forms.CharField(required=True)
    access_token_secret = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(CredentialTwitterForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][1].extend(['consumer_key', 'consumer_key', 'access_token', 'access_token_secret'])
        if self.instance and self.instance.token:
            token = json.loads(self.instance.token)
            self.fields['consumer_key'].initial = token.get('consumer_key')
            self.fields['consumer_secret'].initial = token.get('consumer_secret')
            self.fields['access_token'].initial = token.get('access_token')
            self.fields['access_token_secret'].initial = token.get('access_token_secret')

    def save(self, commit=True):
        m = super(CredentialTwitterForm, self).save(commit=False)
        m.platform = Credential.TWITTER
        token = {
            "consumer_key": self.cleaned_data["consumer_key"],
            "consumer_secret": self.cleaned_data["consumer_secret"],
            "access_token": self.cleaned_data["access_token"],
            "access_token_secret": self.cleaned_data["access_token_secret"],
        }
        m.token = json.dumps(token)
        m.save()
        return m


class CredentialWeiboForm(BaseCredentialForm):
    api_key = forms.CharField(required=True)
    api_secret = forms.CharField(required=True)
    redirect_uri = forms.CharField(required=True)
    access_token = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(CredentialWeiboForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][1].extend(['api_key', 'api_secret', 'redirect_uri', 'access_token'])

        if self.instance and self.instance.token:
            token = json.loads(self.instance.token)
            self.fields['api_key'].initial = token.get('api_key')
            self.fields['api_secret'].initial = token.get('api_secret')
            self.fields['redirect_uri'].initial = token.get('redirect_uri')
            self.fields['access_token'].initial = token.get('access_token')

    def save(self, commit=True):
        m = super(CredentialWeiboForm, self).save(commit=False)
        m.platform = Credential.WEIBO
        token = {
            "api_key": self.cleaned_data["api_key"],
            "api_secret": self.cleaned_data["api_secret"],
            "redirect_uri": self.cleaned_data["redirect_uri"],
            "access_token": self.cleaned_data["access_token"],
        }
        m.token = json.dumps(token)
        m.save()
        return m


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
