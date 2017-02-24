#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Button, Submit, Div
from crispy_forms.bootstrap import FormActions
from datetimewidget.widgets import DateTimeWidget
from .models import CollectionSet, Collection, Seed, Credential, Export, User
from .utils import clean_token, clean_blogname

import json
import logging
import re

log = logging.getLogger(__name__)

HISTORY_NOTE_LABEL = "Change Note"
HISTORY_NOTE_HELP = "Explain why you made these changes at this time."
HISTORY_NOTE_HELP_ADD = "Further information about this addition."
HISTORY_NOTE_WIDGET = forms.Textarea(attrs={'rows': 4})

DATETIME_WIDGET = DateTimeWidget(
    usel10n=True,
    bootstrap_version=3,
    attrs={'data-readonly': 'false'},
    options={
        'showMeridian': True
    }
)

TWITTER_MEDIA_LABEL = "Media"
TWITTER_MEDIA_HELP = "Perform web harvests of media (e.g., images) embedded in tweets."
TWITTER_WEB_RESOURCES_LABEL = "Web resources"
TWITTER_WEB_RESOURCES_HELP = "Perform web harvests of resources (e.g., web pages) linked in tweets."
INCREMENTAL_LABEL = "Incremental"
INCREMENTAL_HELP = "Only harvest new items."
GROUP_HELP = "Group members will be able to view and edit this collection set."
USER_PROFILE_LABEL = "User profile images"
USER_PROFILE_HELP = "Perform web harvests of user profile images and user banner images"


class CollectionSetForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = CollectionSet
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
            'history_note': HISTORY_NOTE_HELP,
        }
        error_messages = {}

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')

        super(CollectionSetForm, self).__init__(*args, **kwargs)
        # limiting groups in dropdown to user's and setting default if only 1 value.
        group_queryset = Group.objects.filter(pk__in=request.user.groups.all())
        if len(group_queryset) == 1:
            self.initial['group'] = group_queryset[0]
        self.fields['group'].queryset = group_queryset
        self.fields['group'].help_text = GROUP_HELP

        # check whether it's a CreateView and offer different help text
        if self.instance.pk is None:
            self.fields['history_note'].help_text = HISTORY_NOTE_HELP_ADD

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


class NameModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class BaseCollectionForm(forms.ModelForm):
    credential = NameModelChoiceField(None)

    class Meta:
        model = Collection
        fields = ['name', 'description', 'collection_set',
                  'schedule_minutes', 'credential', 'end_date',
                  'history_note']
        exclude = []
        widgets = {'collection_set': forms.HiddenInput,
                   'history_note': HISTORY_NOTE_WIDGET,
                   'end_date': DATETIME_WIDGET}
        labels = {
            'history_note': HISTORY_NOTE_LABEL
        }
        help_texts = {
            'history_note': HISTORY_NOTE_HELP
        }
        error_messages = {}

    def __init__(self, *args, **kwargs):
        self.coll = kwargs.pop("coll", None)
        self.credential_list = kwargs.pop('credential_list', None)
        super(BaseCollectionForm, self).__init__(*args, **kwargs)

        # Set default if only 1 value.
        if len(self.credential_list) == 1:
            self.initial['credential'] = self.credential_list[0]
        self.fields['credential'].queryset = self.credential_list

        # check whether it's a create view and offer different help text
        if self.instance.pk is None:
            self.fields['history_note'].help_text = HISTORY_NOTE_HELP_ADD

        cancel_url = reverse('collection_set_detail', args=[self.coll])
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'description',
                'credential',
                Div(css_id='credential_warning'),
                Div(),
                'schedule_minutes',
                'end_date',
                'collection_set',
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


class CollectionTwitterUserTimelineForm(BaseCollectionForm):
    incremental = forms.BooleanField(initial=True, required=False, help_text=INCREMENTAL_HELP, label=INCREMENTAL_LABEL)
    media_option = forms.BooleanField(initial=False, required=False, help_text=TWITTER_MEDIA_HELP,
                                      label=TWITTER_MEDIA_LABEL)
    web_resources_option = forms.BooleanField(initial=False, required=False, help_text=TWITTER_WEB_RESOURCES_HELP,
                                              label=TWITTER_WEB_RESOURCES_LABEL)
    user_images_option = forms.BooleanField(initial=False, required=False, help_text=USER_PROFILE_HELP,
                                            label=USER_PROFILE_LABEL)

    def __init__(self, *args, **kwargs):
        super(CollectionTwitterUserTimelineForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][4].extend(('incremental', 'media_option', 'user_images_option', 'web_resources_option'))

        if self.instance and self.instance.harvest_options:
            harvest_options = json.loads(self.instance.harvest_options)
            if "incremental" in harvest_options:
                self.fields['incremental'].initial = harvest_options["incremental"]
            if "media" in harvest_options:
                self.fields['media_option'].initial = harvest_options["media"]
            if "web_resources" in harvest_options:
                self.fields['web_resources_option'].initial = harvest_options["web_resources"]
            if "user_images" in harvest_options:
                self.fields['user_images_option'].initial = harvest_options["user_images"]

    def save(self, commit=True):
        m = super(CollectionTwitterUserTimelineForm, self).save(commit=False)
        m.harvest_type = Collection.TWITTER_USER_TIMELINE
        harvest_options = {
            "incremental": self.cleaned_data["incremental"],
            "media": self.cleaned_data["media_option"],
            "web_resources": self.cleaned_data["web_resources_option"],
            "user_images": self.cleaned_data["user_images_option"]
        }
        m.harvest_options = json.dumps(harvest_options, sort_keys=True)
        m.save()
        return m


