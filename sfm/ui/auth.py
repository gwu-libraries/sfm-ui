from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db import IntegrityError

from .forms import CredentialTwitterForm, CredentialWeiboForm, CredentialTumblrForm
from .models import Credential


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
        except IntegrityError:
            messages.warning(request, "Credential already exists.")
            raise ImmediateHttpResponse(HttpResponseRedirect(reverse('credential_list')))

        messages.info(request, "New credential created.")

        raise ImmediateHttpResponse(HttpResponseRedirect(reverse('credential_detail', args=(credential.pk,))))
