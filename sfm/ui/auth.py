from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse

from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from django.core.exceptions import PermissionDenied

import logging

from .forms import CredentialTwitterForm, CredentialWeiboForm, CredentialTumblrForm
from .models import Credential, CollectionSet, Collection

log = logging.getLogger(__name__)


class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        # Automatically create a group for the user.
        user = DefaultAccountAdapter.save_user(self, request, user, form, commit=True)
        group = Group.objects.create(name=user.username)
        group.save()
        user.groups.add(group)
        user.save()
        return user


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        credential_name = u"{}'s {} credential".format(sociallogin.user.username or request.user.username,
                                                       sociallogin.token.app.name)
        if sociallogin.token.app.provider == 'twitter':
            form = CredentialTwitterForm({
                'name': credential_name,
                'platform': Credential.TWITTER,
                'consumer_key': sociallogin.token.app.client_id,
                'consumer_secret': sociallogin.token.app.secret,
                'access_token': sociallogin.token.token,
                'access_token_secret': sociallogin.token.token_secret,
            })
        elif sociallogin.token.app.provider == 'tumblr':
            form = CredentialTumblrForm({
                'name': credential_name,
                'platform': Credential.TUMBLR,
                'api_key': sociallogin.token.app.client_id,
            })
        elif sociallogin.token.app.provider == 'weibo':
            form = CredentialWeiboForm({
                'name': credential_name,
                'platform': Credential.WEIBO,
                'access_token': sociallogin.token.token,
            })
        else:
            assert False, "Unrecognized social login provider"
        form.instance.user = request.user
        try:
            credential = form.save()
        except (IntegrityError, ValueError):
            messages.warning(request, "Credential already exists.")
            raise ImmediateHttpResponse(HttpResponseRedirect(reverse('credential_list')))

        messages.info(request, "New credential created.")

        raise ImmediateHttpResponse(HttpResponseRedirect(reverse('credential_detail', args=(credential.pk,))))


def has_collection_set_based_permission(obj, user, allow_superuser=True, allow_staff=False,
                                        allow_collection_visibility=False):
    """
    Based on obj.get_collection_set(), checks if user is in the collection set's group.

    Based on obj.get_collection(), checks if collection has visibility=local

    Accounts for superusers and staff.
    """
    if hasattr(obj, "get_collection_set"):
        collection_set = obj.get_collection_set()
        # User is logged in
        if user.is_authenticated:
            # If staff or superuser or in group, then yes.
            if (allow_staff and user.is_staff) \
                    or (allow_superuser and user.is_superuser) \
                    or collection_set.group in user.groups.all():
                return True
    if allow_collection_visibility:
        if isinstance(obj, CollectionSet):
            for collection in obj.collections.all():
                if collection.visibility == Collection.LOCAL_VISIBILITY:
                    return True
        elif hasattr(obj, "get_collection"):
            collection = obj.get_collection()
            if collection.visibility == Collection.LOCAL_VISIBILITY:
                return True

    return False


def check_collection_set_based_permission(obj, user, allow_superuser=True, allow_staff=False,
                                          allow_collection_visibility=False):
    if not has_collection_set_based_permission(obj, user, allow_superuser=allow_superuser, allow_staff=allow_staff,
                                               allow_collection_visibility=allow_collection_visibility):
        log.warning("Permission denied for %s", user)
        raise PermissionDenied()


def has_user_based_permission(obj, user, allow_superuser=True, allow_staff=False):
    """
    Based on obj.get_user(), checks if provided user is that user.

    Accounts for superusers and staff.
    """

    if hasattr(obj, "get_user"):
        obj_user = obj.get_user()
        # User is logged in
        if user.is_authenticated:
            # If staff or superuser or share a common group, then yes.
            if (allow_staff and user.is_staff) \
                    or (allow_superuser and user.is_superuser) \
                    or obj_user == user:
                return True
    return False