class CollectionTwitterSearchForm(BaseCollectionForm):
    incremental = forms.BooleanField(initial=True, required=False, help_text=INCREMENTAL_HELP, label=INCREMENTAL_LABEL)
    media_option = forms.BooleanField(initial=False, required=False, help_text=TWITTER_MEDIA_HELP,
                                      label=TWITTER_MEDIA_LABEL)
    web_resources_option = forms.BooleanField(initial=False, required=False, help_text=TWITTER_WEB_RESOURCES_HELP,
                                              label=TWITTER_WEB_RESOURCES_LABEL)

    def __init__(self, *args, **kwargs):
        super(CollectionTwitterSearchForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][4].extend(('incremental', 'media_option', 'web_resources_option'))

        if self.instance and self.instance.harvest_options:
            harvest_options = json.loads(self.instance.harvest_options)
            if "incremental" in harvest_options:
                self.fields['incremental'].initial = harvest_options["incremental"]
            if "media" in harvest_options:
                self.fields['media_option'].initial = harvest_options["media"]
            if "web_resources" in harvest_options:
                self.fields['web_resources_option'].initial = harvest_options["web_resources"]

    def save(self, commit=True):
        m = super(CollectionTwitterSearchForm, self).save(commit=False)
        m.harvest_type = Collection.TWITTER_SEARCH
        harvest_options = {
            "incremental": self.cleaned_data["incremental"],
            "media": self.cleaned_data["media_option"],
            "web_resources": self.cleaned_data["web_resources_option"]
        }
        m.harvest_options = json.dumps(harvest_options, sort_keys=True)
        m.save()
        return m


class CollectionTwitterSampleForm(BaseCollectionForm):
    media_option = forms.BooleanField(initial=False, required=False, help_text=TWITTER_MEDIA_HELP,
                                      label=TWITTER_MEDIA_LABEL)
    web_resources_option = forms.BooleanField(initial=False, required=False, help_text=TWITTER_WEB_RESOURCES_HELP,
                                              label=TWITTER_WEB_RESOURCES_LABEL)

    class Meta(BaseCollectionForm.Meta):
        exclude = ('schedule_minutes',)

    def __init__(self, *args, **kwargs):
        super(CollectionTwitterSampleForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][4].extend(('media_option', 'web_resources_option'))
        if self.instance and self.instance.harvest_options:
            harvest_options = json.loads(self.instance.harvest_options)
            if "media" in harvest_options:
                self.fields['media_option'].initial = harvest_options["media"]
            if "web_resources" in harvest_options:
                self.fields['web_resources_option'].initial = harvest_options["web_resources"]

    def save(self, commit=True):
        m = super(CollectionTwitterSampleForm, self).save(commit=False)
        m.harvest_type = Collection.TWITTER_SAMPLE
        harvest_options = {
            "media": self.cleaned_data["media_option"],
            "web_resources": self.cleaned_data["web_resources_option"],
        }
        m.harvest_options = json.dumps(harvest_options, sort_keys=True)
        m.schedule_minutes = None
        m.save()
        return m


class CollectionTwitterFilterForm(BaseCollectionForm):
    media_option = forms.BooleanField(initial=False, required=False, help_text=TWITTER_MEDIA_HELP,
                                      label=TWITTER_MEDIA_LABEL)
    web_resources_option = forms.BooleanField(initial=False, required=False, help_text=TWITTER_WEB_RESOURCES_HELP,
                                              label=TWITTER_WEB_RESOURCES_LABEL)

    class Meta(BaseCollectionForm.Meta):
        exclude = ('schedule_minutes',)

    def __init__(self, *args, **kwargs):
        super(CollectionTwitterFilterForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][4].extend(('incremental', 'media_option', 'web_resources_option'))

        if self.instance and self.instance.harvest_options:
            harvest_options = json.loads(self.instance.harvest_options)
            if "media" in harvest_options:
                self.fields['media_option'].initial = harvest_options["media"]
            if "web_resources" in harvest_options:
                self.fields['web_resources_option'].initial = harvest_options["web_resources"]

    def save(self, commit=True):
        m = super(CollectionTwitterFilterForm, self).save(commit=False)
        m.harvest_type = Collection.TWITTER_FILTER
        harvest_options = {
            "media": self.cleaned_data["media_option"],
            "web_resources": self.cleaned_data["web_resources_option"]
        }
        m.harvest_options = json.dumps(harvest_options, sort_keys=True)
        m.schedule_minutes = None
        m.save()
        return m


