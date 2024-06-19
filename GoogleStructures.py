import csv
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client import client, file, tools
from apiclient import discovery
from httplib2 import Http

from util import get_sheet_values, to_csv_safe, InvalidUsageError



FORM_ID : str = "1p28w1cHyYXombVt7XbInwGcYa-y5OMNSbFWzQMncups"
SPREADSHEET_ID : str = "19V-HINY0_b8xAgFiTxdlq-LyoM0HGd_G1HuMOj-Zf10"


class SubmissionTable:
    def __init__(self, questions: list['GoogleFormsQuestion']):
        self.header = [
            'responseId',
            'createTime',
            'lastSubmittedTime'
        ]
        self.default_name_col: int = 4
        for question in questions:
            self.header.append(to_csv_safe(question.text))
        self._questions = questions
        self._id_to_q = {q.id: q.text for q in questions}
        self.submissions: dict[str, list] = {}
        self._name_lookup: dict[str, tuple[str, str]] = {} # dict[name, tuple[email, phone number]]

    def responses_by_header(self, question: str) -> list[tuple[str, str]]:
        wh_index = self.header.index(question)
        output: list[tuple[str, str]] = []
        for subID, submission in self.submissions.items():
            output.append((subID, submission[wh_index]))
        return output

    def get_questions(self) -> list[str]:
        return self.header[3:]

    def user_lookup(self, responseId: str) -> str:
        candidate = self._find_name_index()
        if candidate == -1:
            return self.submissions[responseId][self.default_name_col]
        return self.submissions[responseId][candidate]
    
    def _find_name_index(self) -> int:
        for i, question in enumerate(self.get_questions()):
            if question.lower() in ['name', 'enter your name', 'first name', 'last name']:
                return i + 3
        return -1

    def add_submission(self, submission):
        temp: list = [submission['responseId'], submission['createTime'], submission['lastSubmittedTime']] + ([''] * (len(self.header) - 3))
        for question_id, answer in submission['answers'].items():
            question_text: str = to_csv_safe(self._id_to_q[question_id])
            if question_text not in self.header:
                raise Exception(f'Could not find Question({question_text}) in table({self.header})')
            temp[self.header.index(question_text)] = answer['textAnswers']['answers'][0]['value'].replace('“', '"').replace('”', '"').replace('’', "'")
        self.submissions[submission['responseId']] = temp
        self._name_lookup[temp[3]] = (temp[4], temp[5])
        
    def get_email_and_phone(self, name) -> tuple[str, str]:
        if name not in self._name_lookup.keys():
            print(f'Could not find "{name}" in keys')
            for key, value in self._name_lookup.items():
                print(f'  "{key}": "{value}"')
            return tuple('unknown email', 'unknown phone number')
        return self._name_lookup[name]

    def to_csv(self, path, display_outcome: bool = True) -> bool:
        try_again: bool = True
        while try_again:
            try:
                with open(path, 'w') as csv:
                    csv.write(','.join(self.header))
                    for submission in self.submissions.values():
                        csv.write('\n')
                        s = (','.join(submission)).replace('\n', ' ')
                        csv.write(s)
                if display_outcome: print(f'> Updated "{path}" successfully')
                return True
            except PermissionError as e:
                print(f"Encountered permission error while triing to write to '{path}'.")
                print("Some process may be using this file... please close the process before trying again.")
                if input("  > try again? (y/n) ") not in ['y', 'yes', 'ye', 'yeah']:
                    try_again = False
        if display_outcome: print(f'> Failed to update "{path}"!')
        return False



class GooglePageBreakException(Exception):
    pass



class GoogleFormsQuestion:
    def __init__(self, question_json):
        if 'pageBreakItem' in question_json:
            raise GooglePageBreakException
        try:
            self.id = question_json['questionItem']['question']['questionId']
            self.text = question_json['title']
            self.itemID = question_json['itemId']
        except Exception as e:
            print(f'{question_json=}')
            raise e
        


