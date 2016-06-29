from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.abstract_creativework import AbstractCreativeWork


class AbstractMediaObject(AbstractCreativeWork):
    """
    An image, video, or audio object embedded in a web page. Note that a
    creative work may have many media objects associated with it on the
    same web page. For example, a page about a single song (MusicRecording)
    may have a music video (VideoObject), and a high and low bandwidth
    audio stream (2 AudioObject's).

    https://schema.org/MediaObject
    """
    class Meta:
        abstract = True
