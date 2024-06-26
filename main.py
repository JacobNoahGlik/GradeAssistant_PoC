import package_manager

from GoogleStructures import SubmissionTable, GoogleFormsQuestion, GoogleUtils
from RubricStructures import Grader
from presets import Presets



if __name__ == '__main__':
    google_form: tuple[list[dict], list[dict]] = GoogleUtils.get_form_questions_and_submissions(Presets.GOOGLE_FORM_ID)
    raw_questions: list[dict]   = google_form[0]
    raw_submissions: list[dict] = google_form[1]
    questions: list[GoogleFormsQuestion] = GoogleUtils.get_GFQ_list(raw_questions)

    table: SubmissionTable = SubmissionTable(questions)
    table.bulk_add_submissions(raw_submissions)
    table.to_csv(Presets.SUBMISSIONS_LOCATION)

    grader = Grader(Presets.RUBRIC_LOCATION, table)
    gradebook_report: str = grader.run_grading_routine(
        Presets.GRADED_SUBMISSIONS_LOCATION,
        Presets.GRADEBOOK_REPORT_LOCATION,
        order_by='Name'  # CASE SENSITIVE
    )

    GoogleUtils.bulk_csv_to_google_sheets(
        Presets.GOOGLE_SPREADSHEET_ID,
        [
            (Presets.SUBMISSIONS_LOCATION,          'Responses'),
            (Presets.GRADED_SUBMISSIONS_LOCATION,   'AI Grades'),
            (Presets.GRADEBOOK_REPORT_LOCATION,     'Student Gradebook')
        ]
    )
