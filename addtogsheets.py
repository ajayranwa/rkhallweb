import gspread
from oauth2client.service_account import ServiceAccountCredentials


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('clever-muse-274319-ab6206394c2d.json', scope)
client = gspread.authorize(creds)

sheet = client.open("Alumni Registration Form")

def addtoregistration_sheet(List):
	worksheet = sheet.worksheet("Registration Responses")

	row_no = worksheet.cell(1, 2).value

	int_row = int(row_no)

	index = int_row+3
	worksheet.insert_row(List, index)

def addtopledge_sheet(List):
	worksheet = sheet.worksheet("Pledge Form Responses")

	row_no = worksheet.cell(1, 2).value

	int_row = int(row_no)

	index = int_row+3
	worksheet.insert_row(List, index)