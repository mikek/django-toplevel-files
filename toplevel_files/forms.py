from django.forms.models import ModelForm, ModelChoiceField
from django.utils.translation import ugettext as _

from .models import TopLevelFileType, TopLevelFile


class TopLevelFileAdminForm(ModelForm):
    type = ModelChoiceField(
        queryset=TopLevelFileType.objects.all(),
        help_text=_('Choose from one of the available types'))

    class Meta:
        model = TopLevelFile

    def __init__(self, *args, **kwargs):
        super(TopLevelFileAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['type'].required = False
            self.fields['type'].widget.attrs['disabled'] = 'disabled'
            self.fields['type'].help_text = _('Changing type is not allowed')
            return
        used_type_ids = TopLevelFile.objects.all().values_list(
            'type_id', flat=True)
        self.fields['type'].queryset = TopLevelFileType.objects.exclude(
            pk__in=used_type_ids)

    def clean_type(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            return self.instance.type_id
        else:
            return self.cleaned_data.get('type', None)
