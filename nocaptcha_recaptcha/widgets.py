from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.utils.translation import get_language
from django.conf import settings
from django import forms
from . import client


def displayhtml(site_key, gtag_attrs, js_params, name):
    """Gets the HTML to display for reCAPTCHA

    site_key -- The public api key provided by Google ReCaptcha
    """

    if 'hl' not in js_params:
        js_params['hl'] = get_language()[:2]

    return render_to_string(
        client.WIDGET_TEMPLATE,
        {
            'fallback_url': client.FALLBACK_URL,
            'site_key': site_key,
            'js_params': js_params,
            'gtag_attrs': gtag_attrs,
            'name': name
        })


class NoReCaptchaWidget(forms.widgets.Widget):
    g_nocaptcha_response = 'g-recaptcha-response'

    def __init__(self, site_key=None,
                 gtag_attrs={}, js_params={}, *args, **kwargs):
        self.site_key = site_key if site_key else \
            settings.NORECAPTCHA_SITE_KEY
        super(NoReCaptchaWidget, self).__init__(*args, **kwargs)
        self.gtag_attrs = gtag_attrs
        self.js_params = js_params

    def render(self, name, value, gtag_attrs=None, **kwargs):
        return mark_safe(u'%s' % displayhtml(self.site_key, self.gtag_attrs, self.js_params, name))

    def value_from_datadict(self, data, files, name):
        return data.get(self.g_nocaptcha_response, None)
