#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/documents/projet_flask/")

from projet_flask import app as application
application.secret_key = '7b31fdc6-85ff-4855-9e25-7dbbe134d746'