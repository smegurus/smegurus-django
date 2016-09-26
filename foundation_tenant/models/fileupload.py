import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from smegurus.settings import env_var

class TenantFileUploadManager(models.Manager):
    def delete_all(self):
        items = TenantFileUpload.objects.all()
        for item in items.all():
            item.delete()


class TenantFileUpload(models.Model):
    """A file uploaded object restricted to specific tenants only."""
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_tenant_file_uploads'
        verbose_name = 'File Upload'
        verbose_name_plural = 'File Uploads'

    objects = TenantFileUploadManager()
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
        return str(self.datafile)

    def get_s3_url(self): 
        return "https://" + env_var('AWS_STORAGE_BUCKET_NAME') + ".s3.amazonaws.com/media/"+str(self.datafile)

    # def delete(self, *args, **kwargs):
    #     """
    #         Overrided delete functionality to include deleting the local file
    #         that we have stored on the system. Currently the deletion funciton
    #         is missing this functionality as it's our responsibility to handle
    #         the local files.
    #     """
    #     if self.datafile:
    #         if os.path.isfile(self.datafile.path):
    #             os.remove(self.datafile.path)
    #     super(TenantFileUpload, self).delete(*args, **kwargs) # Call the "real" delete() method
