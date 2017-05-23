#!/usr/bin/python
# -*- coding: utf-8 -*-

"""View a message using it’s Mailgun storage key."""
import os
import sys

import requests

if len(sys.argv) != 4:
    print "Usage: retrieve.py api_key domain message_id"
    sys.exit(1)

# keep it in secret!
api_key = sys.argv[1]

# output file name 
file_name = "message.eml"

# let's make the url for retrieval
domain = sys.argv[2]
key = sys.argv[3]
url = "https://sw.api.mailgun.net/v3/domains/%s/messages/%s"
url = url % (domain, key)

# this will help us to get the raw MIME
headers = {"Accept": "message/rfc2822"}

# let's make a request to the API
r = requests.get(url, auth=("api", api_key), headers=headers)

if r.status_code == 200:
    # dump the body to a file
    with open(file_name, "w") as message:
        message.write(r.json()["body-mime"])
    # open it in the bird
    if sys.platform == "linux":
      os.system("thunderbird -file %s" % file_name)
    # open it in the apple mail
    if sys.platform == "darwin":
      os.system("open -a 'Mail' %s" % file_name)
else:
    print "Oops! Something went wrong: %s - Check your api_key domain or message_id" % r.content
