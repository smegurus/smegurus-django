import googlemaps
from datetime import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.postaladdress import PostalAddress
from smegurus.settings import env_var


class Command(BaseCommand):
    help = 'Command will fetch the longitude and latitude for the Tenant PostalAddress.'

    def add_arguments(self, parser):
        parser.add_argument('id', nargs='+')

    def handle(self, *args, **options):
        for postaladdress_id in options['id']:
            # Fetch the User account associated with this email.
            try:
                postal_address = PostalAddress.objects.get(id=int(postaladdress_id))
                self.begin_processing(postal_address)
            except Exception as e:
                pass

    def begin_processing(self, postal_address):
        # https://developers.google.com/maps/documentation/geocoding/start#reverse
        gmaps = googlemaps.Client(key=env_var('GOOGLE_MAPS_API_KEY'))

        # Geocoding an address
        geocode_result = gmaps.geocode(str(postal_address))
        for geo_data in geocode_result:
            # Extract the data.
            postal_address.longitude = geo_data['geometry']['location']['lng']
            postal_address.latitude = geo_data['geometry']['location']['lat']

        # Save the longitude and latitude.
        postal_address.save()