class CollectionFlickrUserForm(BaseCollectionForm):
    # See https://www.flickr.com/services/api/flickr.photos.getSizes.html
    SIZE_OPTIONS = (
        ("Thumbnail", "Thumbnail"),
        ("Small", "Small"),
        ("Medium", "Medium"),
        ("Large", "Large"),
        ("Original", "Original")
    )
    image_sizes = forms.MultipleChoiceField(choices=SIZE_OPTIONS, initial=("Thumbnail", "Large", "Original"),
                                            widget=forms.CheckboxSelectMultiple, label="Image sizes", )
    incremental = forms.BooleanField(initial=True, required=False, help_text=INCREMENTAL_HELP, label=INCREMENTAL_LABEL)

    def __init__(self, *args, **kwargs):
        super(CollectionFlickrUserForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][4].extend(('incremental', 'image_sizes'))

        if self.instance and self.instance.harvest_options:
            harvest_options = json.loads(self.instance.harvest_options)
            if "incremental" in harvest_options:
                self.fields['incremental'].initial = harvest_options["incremental"]
            if "image_sizes" in harvest_options:
                self.fields['image_sizes'].initial = harvest_options["image_sizes"]

    def save(self, commit=True):
        m = super(CollectionFlickrUserForm, self).save(commit=False)
        m.harvest_type = Collection.FLICKR_USER
        harvest_options = {
            "incremental": self.cleaned_data["incremental"],
            "image_sizes": self.cleaned_data["image_sizes"]
        }
        m.harvest_options = json.dumps(harvest_options)
        m.save()
        return m


class CollectionWeiboTimelineForm(BaseCollectionForm):
    SIZE_OPTIONS = (
        ("Thumbnail", "Thumbnail"),
        ("Medium", "Medium"),
        ("Large", "Large")
    )
    incremental = forms.BooleanField(initial=True, required=False, help_text=INCREMENTAL_HELP, label=INCREMENTAL_LABEL)
    image_sizes = forms.MultipleChoiceField(required=False, choices=SIZE_OPTIONS, initial=(None,),
                                            help_text="For harvesting images, select the image sizes.",
                                            widget=forms.CheckboxSelectMultiple, label="Image sizes")
    web_resources_option = forms.BooleanField(initial=False, required=False,
                                              help_text="Perform web harvests of resources (e.g., web pages) linked in "
                                                        "weibo texts.",
                                              label="Web resources")

    def __init__(self, *args, **kwargs):
        super(CollectionWeiboTimelineForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][4].extend(('image_sizes', 'incremental', 'web_resources_option'))

        if self.instance and self.instance.harvest_options:
            harvest_options = json.loads(self.instance.harvest_options)
            if "incremental" in harvest_options:
                self.fields['incremental'].initial = harvest_options["incremental"]
            if "image_sizes" in harvest_options:
                self.fields['image_sizes'].initial = harvest_options["image_sizes"]
            if "web_resources" in harvest_options:
                self.fields['web_resources_option'].initial = harvest_options["web_resources"]

    def save(self, commit=True):
        m = super(CollectionWeiboTimelineForm, self).save(commit=False)
        m.harvest_type = Collection.WEIBO_TIMELINE
        harvest_options = {
            "incremental": self.cleaned_data["incremental"],
            "image_sizes": self.cleaned_data["image_sizes"],
            "web_resources": self.cleaned_data["web_resources_option"]
        }
        m.harvest_options = json.dumps(harvest_options, sort_keys=True)
        m.save()
        return m


