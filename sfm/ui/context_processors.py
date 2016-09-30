from django.conf import settings as django_settings


def settings(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'SFM_UI_VERSION': django_settings.SFM_UI_VERSION}