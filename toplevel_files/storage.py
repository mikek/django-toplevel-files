from django.core.files.storage import FileSystemStorage


class OverwriteFSStorage(FileSystemStorage):
    """FS storage subclass that always overwrites existing target file"""

    def get_available_name(self, name):
        """Ensures checked filename is always available"""
        return name

    def _save(self, name, content):
        """Overwrites old file if it was present with a new one"""
        if self.exists(name):
            self.delete(name)
        return super(OverwriteFSStorage, self)._save(name, content)