class GoogleLoginManager:

    def __init__(self):
        self.credentials = None

    def has_expired(self) -> bool:
        return not self.credentials

    def update_login(self, new_credentials) -> None:
        self.credentials = new_credentials

    def get_login(self):
        return self.credentials
    
    def form_login(self):
        SCOPES = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/forms.responses.readonly",
            "https://www.googleapis.com/auth/forms.body.readonly"
        ]

        store = file.Storage("token.json")
        creds = None
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
            os.system(f'start {flow.auth_uri}')
            creds = tools.run_flow(flow, store)
        return creds

    def sheets_login(self):
        SCOPES = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/forms.responses.readonly",
            "https://www.googleapis.com/auth/forms.body.readonly"
        ]
        response: str = 'Access Granted'
        if os.path.exists("token.json"):
            self.credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
            response = 'Access Granted: using cashed credentials from previous login'
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
                print('refreshed')
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES)
                self.credentials = flow.run_local_server(port=8080)
                response: str = 'Logged in Successfully - Access Granted'
        with open("token.json", "w") as token:
            token.write(self.credentials.to_json())
        return self.credentials
    


class GoogleUtils:
    @staticmethod
    def bulk_csv_to_google_sheets(spreadsheet_id: str, csv_calls: list[tuple[str, str]]):
        for csv_filename, google_sheet_name in csv_calls:
            GoogleUtils.csv_to_google_sheets(csv_filename, google_sheet_name, spreadsheet_id)

    @staticmethod
    def csv_to_google_sheets(csv_filename: str, google_sheet_name: str, spreadsheet_id):
        SHEET_NAME = google_sheet_name
        CSV_FILE = csv_filename

        """Converts a CSV file to a Google Sheet."""
        creds = GoogleCredentialManager.sheets_login()
        try:
            service = build("sheets", "v4", credentials=creds)
            sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            sheets = sheet_metadata.get('sheets', '')
            sheet_id = None
            for sheet in sheets:
                name, id = get_sheet_values(sheet)
                if name == SHEET_NAME:
                    sheet_id = id
                    break
            trying: bool = True
            while trying:
                try:
                    with open(CSV_FILE, 'r') as file:
                        csv_data = file.read()
                    trying = False
                    break
                except FileNotFoundError as FNFE:
                    print(f'Could not find "{CSV_FILE}"')
                    CSV_FILE = input('Which file should be used instead (enter file or "quit"): ')
                    if CSV_FILE == 'quit':
                        exit()
            body = {
                "requests": [
                {
                    "updateCells": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 0,
                        "startColumnIndex": 0
                    },
                    "rows": [
                        {
                        "values": [
                            {
                            "userEnteredValue": {
                                "stringValue": value.replace('<INSERT_COMMA>', ',')
                            }
                            } for value in row.split(",")
                        ]
                        }  for row in csv_data.split("\n")
                    ],
                    "fields": "userEnteredValue.stringValue"
                    }
                }
                ]
            }
            result = service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id, 
                body=body
            ).execute()
        except HttpError as err:
            print(err)

    @staticmethod
    def get_form_questions_and_submissions(
        form_id: str, 
        discovery_doc = "https://forms.googleapis.com/$discovery/rest?version=v1"
    ) -> tuple[any, any]:
        
        creds = GoogleCredentialManager.form_login()
        form_service = discovery.build(
            "forms",
            "v1",
            http=creds.authorize(Http()),
            discoveryServiceUrl=discovery_doc
        )

        form_info = form_service.forms().get(formId=form_id).execute()
        questions = form_info.get('items', [])
        
        response = form_service.forms().responses().list(formId=form_id).execute()
        submissions = response.get("responses", [])

        return (questions, submissions)

    @staticmethod
    def get_GFQ_list(raw_questions) -> list[GoogleFormsQuestion]:
        q: list[GoogleFormsQuestion] = []
        for raw_question in raw_questions:
            try:
                q.append(GoogleFormsQuestion(raw_question))
            except GooglePageBreakException as gpbe:
                continue
        return q



GoogleCredentialManager: GoogleLoginManager = GoogleLoginManager()



if __name__ == "__main__":
    raise InvalidUsageError("This file should not be run. Only import this file and its contents. Do not run this file directly.")
