from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from registration.forms import RegistrationForm

from sitemap import sitemaps

admin.autodiscover()

def callback(request, *args, **kwargs):
    return {'user': request.user}

urlpatterns = patterns('',
    url(r'^', include('main.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^ajax-validation/validate/authentication-form/$',
        'ajax_validation.views.validate',
        {'form_class': AuthenticationForm},
        name='ajax_validation-validate_authentication_form'),
    url(r'^ajax-validation/validate/password-change-form/$',
        'ajax_validation.views.validate',
        {'form_class': PasswordChangeForm, 'callback': callback},
        name='ajax_validation-validate_password_change_form'),
    url(r'^ajax-validation/validate/password-reset-form/$',
        'ajax_validation.views.validate',
        {'form_class': PasswordResetForm},
        name='ajax_validation-validate_password_reset_form'),
    url(r'^ajax-validation/validate/registration-form/$',
        'ajax_validation.views.validate',
        {'form_class': RegistrationForm},
        name='ajax_validation-validate_registration_form'),
    url(r'^ajax-validation/validate/set-password-form/$',
        'ajax_validation.views.validate',
        {'form_class': SetPasswordForm, 'callback': callback},
        name='ajax_validation-validate_set_password_form'),
)