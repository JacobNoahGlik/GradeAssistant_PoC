import sys
from securepassing import SecureData
from util import secure_input, selection, update_presets, id_strip, identity



containing_file: str = 'presets.py'
public_facing_functions: list[str] = [
    'update_form',
    'update_spreadsheet',
    'update_token'
]
private_facing_functions: list[str] = [
    '_update_ai_model',
    '_update_comma_placeholder',
    '_update_graded_submissions_location',
    '_update_gradebook report_location',
    '_update_submissions_location',
    '_update_rubric_location'
]



def get_token() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    return secure_input("Enter your token: ")


def update_token():
    token = get_token()
    try:
        SecureData.update_password(token)
        print('Token updated successfully')
    except Exception as e:
        print(f'Error updating token: {e}')


def run_choice(choice: str) -> bool:
    if choice == 'update_token':
        update_token()
        return True

    global containing_file
    url: str = "https://replicate.com/pricing#language-models"
    selections: list[tuple[str, str, str]] = [
        ('update_form',                         '    GOOGLE_FORM_ID',              "Enter the URL of the Google Form: ", id_strip),
        ('update_sheet',                        '    GOOGLE_SPREADSHEET_ID',       "Enter the URL of the Google Spreadsheet: ", id_strip),
        ('_update_comma_placeholder',           '    COMMA_PLACEHOLDER',           "Enter comma placeholder: ", identity),
        ('_update_graded_submissions_location', '    GRADED_SUBMISSIONS_LOCATION', "Enter new graded-submissions location: ", identity),
        ('_update_gradebook_report_location',   '    GRADED_SUBMISSIONS_LOCATION', "Enter new graded-submissions-report location: ", identity),
        ('_update_submissions_location',        '    SUBMISSIONS_LOCATION',        "Enter new submissions location: ", identity),
        ('_update_rubric_location',             '    RUBRIC_LOCATION',             "Enter new rubric location: ", identity),
        ('_update_ai_model',                    '    AI_MODEL',                   f"Enter model name as it apears on {url}: ", identity)
    ] 
    for (selection, find, replace, process) in selections:
        if choice == selection:
            update_presets(
                containing_file,
                find,
                f'{find}: str = "{process(input(replace))}"'
            )
            return True
    return False



if __name__ == '__main__':
    if len(sys.argv) != 1 or not (len(sys.argv) == 2 and sys.argv[1] == '--show-all'):
        print('Argument missmatch')
        print('Usage: python3 update.py')
        print('Options: ["update_form", "update_spreadsheet", "update_token"]')
        exit(1)

    functions: list[str] = public_facing_functions
    if len(sys.argv) == 2 and sys.argv[1] == '--show-all':
        functions += private_facing_functions

    choice: str = selection(functions)
    run_choice(choice)