class CollectionWeiboSearchForm(BaseCollectionForm):
    SIZE_OPTIONS = (
        ("Thumbnail", "Thumbnail"),
        ("Medium", "Medium"),
        ("Large", "Large")
    )
    incremental = forms.BooleanField(initial=True, required=False, help_text=INCREMENTAL_HELP, label=INCREMENTAL_LABEL)
    image_sizes = forms.MultipleChoiceField(required=False, choices=SIZE_OPTIONS, initial=(None,),
                                            help_text="For harvesting images, select the image sizes.",
                                            widget=forms.CheckboxSelectMultiple, label="Image sizes")
    web_resources_option = forms.BooleanField(initial=False, required=False,
                                              help_text="Perform web harvests of resources (e.g., web pages) linked in "
                                                        "weibo texts.",
                                              label="Web resources")

    def __init__(self, *args, **kwargs):
        super(CollectionWeiboSearchForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][4].extend(('image_sizes', 'incremental', 'web_resources_option'))

        if self.instance and self.instance.harvest_options:
            harvest_options = json.loads(self.instance.harvest_options)
            if "incremental" in harvest_options:
                self.fields['incremental'].initial = harvest_options["incremental"]
            if "image_sizes" in harvest_options:
                self.fields['image_sizes'].initial = harvest_options["image_sizes"]
            if "web_resources" in harvest_options:
                self.fields['web_resources_option'].initial = harvest_options["web_resources"]

    def save(self, commit=True):
        m = super(CollectionWeiboSearchForm, self).save(commit=False)
        m.harvest_type = Collection.WEIBO_SEARCH
        harvest_options = {
            "incremental": self.cleaned_data["incremental"],
            "image_sizes": self.cleaned_data["image_sizes"],
            "web_resources": self.cleaned_data["web_resources_option"]
        }
        m.harvest_options = json.dumps(harvest_options, sort_keys=True)
        m.save()
        return m


class CollectionTumblrBlogPostsForm(BaseCollectionForm):
    incremental = forms.BooleanField(initial=True, required=False, help_text=INCREMENTAL_HELP, label=INCREMENTAL_LABEL)
    media_option = forms.BooleanField(initial=False, required=False,
                                      help_text="Perform web harvests of images in photo type posts.",
                                      label="Images option")
    web_resources_option = forms.BooleanField(initial=False, required=False,
                                              help_text="Perform web harvests of resources (e.g., web pages) "
                                                        "linked in Tumblr posts.",
                                              label="Web resources")

    def __init__(self, *args, **kwargs):
        super(CollectionTumblrBlogPostsForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][4].extend(('incremental', 'media_option', 'web_resources_option'))

        if self.instance and self.instance.harvest_options:
            harvest_options = json.loads(self.instance.harvest_options)
            if "incremental" in harvest_options:
                self.fields['incremental'].initial = harvest_options["incremental"]
            if "media" in harvest_options:
                self.fields['media_option'].initial = harvest_options["media"]
            if "web_resources" in harvest_options:
                self.fields['web_resources_option'].initial = harvest_options["web_resources"]

    def save(self, commit=True):
        m = super(CollectionTumblrBlogPostsForm, self).save(commit=False)
        m.harvest_type = Collection.TUMBLR_BLOG_POSTS
        harvest_options = {
            "incremental": self.cleaned_data["incremental"],
            "media": self.cleaned_data["media_option"],
            "web_resources": self.cleaned_data["web_resources_option"]
        }
        m.harvest_options = json.dumps(harvest_options, sort_keys=True)
        m.save()
        return m


class BaseSeedForm(forms.ModelForm):
    class Meta:
        model = Seed
        fields = ['collection', 'is_active',
                  'history_note']
        exclude = []
        widgets = {
            'collection': forms.HiddenInput,
            'history_note': HISTORY_NOTE_WIDGET
        }
        labels = {
            'history_note': HISTORY_NOTE_LABEL
        }
        help_texts = {
            'history_note': HISTORY_NOTE_HELP
        }

    def __init__(self, *args, **kwargs):
        self.collection = kwargs.pop("collection", None)
        # for createView and updateView
        self.view_type = kwargs.pop("view_type", None)
        # for updateView check the updates for the original token and  uid
        self.entry = kwargs.pop("entry", None)
        super(BaseSeedForm, self).__init__(*args, **kwargs)
        cancel_url = reverse('collection_detail', args=[self.collection])

        # check whether it's a create view and offer different help text
        if self.instance.pk is None:
            self.fields['history_note'].help_text = HISTORY_NOTE_HELP_ADD

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',
                Div(),
                'is_active',
                'history_note'
            ),
            FormActions(
                Submit('submit', 'Save'),
                Button('cancel', 'Cancel',
                       onclick="window.location.href='{0}'".format(cancel_url))
            )
        )

    def clean_token(self):
        token_val = self.cleaned_data.get("token")
        return token_val.strip()

    def clean_uid(self):
        uid_val = self.cleaned_data.get("uid")
        return uid_val.strip()

    def clean(self):
        fields = self._meta.fields
        uid_val, token_val = '', ''
        uid_label, token_label = '', ''
        if "uid" in fields:
            uid_val = self.cleaned_data.get("uid")
            uid_label = self._meta.labels["uid"]
        if "token" in fields:
            token_val = self.cleaned_data.get("token")
            token_label = self._meta.labels["token"]

        # if has invalid error before, directly not check deep error
        if self.errors:
            return

        # should not both empty if has token or uid fields, the twitter filter should deal with separately
        if (uid_label or token_label) and (not uid_val and not token_val):
            or_text = 'or' * (1 if uid_label and token_label else 0)
            raise ValidationError(
                u'One of the following fields is required :{} {} {}.'.format(token_label, or_text, uid_label))

        # for the update view
        if self.view_type == Seed.UPDATE_VIEW:
            # check updated seeds exist in db if changes
            # case insensitive match, and user can't add 'token:TeSt' or 'token:teSt', etc if 'token:test exist.',
            # but can update to 'token:TeSt' or other.
            if token_val.lower() != self.entry.token.lower() and \
                    token_val and Seed.objects.filter(collection=self.collection,
                                                      token__iexact=token_val).exists():
                raise ValidationError(u'{}: {} already exist.'.format(token_label, token_val))
            # check updated uid whether exist in db if changes
            if uid_val.lower() != self.entry.uid.lower() and \
                    uid_val and Seed.objects.filter(collection=self.collection,
                                                    uid__iexact=uid_val).exists():
                raise ValidationError(u'{}: {} already exist.'.format(uid_label, uid_val))
        else:
            if token_val and Seed.objects.filter(collection=self.collection, token__iexact=token_val).exists():
                raise ValidationError(u'{}: {} already exist.'.format(token_label, token_val))

            if uid_val and Seed.objects.filter(collection=self.collection, uid__iexact=uid_val).exists():
                raise ValidationError(u'{}: {} already exist.'.format(uid_label, uid_val))


