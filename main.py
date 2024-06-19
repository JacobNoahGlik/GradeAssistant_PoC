from GoogleStructures import SubmissionTable, GoogleFormsQuestion, FORM_ID, SPREADSHEET_ID, GoogleUtils
import RubricStructures



if __name__ == '__main__':
    raw_questions, raw_submissions = GoogleUtils.get_form_questions_and_submissions(FORM_ID)
    questions: list[GoogleFormsQuestion] = GoogleUtils.get_GFQ_list(raw_questions)
    table = SubmissionTable(questions)
    for submission in raw_submissions:
        table.add_submission(submission)
    table.to_csv('./output/submissions.csv')
    grader = RubricStructures.Grader('rubric.csv', table)
    grader.grade_submissions()
    grader._gredebook_report()
    GoogleUtils.bulk_csv_to_google_sheets(
        SPREADSHEET_ID,
        [
            ('./output/submissions.csv', 'Responses'),
            ('./output/graded_submissions.csv', 'AI Grades'),
            ('./output/gradebook_report.csv', 'Student Gradebook')
        ]
    )
    