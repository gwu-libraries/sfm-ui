from django.conf import settings as django_settings


def settings(request):
    # return the value you want as a dictionary. you may add multiple values.
    return {'SFM_UI_VERSION': django_settings.SFM_UI_VERSION, 'CONTACT_EMAIL': django_settings.CONTACT_EMAIL,
            'INSTITUTION_NAME': django_settings.INSTITUTION_NAME, 'INSTITUTION_LINK': django_settings.INSTITUTION_LINK,
            'COOKIE_CONSENT_HTML': django_settings.COOKIE_CONSENT_HTML,
            'COOKIE_CONSENT_BUTTON_TEXT': django_settings.COOKIE_CONSENT_BUTTON_TEXT,
            'ENABLE_COOKIE_CONSENT': django_settings.ENABLE_COOKIE_CONSENT,
            'ENABLE_GW_FOOTER': django_settings.ENABLE_GW_FOOTER}