class SeedTwitterUserTimelineForm(BaseSeedForm):
    class Meta(BaseSeedForm.Meta):
        fields = ['token', 'uid']
        fields.extend(BaseSeedForm.Meta.fields)
        labels = dict(BaseSeedForm.Meta.labels)
        labels["token"] = "Screen name"
        labels["uid"] = "User id"
        widgets = dict(BaseSeedForm.Meta.widgets)
        widgets["token"] = forms.TextInput(attrs={'size': '40'})
        widgets["uid"] = forms.TextInput(attrs={'size': '40'})

    def __init__(self, *args, **kwargs):
        super(SeedTwitterUserTimelineForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][0].extend(('token', 'uid'))

    def clean_uid(self):
        uid_val = self.cleaned_data.get("uid")
        # check the format
        if uid_val and not uid_val.isdigit():
            raise ValidationError('Uid should be numeric.', code='invalid')
        return uid_val

    def clean_token(self):
        token_val = clean_token(self.cleaned_data.get("token"))
        # check the format
        if token_val and token_val.isdigit():
            raise ValidationError('Screen name may not be numeric.', code='invalid')
        return token_val


class SeedTwitterSearchForm(BaseSeedForm):
    class Meta(BaseSeedForm.Meta):
        fields = ['token']
        fields.extend(BaseSeedForm.Meta.fields)
        labels = dict(BaseSeedForm.Meta.labels)
        labels["token"] = "Query"
        help_texts = dict(BaseSeedForm.Meta.help_texts)
        help_texts["token"] = 'See <a href="https://dev.twitter.com/rest/public/search" target="_blank">' \
                              'these instructions</a> for writing a query. ' \
                              'Example: firefly OR "lightning bug"'
        widgets = dict(BaseSeedForm.Meta.widgets)
        widgets["token"] = forms.Textarea(attrs={'rows': 4})

    def __init__(self, *args, **kwargs):
        super(SeedTwitterSearchForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][0].append('token')


class SeedWeiboSearchForm(BaseSeedForm):
    class Meta(BaseSeedForm.Meta):
        fields = ['token']
        fields.extend(BaseSeedForm.Meta.fields)
        labels = dict(BaseSeedForm.Meta.labels)
        labels["token"] = "Query"
        help_texts = dict(BaseSeedForm.Meta.help_texts)
        help_texts["token"] = u'See <a href="http://open.weibo.com/wiki/2/search/topics" target="_blank">' \
                              u'API documents</a> for writing a query. ' \
                              u'Example: "科技".'
        widgets = dict(BaseSeedForm.Meta.widgets)
        widgets["token"] = forms.Textarea(attrs={'rows': 4})

    def __init__(self, *args, **kwargs):
        super(SeedWeiboSearchForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][0].append('token')


