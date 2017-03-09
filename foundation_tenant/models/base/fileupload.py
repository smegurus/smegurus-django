import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from smegurus.settings import env_var

class FileUploadManager(models.Manager):
    def delete_all(self):
        items = FileUpload.objects.all()
        for item in items.all():
            item.delete()


class FileUpload(models.Model):
    """A file uploaded object restricted to specific tenants only."""
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'smeg_file_uploads'
        verbose_name = _('File Upload')
        verbose_name_plural = _('File Uploads')

    objects = FileUploadManager()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    datafile = models.FileField(
        _("File"),
        help_text=_('An file of the upload.'),
        upload_to='upload',
        null=True,
        blank=True
    )
    owner = models.ForeignKey(
        User,
        help_text=_('The user whom owns this object.'),
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        temp_filename = str(self.datafile)
        return temp_filename.replace("upload/", "")

    def get_s3_url(self):
        return "https://" + env_var('AWS_STORAGE_BUCKET_NAME') + ".s3.amazonaws.com/media/"+str(self.datafile)

    def delete(self, *args, **kwargs):
        """
            Overrided delete functionality to include deleting the S3 file
            that we have stored in the cloud.
        """
        # If a file was uploaded to the cloud, then we need to remove it.
        if self.datafile:
            from django.core.files.storage import default_storage
            from django.core.files.base import ContentFile

            if default_storage.exists(str(self.datafile)):
                default_storage.delete(str(self.datafile))

        super(FileUpload, self).delete(*args, **kwargs) # Call the "real" delete() method
