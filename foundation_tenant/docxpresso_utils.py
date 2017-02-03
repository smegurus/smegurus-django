import os.path
import json
import urllib3  # Library used for sending POST/GET.
from passlib.hash import sha1_crypt # Library used for the SHA1 hash algorithm.
from datetime import datetime, timedelta  # Datetime.


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

    def add_array(self, key, array):
        """
        Add array per key for document construction.
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
                "name": self.name
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

    def __str__(self):
        """
        To-string function will return the data used for constructing the
        document.
        """
        return str(self.data)
