from django import forms
from django.contrib.auth.models import Group
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


class AddSeedsetButtonForm(forms.Form):

    collection = forms.ModelChoiceField(queryset=Collection.objects.all(), widget=forms.HiddenInput)


class SeedSetForm(forms.ModelForm):

    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)
 
    class Meta:
        model = SeedSet
        fields = '__all__'
        exclude = []
        widgets = {'collection': forms.HiddenInput}
        localized_fields = None
        labels = {}
        help_texts = {}
        error_messages = {}

    def __init__(self, *args, **kwargs):
        coll = kwargs.pop('coll')
        super(SeedSetForm, self).__init__(*args, **kwargs)
        self.fields['collection'].initial = coll

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
