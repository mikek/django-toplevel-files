from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import TopLevelFile, TopLevelFileType
from .forms import TopLevelFileAdminForm


class TopLevelFileAdmin(admin.ModelAdmin):
    list_display = ('type', 'mod_date')
    form = TopLevelFileAdminForm
    # disable actions to avoid skipping our custom .delete()
    actions = None


class TopLevelFileTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'file_name')
    actions = None


admin.site.register(TopLevelFile, TopLevelFileAdmin)
admin.site.register(TopLevelFileType, TopLevelFileTypeAdmin)
