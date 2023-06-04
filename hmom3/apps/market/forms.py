from django import forms

from .validators import validate_resource


class TradeForm(forms.Form):
    """Form for fill trade request."""
    from_resource = forms.CharField(
        widget=forms.HiddenInput,
        validators=(validate_resource,),
    )
    to_resource = forms.CharField(
        widget=forms.HiddenInput,
        validators=(validate_resource,),
    )
    value = forms.CharField(required=True)

    value.widget.attrs['class'] = 'market-text-input market-text-body'
    value.widget.attrs['style'] = "position: relative; left:20px; top:30px;"
    value.widget.attrs['onchange'] = "updateResult(this.value)"

    def clean(self):
        cleaned_data = super().clean()
        from_resource = cleaned_data.get('from_resource')
        to_resource = cleaned_data.get('to_resource')
        value = cleaned_data.get('value')
        if not value.isnumeric():
            raise forms.ValidationError('Значение должно быть указано числом.')
        if value == '0':
            raise forms.ValidationError('Укажите не нулевое значение.')
        if to_resource is None or from_resource is None:
            raise forms.ValidationError('Не указан ресурс.')
        if from_resource == to_resource:
            raise forms.ValidationError('Для обмена выберете разные ресурсы.')
        return cleaned_data
