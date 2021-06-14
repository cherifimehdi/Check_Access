# Author : Mehdi CHERIFI

# Note : Please make sure to apply your <YOUR_SYSLOG_SERVER> and <YOUR_ROOM_ID> in the required emplacement

from genie.testbed import load
from prettytable import PrettyTable
import logging.handlers
from logging import Formatter
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("Token")
testbed=load('connex.yml')
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.INFO)

handler = logging.handlers.SysLogHandler(address = ('<YOUR_SYSLOG_SERVER>',514))
my_logger.addHandler(handler)

log_format = '[%(levelname)s] \"%(message)s\"'
handler.setFormatter(Formatter(fmt=log_format))

Table_Result = PrettyTable(["Device", "Status"])

Table_Result.padding_width = 1
Table_Result.title = 'Access Check'

# Try access to each device and generate logs to send to the Syslog server and to save the result as table

for device in testbed.devices:
   try:
      testbed.devices[device].connect(log_stdout=False)

      MSG = f'No Access Issue with {device} device'
      my_logger.info(MSG)
      Table_Result.add_row([str(device),"Access Ok"])

   except ConnectionError:

      MSG = f'Access Issue with {device} device!!!, please proceed for a solution'
      my_logger.info(MSG)
      Table_Result.add_row([str(device),"No Access"])


print(Table_Result)

# Send Table_Result as a text file to Webex Teams Space

with open('Result.txt', 'w') as w:
    w.write(str(Table_Result))

m = MultipartEncoder({'roomId': '<YOUR_ROOM_ID>',
                         'text': 'CHECK ACCESS RESULT  !!!',
                         'files': ('Result.txt', open('Result.txt', 'rb'),
                         'document/txt')})
r = requests.post('https://webexapis.com/v1/messages', data=m,
                     headers={'Authorization': 'Bearer '+token,
                    'Content-Type': m.content_type})