import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.utils import generate_hash
from foundation_tenant.utils import int_or_none
from foundation_tenant.utils import django_sign
from foundation_tenant.utils import django_unsign
from foundation_tenant.s3utils import PrivateS3Bucket


URL_EXPIRY_TIME_IN_SECONDS = 60


private_s3 = PrivateS3Bucket() # Connect to our private s3 server and keep a
                               # singleton object loaded in memory.


class S3FileManager(models.Manager):
    def delete_all(self):
        """Utility function will delete all the S3 files in our system."""
        items = S3File.objects.all()
        for item in items.all():
            item.delete()

    def get_by_pk_or_none(self, pk):
        """
        Helper function which gets the S3File object by PK parameter or
        returns None result.
        """
        try:
            return S3File.objects.get(pk=pk)
        except S3File.DoesNotExist:
            return None

    def get_by_verifying_pk(self, signed_pk):
        """
        Utility function will attempt to lookup our S3File object based on
        whether the PK was verified to be authenticate and the PK matches
        an object in our record.
        """
        pk_string = django_unsign(signed_pk)
        pk = int_or_none(pk_string)
        try:
            return self.get(pk=pk)
        except S3File.DoesNotExist:
            return None


class S3File(models.Model):
    """
    A uploaded file saved as a S3 object inside a remote S3 server.
    """
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'smeg_s3_files'
        verbose_name = _('S3 File')
        verbose_name_plural = _('S3 Files')

    objects = S3FileManager()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    stem = models.CharField(
        _("Stem"),
        max_length=63,
        help_text=_('The name of the file without the file extension.'),
    )
    suffix = models.CharField(
        _("Suffix"),
        max_length=7,
        help_text=_('The extension of the file. Ex: png, jpg, etc'),
    )
    key = models.CharField(
        _("S3 Key"),
        max_length=127,
        help_text=_('The unique file identifier of our remote object in the S3 server.'),
        db_index=True,
        default=generate_hash,
        unique=True,
    )
    owner = models.ForeignKey(
        User,
        help_text=_('The user whom owns this object.'),
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        """
        Return the S3 filename as the object string.
        """
        return str(self.key)

    def signed_pk(self):
        """
        Function will return the object PK, signed with Django's SECRET_KEY,
        so the PK will be unreadable by regular Users, thus protecting it.
        """
        return django_sign(str(self.id))

    def verify_pk(self, signed_id):
        """
        Utility function will read the signed PK, get Django to verify the
        signature using SECRET_KEY, and return the plaintext PK value.
        """
        pk_string = django_unsign(signed_id)
        return int_or_none(pk_string)

    def get_absolute_url(self):
        """
        Generates a unique time-limited URL to access this file.
        """
        # Return our timed URL.
        return private_s3.get_limited_url(self.key, URL_EXPIRY_TIME_IN_SECONDS)

    def delete(self, *args, **kwargs):
        """
        Overrided delete functionality to include sending a "delete" command
        to the S3 server for our file before deleting this S3File object
        from the database.
        """
        if self.key:
            private_s3.delete_file(self.key) # Delete from S3 server.
        super(S3File, self).delete(*args, **kwargs) # Call the "real" delete() method

    def upload_file(self, bin_data):
        """
        Function takes the FILE from the request and uploades it to S3 and
        keeps a reference. Returns True or False depending on whether the
        upload was successful.
        """
        from django.core.files.base import ContentFile

        # Upload our file to S3 server.
        return private_s3.upload_file(
            ContentFile(bin_data),
            self.key
        )

    def get_filename(self):
        """
        Function returns the stem & suffix concatinated to form a filename.
        """
        return self.stem + self.suffix
