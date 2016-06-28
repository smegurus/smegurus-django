import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class PrivateImageUpload(models.Model):
    """
    An image upload file restricted to specific tenants only.

    https://schema.org/ImageObject
    """
    class Meta:
        app_label = 'api'
        db_table = 'den_private_image_uploads'
        verbose_name = 'Image Upload'
        verbose_name_plural = 'Image Uploads'

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    imagefile = models.ImageField(
        _("Image"),
        help_text=_('An image of the upload.'),
        upload_to='upload',
        null=True,
        blank=True
    )
    owner = models.ForeignKey(
        User,
        help_text=_('The user whom owns this object.'),
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.imagefile)

    def delete(self, *args, **kwargs):
        """
            Overrided delete functionality to include deleting the local file
            that we have stored on the system. Currently the deletion funciton
            is missing this functionality as it's our responsibility to handle
            the local files.
        """
        if self.imagefile:
            if os.path.isfile(self.imagefile.path):
                os.remove(self.imagefile.path)
        super(PrivateImageUpload, self).delete(*args, **kwargs) # Call the "real" delete() method
