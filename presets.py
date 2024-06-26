class Presets:
    AI_MODEL: str = "meta/llama-2-70b-chat"
    GOOGLE_SPREADSHEET_ID: str = ""
    GOOGLE_FORM_ID: str = ""
    GOOGLE_FORM_USER_IDENTIFIER: str = "Name"
    COMMA_PLACEHOLDER: str = '<INSERT_COMMA>'
    GRADED_SUBMISSIONS_LOCATION: str = './output/graded_submissions.csv'
    GRADEBOOK_REPORT_LOCATION: str = './output/gradebook_report.csv'
    SUBMISSIONS_LOCATION: str = './output/submissions.csv'
    RUBRIC_LOCATION: str = 'rubric.csv'
    REQUIRED_PACKAGES_FILENAME: str = 'required_packages.txt'



class PresetsMissingOrCorruptedException(Exception):
    pass



class InvalidUsageError(Exception):
    pass



for preset_name, value in Presets.__dict__.items():
    if isinstance(value, str) and not value.strip():
        print(
           f"\nPresets.{preset_name} is not defined! All variables in the Presets class (found in the 'presets.py' file) must have values. " \
            "Update the values directly or run 'python3 update.py --show-all'\n"
        )
        exit()



if __name__ == '__main__':
    raise InvalidUsageError("This file should not be run. Only import this file and its contents. Do not run this file directly.")
