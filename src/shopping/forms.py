from django import forms
from django.forms.util import flatatt
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

class NoNameTextInput(forms.TextInput):
    # Implementation depends on Django version
    # For example, this is for 1.4.1.
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        # Don't pass in the 'name' variable.
        final_attrs = self.build_attrs(attrs, type=self.input_type)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(self._format_value(value))
        return mark_safe(u'<input%s />' % flatatt(final_attrs))

class NoNameCharField(forms.CharField):
    widget = NoNameTextInput

class CheckoutForm(forms.Form):
    name = NoNameCharField(label='Cardholder name', required=False)
    address_line1 = NoNameCharField(label='Billing address line 1', required=False)
    address_line2 = NoNameCharField(label='Billing address line 2', required=False)
    address_state = NoNameCharField(label='Billing address state', required=False)
    address_zip = NoNameCharField(label='Billing zip', required=False)
    address_country = NoNameCharField(label='Billing address country', required=False)
    number = NoNameCharField(label='Card number', required=False)
    exp_month = NoNameCharField(label='Card expiration month', required=False)
    exp_year = NoNameCharField(label='Card expiration year', required=False)
    cvc = NoNameCharField(label='Card security code', required=False)
    stripe_token = forms.CharField(widget=forms.HiddenInput)