import os
import boto
from boto.s3.key import Key
from boto.exception import S3CreateError
from boto.s3.connection import S3Connection
from django.conf import settings


class Singleton(type):
    """
    http://stackoverflow.com/a/6798042
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class PrivateS3Bucket(metaclass=Singleton):
    def __init__(self):
        self.s3 = S3Connection( # WORKS
            aws_access_key_id = settings.PRIVATE_AWS_ACCESS_KEY_ID,
            aws_secret_access_key = settings.PRIVATE_AWS_SECRET_ACCESS_KEY,
            host = settings.PRIVATE_AWS_S3_HOST,
            #is_secure=False, # uncomment if you are not using ssl calling_format = boto.s3.connection.OrdinaryCallingFormat(),
            calling_format = boto.s3.connection.OrdinaryCallingFormat()
        )

        self.bucket = self.s3.get_bucket(settings.PRIVATE_AWS_STORAGE_BUCKET_NAME, validate=False)
        self.bucket.set_acl('private') # Make the files restricted to us.

    def get_default_s3():
        return self.s3

    def get_default_bucket():
        return self.bucket

    def upload_file(self, file, key):
        upload_to_s3_bucket(self.bucket, file, key, encrypt_key=True)

    def delete_file(self, key):
        delete_from_s3_bucket(self.bucket, key)

    def get_limited_url(self, key, expire_time=60):
        return get_timed_s3_url(self.s3, self.bucket, key, expire_time)


def upload_to_s3_bucket(bucket, file, key, callback=None, md5=None, reduced_redundancy=False, content_type=None, encrypt_key=False):  #TODO: Unit Test.
    """
    Uploads the given file to the AWS S3
    bucket and key specified.

    callback is a function of the form:

    def callback(complete, total)

    The callback should accept two integer parameters,
    the first representing the number of bytes that
    have been successfully transmitted to S3 and the
    second representing the size of the to be transmitted
    object.

    Returns boolean indicating success/failure of upload.

    SOURCE: http://stackabuse.com/example-upload-a-file-to-aws-s3/
    """
    try:
        size = os.fstat(file.fileno()).st_size
    except:
        # Not all file objects implement fileno(),
        # so we fall back on this
        file.seek(0, os.SEEK_END)
        size = file.tell()

    # DEVELOPERS NOTE: ENCRYPTION
    # According to the details of the following Stackoverflow issue,
    # it appears that when you set the 'encrypt_key=True' parameter in the
    # 'set_contents_from_file' boto function, the S3 server will automatically
    # store the files in an encrypted mannor and decrypt the files when a User
    # fetches them from our generated URL:
    # - http://stackoverflow.com/a/14624505)

    k = Key(bucket)
    k.key = key
    if content_type:
        k.set_metadata('Content-Type', content_type)
    sent = k.set_contents_from_file(file, cb=callback, md5=md5, reduced_redundancy=reduced_redundancy, rewind=True, encrypt_key=encrypt_key)

    # Rewind for later use
    file.seek(0)

    if sent == size:
        return True
    return False


def get_timed_s3_url(s3, bucket, key, expire_time=60):
    """Utility function will get the URL of the resource."""
    # Generate a temporary 60 second url for the file. Once expires, the URL becomes PermissionDenied.
    return s3.generate_url(
        expire_time,
        'GET',
        bucket=bucket.name,
        key=key,
        force_http=True
    )


def delete_from_s3_bucket(bucket, search_key):
    """Utility function will delete the object based on the inputted key."""
    s3_object = bucket.get_key(search_key)
    if s3_object:
        s3_object.delete()
