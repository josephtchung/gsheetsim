# gsheetsim

## What the?
This is a super simple proof of concept test of using a Google spreadsheet as a sort of back-end calculator/simulator via the Google Apps Script Execution REST API.

It has a 3 components:

1. Spreadsheet Simulator POC.xlsx

   This is an excel download of the base GApps Sheet. Import this into Google Drive and note the ID for the sheet. (Note as of this moment I haven't actually tried re-uploading the file, but it should work right?
   
2. gsheetsim_gapp_script.js

   This is the Google Apps Script that drives the spreadsheet. It performs the following steps:
   - Clone base spreadsheet (in our case Spreadsheet Simulator POC) which should have a sheet named "inputs" and a sheet named "outputs" plus additional sheets that actually do the work linking inputs to outputs 
   - Match the passed input key-value pairs to the inputs sheet, filling in the passed values
   - Read off the outputs and return them as key-value pairs
   
   To run this script you have to enable the script through the Google Apps Script Execution API. Read through this: https://developers.google.com/apps-script/guides/rest/ and specifically the Python Quickstart: https://developers.google.com/apps-script/guides/rest/quickstart/python

   The Javascript function you should enable is "SheetTest". The function "SheetTestTest" is there so you can test the script by itself without running through the whole REST API (see below).

3. gsheetsim_poc.py

   This is the Python counterpart which is run from the command line anywhere on the internet (once the GApps execution API is set up). To use, you have to first save the Client Secret from setting up the GApps Execution API in a file called "client_secret.json". Again, refer to https://developers.google.com/apps-script/guides/rest/quickstart/python
   
   Note that you have to edit gsheetsim_poc.py to change the SCRIPT_ID and BASE_SPREADSHEET_ID constants to reflect the ID of the enabled script and the correct ID of the uploaded spreadsheet respectively.

And if all is configured correctly, running gsheetsim_poc.py should fire up the script and read back the results. The first time it runs, it will take you through the OAUTH process requiring a web page sign in to create an auth token. Google documents methods for avoiding the user interaction for server-server use cases: https://developers.google.com/identity/protocols/OAuth2
