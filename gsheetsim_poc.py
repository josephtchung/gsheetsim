# Proof of concept script for using a Google Spreadsheet as a numeric simulator
# Takes a Spreadsheet with a simple table of named inputs and outputs. Clones
# the spreadsheet, fills in the inputs by keyword and reads off the outputs
#
# Adapted from: https://developers.google.com/apps-script/guides/rest/quickstart/python

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

from apiclient import errors

import argparse




# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/script-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
CREDENTIAL_FILE = 'credentials.json'
APPLICATION_NAME = 'Google Spreadsheet Simulator POC'

# SCRIPT_ID is the google identifier for the Apps Script that is being invoked by this
# command line script which does all the work!
SCRIPT_ID = 'Mslj1R0jEFcqwdwH8z3bYVr0UMNckJP8z'
# BASE_SPREADSHEET_ID is the google identifier for the base spreadsheet that will be
# cloned and then operated on
BASE_SPREADSHEET_ID = '1w-chXNWK2GBaiSo7MCYv2-5YjDf1prb_Wa4zNlDQqs0'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

    credential_path = CREDENTIAL_FILE
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Apps Script Execution API.

    Creates a Apps Script Execution API service object and uses it to call an
    Apps Script function to print out a list of folders in the user's root
    directory.
    """

    # Authorize and create a service object.
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('script', 'v1', http=http)

    # Create an execution request object.
    request = {"function": "sheetTest", 
               "parameters": [BASE_SPREADSHEET_ID, 
                              {"mortgage": 150000, "interest_percent": 4.2, "length_years": 30}
                              ] }

    try:
        # Make the API request.
        response = service.scripts().run(body=request,
                scriptId=SCRIPT_ID).execute()

        if 'error' in response:
            # The API executed, but the script returned an error.

            # Extract the first (and only) set of error details. The values of
            # this object are the script's 'errorMessage' and 'errorType', and
            # an list of stack trace elements.
            error = response['error']['details'][0]
            print("Script error message: {0}".format(error['errorMessage']))

            if 'scriptStackTraceElements' in error:
                # There may not be a stacktrace if the script didn't start
                # executing.
                print("Script error stacktrace:")
                for trace in error['scriptStackTraceElements']:
                    print("\t{0}: {1}".format(trace['function'],
                        trace['lineNumber']))
        else:
            # The structure of the result will depend upon what the Apps Script
            # function returns. Here, the function returns an Apps Script Object
            # with String keys and values, and so the result is treated as a
            # Python dictionary.
            result = response['response'].get('result', {})
            if not result:
                print('Nothing returned!')
            else:
                for (item, value) in result.iteritems():
                    print("\t{0}: {1}".format(item, value))

    except errors.HttpError as e:
        # The API encountered a problem before the script started executing.
        print(e.content)

if __name__ == '__main__':
    main()