def check_user_based_permission(obj, user, allow_superuser=True, allow_staff=False):
    if not has_user_based_permission(obj, user, allow_superuser=allow_superuser, allow_staff=allow_staff):
        log.warning("Permission denied for %s", user)
        raise PermissionDenied()


class CollectionSetOrSuperuserPermissionMixin(object):
    def get_object(self, queryset=None):
        """
        Overrides get_object from SingleObjectMixin to check model object.

        Model object must provide a get_collection_set method.
        """
        obj = super(CollectionSetOrSuperuserPermissionMixin, self.__class__).get_object(self, queryset)
        check_collection_set_based_permission(obj, self.request.user)
        return obj

    def get_form(self, form_class=None):
        """
        Overrides get_form (from FormMixin) to check when rendering or submitting a form.

        View must provide collection_set as initial data.
        """
        form = super(CollectionSetOrSuperuserPermissionMixin, self).get_form(form_class=form_class)
        if "collection_set" in form.initial and isinstance(form.initial["collection_set"], CollectionSet):
            check_collection_set_based_permission(form.initial["collection_set"], self.request.user)
        return form


class CollectionSetOrSuperuserOrStaffPermissionMixin(object):
    def get_object(self, queryset=None):
        """
        Overrides get_object from SingleObjectMixin to check model object.

        Model object must provide a get_collection_set method.
        """
        obj = super(CollectionSetOrSuperuserOrStaffPermissionMixin, self.__class__).get_object(self, queryset)
        check_collection_set_based_permission(obj, self.request.user, allow_staff=True)
        return obj

    def get_form(self, form_class=None):
        """
        Overrides get_form (from FormMixin) to check when rendering or submitting a form.

        View must provide collection_set as initial data.
        """
        form = super(CollectionSetOrSuperuserOrStaffPermissionMixin, self).get_form(form_class=form_class)
        if "collection_set" in form.initial:
            check_collection_set_based_permission(form.initial["collection_set"], self.request.user, allow_staff=True)
        return form


class CollectionSetOrCollectionVisibilityOrSuperuserOrStaffPermissionMixin(object):
    def get_object(self, queryset=None):
        """
        Overrides get_object from SingleObjectMixin to check model object.

        Model object must provide a get_collection_set and get_collection method.
        """
        obj = super(CollectionSetOrCollectionVisibilityOrSuperuserOrStaffPermissionMixin, self.__class__).get_object(
            self, queryset)
        check_collection_set_based_permission(obj, self.request.user, allow_staff=True,
                                              allow_collection_visibility=True)
        return obj

    def get_form(self, form_class=None):
        """
        Overrides get_form (from FormMixin) to check when rendering or submitting a form.

        View must provide collection_set as initial data.
        """
        form = super(CollectionSetOrCollectionVisibilityOrSuperuserOrStaffPermissionMixin, self).get_form(
            form_class=form_class)
        # if "collection_set" in form.initial:
        #     check_collection_set_based_permission(form.initial["collection_set"], self.request.user, allow_staff=True)
        if "collection" in form.initial:
            check_collection_set_based_permission(form.initial["collection_set"], self.request.user, allow_staff=True,
                                                  allow_collection_visibility=True)
        return form


class UserOrSuperuserPermissionMixin(object):
    def get_object(self, queryset=None):
        """
        Overrides get_object from SingleObjectMixin to check model object.

        Model object must provide a get_user method.
        """
        obj = super(UserOrSuperuserPermissionMixin, self.__class__).get_object(self, queryset)
        check_user_based_permission(obj, self.request.user)
        return obj


class UserOrSuperuserOrStaffPermissionMixin(object):
    def get_object(self, queryset=None):
        """
        Overrides get_object from SingleObjectMixin to check model object.

        Model object must provide a get_user method.
        """
        obj = super(UserOrSuperuserOrStaffPermissionMixin, self.__class__).get_object(self, queryset)
        check_user_based_permission(obj, self.request.user, allow_staff=True)
        return obj
