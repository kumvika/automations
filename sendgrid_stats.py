#
# Author: Vikash
#
# Script to get daily sendgrid stats like:
#   - How many requests came?
#   - How many of them got delivered?
#   - How many of them got bounced?
#   - How many of them got reported as spam?

import os
import sys
import json
import logging
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

# TODO Use argparse instead of checking command line argument
if len(sys.argv) != 3:
	print("\nPlease pass correct arguments:\n")
	print("Usage: python sendgrid_stats.py [from_date] [to_date]")
	print("Example: sendgrid_stats.py 2021-01-31 2021-02-02\n")
	sys.exit()

from_date = sys.argv[1]
to_date = sys.argv[2]

URL = "https://api.sendgrid.com/v3/stats?aggregated_by=day&start_date={}&end_date={}".format(from_date, to_date)
API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXX"

payload = "{}"
headers = {
    'Authorization': API_KEY
}

print("===================================================")
print("SENDGRID STATS : From Date {} To {}: ".format(from_date, to_date))

response = requests.request("GET", URL, data=payload, headers=headers)
json_op = eval(json.dumps(response.content))
stats = json.loads(json_op)

for i in range(len(stats)):
    print("===================================================")
    print("Going to show the stats of date {}: ".format(stats[i]['date']))
    print("===================================================")
    sendgrid_stats = stats[i]['stats'][0]['metrics']
    for key, val in sendgrid_stats.items():
        if (key == "requests" or key == "delivered" or key == "bounces" or key == "spam_reports"):
            print("{} = {}".format(str(key).ljust(14), val)
