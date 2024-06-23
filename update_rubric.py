from GoogleStructures import GoogleUtils
from presets import Presets
import sys



class RubricChanges:
    @staticmethod
    def download_rubric(print_status: bool = True):
        if GoogleUtils.google_sheets_to_csv(
            Presets.GOOGLE_SPREADSHEET_ID,
            'Rubric',
            RubricChanges.get_filename()
        ):
            if print_status: print('> download success')
        else:
            if print_status: print('> download failure')

    @staticmethod
    def upload_rubric(print_status: bool = True):
        if GoogleUtils.csv_to_google_sheets(
            RubricChanges.get_filename(),
            'Rubric',
            Presets.RUBRIC_LOCATION
        ):
            if print_status: print('> upload success')
        else:
            if print_status: print('> upload failure')

    @staticmethod
    def get_filename() -> str:
        if len(sys.argv) != 3:
            return input('> Enter rubric filename: ')
        return sys.argv[2]



if len(sys.argv) not in [2, 3] or sys.argv[1].lower() not in ['--download', '--upload']:
    print('UsageError - expected:')
    print('\t"python3 update_rubric.py --download [optional: rubric_filename.csv]"')
    print('\t"python3 update_rubric.py --upload [optional: rubric_filename.csv]"')

if sys.argv[1].lower() == '--download':
    RubricChanges.download_rubric()
else:
    RubricChanges.upload_rubric()
