from django.db import models
from django.utils.translation import ugettext_lazy as _

from .storage import OverwriteFSStorage


class TopLevelFileType(models.Model):
    title = models.CharField(_('title'), max_length=128, unique=True)
    file_name = models.CharField(_('file name'), max_length=512, unique=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('top level file type')
        verbose_name_plural = _('top level file types')
        ordering = ['-id']


class TopLevelFile(models.Model):
    def file_path(instance=None, filename=None):
        return instance.type.file_name

    type = models.OneToOneField(TopLevelFileType, verbose_name=_('type'))
    file = models.FileField(
        _('file'), upload_to=file_path, storage=OverwriteFSStorage(),
        help_text=_('you can choose a file with arbitrary name')
    )
    mod_date = models.DateTimeField(_('modification date'), auto_now=True)

    class Meta:
        verbose_name = _('top level file')
        verbose_name_plural = _('top level files')
        ordering = ['-id']

    def __unicode__(self):
        return '{} {}'.format(self.type.title, self.mod_date)

    def delete(self, *args, **kwargs):
        """Delete the object then delete the file itself"""
        storage, path = self.file.storage, self.file.path
        super(TopLevelFile, self).delete(*args, **kwargs)
        storage.delete(path)
