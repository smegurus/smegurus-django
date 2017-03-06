# -*- coding: utf-8 -*-
import os.path
import json
import urllib3  # Library used for sending POST/GET.
from passlib.hash import sha1_crypt # Library used for the SHA1 hash algorithm.
from datetime import datetime, timedelta  # Datetime.
from foundation_tenant.utils import humanize_number


class DocxspressoAPI:
    """
    The following class is responsible for communicating back and forth with
    Eduardo Ramos's propriatery "Docxpresso" document generation software.
    """

    name = "default"
    format = ".odt"
    response = "doc"
    data = []

    def __init__(self, public_key, private_key, url):
        """
        Function will create our API interface.
        """
        # assign unique public and private keys to this instance.
        self.public_key = public_key
        self.private_key = private_key
        self.url = url

    def new(self, name, format, template, response="doc"):
        """
        Function will setup a new document that will be constructed.
        """
        self.name = name
        self.format = format
        self.template = template
        self.response = response

    def get_filename(self):
        """
        Return's the filename of the constructed document.
        """
        return self.name + "." + self.format

    def add_text(self, key, value):
        """
        Add text value per key for document construction.
        """
        self.data.append({
            "vars": [{
                "var": key,
                "value": value
            }]
        })

    def add_number(self, key, value):
        """
        Add number value per key for document construction which will be humanized
        depending on the language of the user.
        """
        self.data.append({
            "vars": [{
                "var": key,
                "value": humanize_number(value)
            }]
        })

    def add_text_paragraphs(self, key, array):
        """
        Add html per key for document struction.

        Note:
        The content of 'value' parameter must look like this, for example:
        <p>My choice 1</p><p>My choice 3</p><p>My choice 4</p>
        """
        value = ""
        for text in array:
            value += "<p>" + text + "</p>"

        self.data.append({
            "vars": [{
                "var": key,
                "value": [value],
                 "html": 1,
                 "block-type": 1
            }]
        })

    def add_unordered_list(self, key, array): #BUG: DOES NOT WORK AS ADVERTISED.
        """
        Add array per key to generate unordered list of items.
        """
        self.data.append({
            "vars": [{
                "var": key,
                "value": array
            }],
            "options": {
                "element": "list"
            }
        })

    def generate(self):
        """
        Function will take the constructed document and submit it to
        Docxpresso to be generated. Once document has been generated
        this function will return binary data of the file.
        """
        # Generate timestamp.
        current = datetime.now()
        timestamp = str(current.strftime('%Y%m%d%H%M%S'))

        # Generate our API key.
        api_key = self.public_key + self.private_key + str(timestamp)
        api_key_hashed = sha1_crypt.hash(api_key) #  (Deprecated: https://passlib.readthedocs.io/en/stable/lib/passlib.hash.sha1_crypt.html)

        # Format our data.
        data = {
            "security": {
                "publicKey": self.public_key,
                "timestamp": timestamp,
                "APIKEY": api_key_hashed
            },
            "template": self.template,
            "output": {
                "format": self.format,
                "response": self.response,
                "name": self.name,
                "repairVariables": True
            },
            "replace": self.data
        }

        # We will convert our Python dictonary into a JSON diconary.
        encoded_body = json.dumps(data).encode('utf-8')

        # Send AJAX Post to Docxpresso server.
        http = urllib3.PoolManager()
        r = http.request(
            'POST',
            self.url,
            # body=encoded_body,
            fields={
                "dataJSON": encoded_body
            }
            # headers={'Content-Type': 'application/json'}
        )

        # Return the data of our POST response object.
        return r.data

    def add_custom(self, array):
        """
        Function used if you have an extremly complex API call to make that
        you need to run it manually and insert it.
        """
        self.data.append(array)

    def add_picture(self, key, value, pixel_width=175, pixel_height=175):
        """
        Add picture value per key for document construction.
        """
        self.data.append({
            "vars": [
                {
                    "var": key,
                    "value": [
                        value
                    ],
                    "width": str(pixel_width)+"px",
                    "height": str(pixel_height)+"px"
                }
            ],
            "options": {
                "element": "image"
            }
        })

    def add_text_to_footer(self, key, value):
        """
        Add text value per key for document construction into the footer.
        """
        self.data.append({
            "vars": [{
                "var": key,
                "value": value
            }],
            "options": {
                "target": "footer"
            }
        })

    def add_text_to_header(self, key, value):
        """
        Add text value per key for document construction into the header.
        """
        self.data.append({
            "vars": [{
                "var": key,
                "value": value
            }],
            "options": {
                "target": "header"
            }
        })

    def __str__(self):
        """
        To-string function will return the data used for constructing the
        document.
        """
        return str(self.data)
