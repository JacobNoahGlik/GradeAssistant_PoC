import os
import sys
from securepassing import SecureData
from util import get_pass, selection



def get_token() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    return get_pass("Enter your token: ")


def update_token():
    token = get_token()
    try:
        SecureData.update_password(token)
        print('Token updated successfully')
    except Exception as e:
        print(f'Error updating token: {e}')


def update_form(form_url: str):
    form_id = form_url.split('/d/', 1)[1]
    form_id = form_id.split('/', 1)[0]
    main_lines: str = ''
    containing_file: str = 'GoogleStructures.py'
    with open(containing_file, 'r') as main:
        lines = main.readlines()
    for line in lines:
        if line.startswith('FORM_ID: ') or line.startswith('FORM_ID '):
            main_lines += f'FORM_ID : str = "{form_id}"\n'
            continue
        main_lines += line
    with open(containing_file, 'w') as main:
        main.write(main_lines)
    print(f'updated with {form_id}')


def update_sheet(sheet_url: str):
    sheet_id = sheet_url.split('/d/', 1)[1]
    sheet_id = sheet_id.split('/', 1)[0]
    main_lines: str = ''
    containing_file: str = 'GoogleStructures.py'
    with open(containing_file, 'r') as main:
        lines = main.readlines()
    for i, line in enumerate(lines):
        if line.startswith('SPREADSHEET_ID: ') or line.startswith('SPREADSHEET_ID '):
            main_lines += f'SPREADSHEET_ID : str = "{sheet_id}"\n'
            continue
        main_lines += line
    with open(containing_file, 'w') as main:
        main.write(main_lines)
    print(f'updated with {sheet_id}')



if __name__ == '__main__':
    if len(sys.argv) == 1:
        functions = {
            'update_form': update_form,
            'update_spreadsheet': update_sheet,
            'update_token': update_token
        }
        choice: callable = selection(functions)
        if choice == update_form:
            update_form(input('Enter the URL of the google form: '))
            exit(0)
        if choice == update_sheet:
            update_sheet(input('Enter the URL of the google spreadsheet: '))
            exit(0)
        if choice == update_token:
            update_token()
    elif len(sys.argv) != 3 or sys.argv[1] != 'form_update':
        print('Argument missmatch')
        print('Usage: python3 update.py')
        print('Usecase: ["update_form", "update_spreadsheet", "update_token"]')
    else:
        update_form(sys.argv[2])