class SeedTwitterFilterForm(BaseSeedForm):
    track = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4}),
                            help_text='Keywords to track. Phrases of keywords are specified by a comma-separated list. '
                                      'See <a '
                                      'href="https://dev.twitter.com/streaming/overview/request-parameters#track">'
                                      'track</a> for more information.')
    follow = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4}),
                             help_text='A comma separated list of <i>user IDs</i> (not screen names), indicating the '
                                       'users to return statuses for in the stream. See <a '
                                       'href="https://dev.twitter.com/streaming/overview/request-parameters#follow">'
                                       'follow</a> for more information.')
    locations = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4}),
                                help_text='Specifies a set of bounding boxes to track. See <a href='
                                          '"https://dev.twitter.com/streaming/overview/request-parameters#locations">'
                                          'locations</a> for more information.')

    def __init__(self, *args, **kwargs):
        super(SeedTwitterFilterForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][0].extend(('track', 'follow', 'locations'))

        if self.instance and self.instance.token:
            token = json.loads(self.instance.token)
            if 'track' in token:
                self.fields['track'].initial = token['track']
            if 'follow' in token:
                self.fields['follow'].initial = token['follow']
            if 'locations' in token:
                self.fields['locations'].initial = token['locations']

    def clean_track(self):
        track_val = self.cleaned_data.get("track")
        return track_val.strip()

    def clean_locations(self):
        locations_val = self.cleaned_data.get("locations")
        return locations_val.strip()

    def clean_follow(self):
        follow_val = self.cleaned_data.get("follow")
        return follow_val.strip()

    def clean(self):
        # if do string strip in here, string ends an empty space, not sure why
        track_val = self.cleaned_data.get("track")
        follow_val = self.cleaned_data.get("follow")
        locations_val = self.cleaned_data.get("locations")

        # should not all be empty
        if not track_val and not follow_val and not locations_val:
            raise ValidationError(u'One of the following fields is required :track, follow, locations.')

        # check follow should be number uid
        if re.compile(r'[^0-9, ]').search(follow_val):
            raise ValidationError('Follow must be user ids', code='invalid_follow')

        token_val = {}
        if track_val:
            token_val['track'] = track_val
        if follow_val:
            token_val['follow'] = follow_val
        if locations_val:
            token_val['locations'] = locations_val
        token_val = json.dumps(token_val, ensure_ascii=False)
        # for the update view
        if self.view_type == Seed.UPDATE_VIEW:
            # check updated seeds exist in db if changes
            # case insensitive match, and user can update seed `tack:Test` to 'tack:test'
            if token_val.lower() != self.entry.token.lower() and \
                    token_val and Seed.objects.filter(collection=self.collection,
                                                      token__iexact=token_val).exists():
                raise ValidationError(u'Seed: {} already exist.'.format(token_val))
        else:
            if token_val and Seed.objects.filter(collection=self.collection, token__iexact=token_val).exists():
                raise ValidationError(u'Seed: {} already exist.'.format(token_val))

    def save(self, commit=True):
        m = super(SeedTwitterFilterForm, self).save(commit=False)
        token = dict()
        if self.cleaned_data['track']:
            token['track'] = self.cleaned_data['track']
        if self.cleaned_data['follow']:
            token['follow'] = self.cleaned_data['follow']
        if self.cleaned_data['locations']:
            token['locations'] = self.cleaned_data['locations']
        m.token = json.dumps(token, ensure_ascii=False)
        m.save()
        return m


class SeedFlickrUserForm(BaseSeedForm):
    class Meta(BaseSeedForm.Meta):
        fields = ['token', 'uid']
        fields.extend(BaseSeedForm.Meta.fields)
        labels = dict(BaseSeedForm.Meta.labels)
        labels["token"] = "Username"
        labels["uid"] = "NSID"
        help_texts = dict(BaseSeedForm.Meta.help_texts)
        help_texts["token"] = 'A string name for the user account. Finding this on the Flickr website can be ' \
                              'confusing, so see NSID below.'
        help_texts["uid"] = 'An unchanging identifier for a user account, e.g., 80136838@N05. To find the NSID for a ' \
                            'user account, use <a href="http://www.webpagefx.com/tools/idgettr/">idGettr</a>.'
        widgets = dict(BaseSeedForm.Meta.widgets)
        widgets["token"] = forms.TextInput(attrs={'size': '40'})
        widgets["uid"] = forms.TextInput(attrs={'size': '40'})

    def __init__(self, *args, **kwargs):
        super(SeedFlickrUserForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][0].extend(('token', 'uid'))


