from GoogleStructures import GoogleUtils
from presets import Presets



GoogleUtils.csv_to_google_sheets(
    'rubric.csv',
    'Rubric',
    Presets.RUBRIC_LOCATION
)
