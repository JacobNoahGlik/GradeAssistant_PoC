import package_manager

from GoogleStructures import GoogleUtils
from presets import Presets
import sys



class RubricChanges:
    @staticmethod
    def download(
        print_status: bool = True, 
        defined_filename: str | None = None
    ):
        if defined_filename is not None:
            rubric_location = defined_filename
        else:
            rubric_location = RubricChanges.get_filename()
        if GoogleUtils.google_sheets_to_csv(
            Presets.GOOGLE_SPREADSHEET_ID,
            'Rubric',
            rubric_location
        ):
            if print_status: print('> download success')
        else:
            if print_status: print('> download failure')

    @staticmethod
    def upload(
        print_status: bool = True, 
        defined_filename: str | None = None
    ):
        if defined_filename is not None:
            rubric_location = defined_filename
        else:
            rubric_location = RubricChanges.get_filename()
        if GoogleUtils.csv_to_google_sheets(
            rubric_location,
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



if __name__ == '__main__':
    if len(sys.argv) not in [2, 3] or sys.argv[1].lower() not in ['--download', '--upload']:
        print('UsageError - expected:')
        print('\t"python3 update_rubric.py --download [optional: rubric_filename.csv]"')
        print('\t"python3 update_rubric.py --upload [optional: rubric_filename.csv]"')

    if sys.argv[1].lower() == '--download':
        RubricChanges.download()
    else:
        RubricChanges.upload()