class SeedTumblrBlogPostsForm(BaseSeedForm):
    class Meta(BaseSeedForm.Meta):
        fields = ['uid']
        fields.extend(BaseSeedForm.Meta.fields)
        labels = dict(BaseSeedForm.Meta.labels)
        labels["uid"] = "Blog hostname"
        help_texts = dict(BaseSeedForm.Meta.help_texts)
        help_texts["uid"] = 'Please provide the standard blog hostname, eg. codingjester or codingjester.tumblr.com.' \
                            'If blog hostname is codingjester.tumblr.com, it would be considered as codingjester. ' \
                            'To better understand standard blog hostname, See ' \
                            '<a target="_blank" href="https://www.tumblr.com/docs/en/api/v2#hostname">' \
                            'these instructions</a>.'

        widgets = dict(BaseSeedForm.Meta.widgets)
        widgets["uid"] = forms.TextInput(attrs={'size': '40'})

    def __init__(self, *args, **kwargs):
        super(SeedTumblrBlogPostsForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][0].append('uid')

    def clean_uid(self):
        return clean_blogname(self.cleaned_data.get("uid"))


class BaseBulkSeedForm(forms.Form):
    TYPES = (('token', 'Username'), ('uid', 'NSID'))
    seeds_type = forms.ChoiceField(required=True, choices=TYPES, widget=forms.RadioSelect)
    tokens = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 20}),
                             help_text="Enter each seed on a separate line.", label="Bulk Seeds")
    history_note = forms.CharField(label=HISTORY_NOTE_LABEL, widget=HISTORY_NOTE_WIDGET, help_text=HISTORY_NOTE_HELP,
                                   required=False)

    def __init__(self, *args, **kwargs):
        self.collection = kwargs.pop("collection", None)
        super(BaseBulkSeedForm, self).__init__(*args, **kwargs)
        self.fields['history_note'].help_text = HISTORY_NOTE_HELP_ADD
        cancel_url = reverse('collection_detail', args=[self.collection])
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',
                'seeds_type',
                'tokens',
                'history_note'
            ),
            FormActions(
                Submit('submit', 'Save'),
                Button('cancel', 'Cancel',
                       onclick="window.location.href='{0}'".format(cancel_url))
            )
        )


class BulkSeedTwitterUserTimelineForm(BaseBulkSeedForm):
    def __init__(self, *args, **kwargs):
        super(BulkSeedTwitterUserTimelineForm, self).__init__(*args, **kwargs)
        self.fields['seeds_type'].choices = (('token', 'Screen Name'), ('uid', 'User id'))

    def clean_tokens(self):
        seed_type = self.cleaned_data.get("seeds_type")
        tokens = self.cleaned_data.get("tokens")
        splittoken = ''.join(tokens).splitlines()
        numtoken, strtoken = [], []
        for t in splittoken:
            clean_t = clean_token(t)
            if clean_t and clean_t.isdigit():
                numtoken.append(clean_t)
            elif clean_t and not clean_t.isdigit():
                strtoken.append(clean_t)
        if seed_type == 'token' and numtoken:
            raise ValidationError(
                'Screen names may not be numeric. Please correct the following seeds: ' + ', '.join(numtoken) + '.')
        elif seed_type == 'uid' and strtoken:
            raise ValidationError(
                'UIDs must be numeric. Please correct the following seeds: ' + ', '.join(strtoken) + '.')
        return tokens


class BulkSeedFlickrUserForm(BaseBulkSeedForm):
    def __init__(self, *args, **kwargs):
        super(BulkSeedFlickrUserForm, self).__init__(*args, **kwargs)


class BulkSeedTumblrBlogPostsForm(BaseBulkSeedForm):
    def __init__(self, *args, **kwargs):
        super(BulkSeedTumblrBlogPostsForm, self).__init__(*args, **kwargs)
        self.fields['seeds_type'].choices = (('uid', 'Blog hostnames'),)
        self.fields['seeds_type'].initial = 'uid'


class BaseCredentialForm(forms.ModelForm):
    class Meta:
        model = Credential
        fields = ['name', 'history_note']
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
        super(BaseCredentialForm, self).__init__(*args, **kwargs)

        # check whether it's a create view and offer different help text
        if self.instance.pk is None:
            self.fields['history_note'].help_text = HISTORY_NOTE_HELP_ADD

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

    def clean(self):
        cleaned_data = super(BaseCredentialForm, self).clean()
        token = json.dumps(self.to_token())
        if Credential.objects.filter(token=token).exists():
            raise ValidationError('This is a duplicate of an existing credential')
        return cleaned_data


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

    def to_token(self):
        return {
            "key": self.cleaned_data["key"].strip(),
            "secret": self.cleaned_data["secret"].strip(),
        }

    def save(self, commit=True):
        m = super(CredentialFlickrForm, self).save(commit=False)
        m.platform = Credential.FLICKR
        m.token = json.dumps(self.to_token())
        m.save()
        return m


