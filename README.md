[![Build Status](https://travis-ci.org/ImaginaryLandscape/django-nocaptcha-recaptcha.svg?branch=master)](https://travis-ci.org/ImaginaryLandscape/django-nocaptcha-recaptcha)

# Django google reCaptcha v2

Add new-style Google ReCaptcha widgets to your Django forms simply by adding a 
NoReCaptchaField field to said forms. 

### About

In late 2014, Google updated their ReCaptcha service, changing its API.  The update significantly
changes the appearance and function of ReCaptcha.  This has been referred to as
ReCaptcha 2 or "nocaptcha recaptcha".

This module is intended to be a successor to django-recaptcha to support the new style
Google Recaptcha.  It borrows a lot of the logic from the django-recaptcha, but has been
updated to support the Google change.

For the Google documentation for this service, visit the following:

    https://developers.google.com/recaptcha/intro

The original django-recaptcha project is located at the following location:

    https://github.com/praekelt/django-recaptcha

## Features

 - Implements Google's New "NoCaptcha ReCaptcha Field"
 - Uses the fallback option for browsers without JavaScript
 - Easy to add to a Form via a FormField
 - Works similar to django-recaptcha
 - Working demo projects
 - Works with Python 2.7 and 3.4


## Requirements
- Django from 1.5 to 1.11
- Python 2.7

## Installation and basic usage
1. Install package

	`` pip install git+git://github.com/oldroute/django-nocaptcha-recaptcha.git``

2. [Register](https://www.google.com/recaptcha/) google reCaptcha (v2 check box) and copy site and sectet keys
3. Configure your setting file:

	```python
    INSTALLED_APPS += ['nocaptcha_recaptcha']
	NORECAPTCHA_SITE_KEY = the Google provided site_key
    NORECAPTCHA_SECRET_KEY = the Google provided secret_key
	```
4. Import field and connect to your form:

	```python
    from django import forms
    from nocaptcha_recaptcha.fields import NoReCaptchaField
	...

    class MyForm(forms.Form):
    	... # other fields
        captcha = NoReCaptchaField()
	```

    You can customize the field. You can add attributes to the g-recaptcha div tag through the following:

     ``captcha = NoReCaptchaField(gtag_attrs={'data-theme':'dark'}))``

5. Add following js to your ``main.js`` file

	```javascript
    // dictionary must contain all capthcas ids with value 'false'
	var captchas = {
        'id-my-form-captcha': false, # css id form field
    }
	// callback for google script, when running - all captchas will be rendered
	var captchaReady = function(){
        for (key in captchas){
            var el = document.getElementById(key);
            if( el ){
                grecaptcha.render(el, {'sitekey': el.getAttribute('data-sitekey') });
                captchas[key] = true;
            }
        }
	}
	// callback fired when form updated (ajax case) and rerender all captchas
    var captchaWidgetLoaded = fucntion() {
        let captcha = document.querySelectorAll('.g-recaptcha')

        $('.g-recaptcha').each(function(){
            var captcha_id = $(this).attr('id');
            if(captchas[captcha_id] === true){
                var el = document.getElementById(captcha_id);
                try {
                    grecaptcha.render(el, { 'sitekey': el.getAttribute('data-sitekey'), 'theme': 'dark' });
                } catch (err){ }
            } else {
                captchas[captcha_id] = false;
            }
        })
    }
	```

6. Insert google script in your base template footer:
	```html
   <script src="/static/js/main.js"></script>
   <script src="//www.google.com/recaptcha/api.js?onload=captchaReady&render=explicit&hl=ru" async defer></script>

	```

## Demo project

The demo project includes a fully working example of this module.
To use it, run the following:

    cd demo
    export NORECAPTCHA_SITE_KEY="<your site key>"
    export NORECAPTCHA_SECRET_KEY="<your secret key>"
    ./manage.py runserver

    # in a browser, visit http://localhost:8000

## Testing

    python setup.py test
