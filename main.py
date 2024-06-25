from GoogleStructures import SubmissionTable, GoogleFormsQuestion, GoogleUtils
from RubricStructures import Grader
from presets import Presets



if __name__ == '__main__':
    raw_questions, raw_submissions = GoogleUtils.get_form_questions_and_submissions(Presets.GOOGLE_FORM_ID)
    questions: list[GoogleFormsQuestion] = GoogleUtils.get_GFQ_list(raw_questions)

    table = SubmissionTable(questions)
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