class CredentialTwitterForm(BaseCredentialForm):
    consumer_key = forms.CharField(required=True)
    consumer_secret = forms.CharField(required=True)
    access_token = forms.CharField(required=True)
    access_token_secret = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(CredentialTwitterForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][1].extend(['consumer_key', 'consumer_secret', 'access_token', 'access_token_secret'])
        if self.instance and self.instance.token:
            token = json.loads(self.instance.token)
            self.fields['consumer_key'].initial = token.get('consumer_key')
            self.fields['consumer_secret'].initial = token.get('consumer_secret')
            self.fields['access_token'].initial = token.get('access_token')
            self.fields['access_token_secret'].initial = token.get('access_token_secret')

    def to_token(self):
        return {
            "consumer_key": self.cleaned_data["consumer_key"].strip(),
            "consumer_secret": self.cleaned_data["consumer_secret"].strip(),
            "access_token": self.cleaned_data["access_token"].strip(),
            "access_token_secret": self.cleaned_data["access_token_secret"].strip(),
        }

    def save(self, commit=True):
        m = super(CredentialTwitterForm, self).save(commit=False)
        m.platform = Credential.TWITTER
        m.token = json.dumps(self.to_token())
        m.save()
        return m


class CredentialTumblrForm(BaseCredentialForm):
    api_key = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(CredentialTumblrForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][1].extend(['api_key'])
        if self.instance and self.instance.token:
            token = json.loads(self.instance.token)
            self.fields['api_key'].initial = token.get('api_key')

    def to_token(self):
        return {
            "api_key": self.cleaned_data["api_key"].strip(),
        }

    def save(self, commit=True):
        m = super(CredentialTumblrForm, self).save(commit=False)
        m.platform = Credential.TUMBLR
        m.token = json.dumps(self.to_token())
        m.save()
        return m


class CredentialWeiboForm(BaseCredentialForm):
    access_token = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(CredentialWeiboForm, self).__init__(*args, **kwargs)
        self.helper.layout[0][1].extend(['access_token'])

        if self.instance and self.instance.token:
            token = json.loads(self.instance.token)
            self.fields['access_token'].initial = token.get('access_token')

    def to_token(self):
        return {
            "access_token": self.cleaned_data["access_token"].strip(),
        }

    def save(self, commit=True):
        m = super(CredentialWeiboForm, self).save(commit=False)
        m.platform = Credential.WEIBO
        m.token = json.dumps(self.to_token())
        m.save()
        return m


# sizes = forms.MultipleChoiceField(choices=SIZE_OPTIONS, initial=("Thumbnail", "Large", "Original"),
#                                   widget=forms.CheckboxSelectMultiple, label="Image sizes", )

class SeedChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.label()


class ExportForm(forms.ModelForm):
    seeds = SeedChoiceField(None, required=False, widget=forms.CheckboxSelectMultiple,
                            help_text="If no seeds are checked, all seeds will be exported.")

    class Meta:
        model = Export
        fields = ['seeds', 'export_format', 'export_segment_size', 'dedupe',
                  'item_date_start', 'item_date_end',
                  'harvest_date_start', 'harvest_date_end']
        localized_fields = None
        error_messages = {}
        widgets = {
            'item_date_start': DATETIME_WIDGET,
            'item_date_end': DATETIME_WIDGET,
            'harvest_date_start': DATETIME_WIDGET,
            'harvest_date_end': DATETIME_WIDGET,
        }
        labels = {
            'dedupe': "Deduplicate"
        }

    def __init__(self, *args, **kwargs):
        self.collection = Collection.objects.get(pk=kwargs.pop("collection"))
        super(ExportForm, self).__init__(*args, **kwargs)
        self.fields["seeds"].queryset = self.collection.seeds.all()
        cancel_url = reverse('collection_detail', args=[self.collection.pk])
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',
                'seeds',
                'export_format',
                'export_segment_size',
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
        if len(self.fields["seeds"].queryset) < 2:
            del self.fields["seeds"]
            self.helper.layout[0].pop(0)

    def save(self, commit=True):
        m = super(ExportForm, self).save(commit=False)
        # This may need to change.
        m.export_type = self.collection.harvest_type
        # If seeds is none
        if not self.cleaned_data.get("seeds"):
            m.collection = self.collection
        m.save()
        self.save_m2m()
        return m


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'email_frequency', 'harvest_notifications']
        widgets = {
            "username": forms.TextInput(attrs={'size': '40'}),
            "email": forms.TextInput(attrs={'size': '40'})
        }
        help_texts = {
            'harvest_notifications': "Receive an email when there is a problem with a harvest.",
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # set up crispy forms helper
        self.helper = FormHelper(self)
        # set up crispy forms helper
        self.helper.layout = Layout(
            Fieldset(
                '',
                'username',
                'email',
                'email_frequency',
                'harvest_notifications',
                Div()
            ),
            FormActions(
                Submit('submit', 'Save'),
                Button('cancel', 'Cancel', onclick="window.history.back()")
            )
        )
