from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .forms import CredentialTwitterForm
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
        credential_name = "{}'s {} credential".format(request.user.username, sociallogin.token.app.name)
        if sociallogin.token.app.provider == 'twitter':
            form = CredentialTwitterForm({
                'name': credential_name,
                'platform': Credential.TWITTER,
                'consumer_key': sociallogin.token.app.client_id,
                'consumer_secret': sociallogin.token.app.secret,
                'access_token': sociallogin.token.token,
                'access_token_secret': sociallogin.token.token_secret,
            })
        else:
            assert False, "Unrecognized social login provider"
        form.instance.user = request.user
        credential = form.save()

        raise ImmediateHttpResponse(HttpResponseRedirect(reverse('credential_detail', args=(credential.pk,))))
