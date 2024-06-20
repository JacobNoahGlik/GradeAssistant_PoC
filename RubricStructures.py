import GoogleStructures
from auto_grader_ai import Auto_Grader_AI
from util import safe_write, to_csv_safe, InvalidUsageError, classification, calc_volatility, value_to_score, comma_swap, time_formater
from presets import Presets

class RubricTable:
    def __init__(self, filename: str):
        self.filename = filename
        self._cols: list = []
        self.qid: int = -1
        self.rubric: dict[str, dict[str, str]] = {}
        self._load_rubric_table()

    def __repr__(self) -> str:
        s: str = f'RubricTable: {self.filename}\n'
        for k, v in self.rubric.items():
            s += f'\t{k}:\n'
            for k2, v2 in v.items():
                s += f'\t > {k2}: "{v2}"\n'
        return s
    
    def _load_rubric_table(self) -> None:
        with open(self.filename, "r") as table:
            lines = table.read().split('\n')
        self._cols = [
            comma_swap(col)
            for col in lines[0].split(',')
        ]
        self._search_for_question_id()
        for line in lines[1:]:
            if line in ['', ' ', '\t']:
                continue
            row = line.split(',')
            self.rubric[
                comma_swap(row[self.qid])
            ] = self._dictify_row(row)

    def rubric_by_question(self, question: str) -> None | str:
        if question not in self.rubric.keys():
            keys = [to_csv_safe(key) for key in self.rubric.keys()]
            if question not in keys:
                return None
            index = keys.index(question)
            question = list(self.rubric.keys())[index]
        return self._to_string(self.rubric[question])

    def _to_string(self, rubric: dict[str, str]) -> str:
        s: str = ''
        for k, v in rubric.items():
            s += f'{k}: "{v}"\n'
        return s
    
    def _dictify_row(self, row: list) -> dict[str, str]:
        d: dict[str, str] = {}
        for i, r in enumerate(row):
            d[self._cols[i]] = r
        return d
    
    def _search_for_question_id(self) -> None:
        for i, col in enumerate(self._cols):
            if col.lower() == 'question':
                self.qid = i
                return
        self.qid = -1
        raise QuestionColumnNotFoundException(f'Could not find question column in rubric table {self.filename}.\n{self._cols = }')



class QuestionColumnNotFoundException(Exception):
    pass



class Grader:
    def __init__(self, RubricTableFilename: str, submissions: GoogleStructures.SubmissionTable):
        self.Filename: str = RubricTableFilename
        self.Gradebook: dict[str, list[int]] = {}
        self.Submissions = submissions
        self.Rubric: RubricTable = RubricTable(self.Filename)
        self.Gradeable_questions: list = []
        self._load_gradeable_questions()

    def _load_gradeable_questions(self) -> None:
        kyes = [to_csv_safe(key) for key in self.Rubric.rubric.keys()]
        for q in self.Submissions.get_questions():
            question = to_csv_safe(q)
            if question in kyes:
                self.Gradeable_questions.append(question)

    def _get_total_iter(self) -> int:
        counter: int = 0
        for question in self.Gradeable_questions:
            counter += len(self.Submissions.responses_by_header(question))
        return counter

    def grade_submissions(self, file_out: str) -> None:
        std_out: str = 'Name,Question,Response,AI Grade,AI Reasoning\n'
        total_iter: int = self._get_total_iter()
        counter: int = 0
        avg_api_call_time: float = 3.41
        projected_time: int = total_iter * avg_api_call_time
        for question in self.Gradeable_questions:
            print(f'AI has graded {counter} out of {total_iter} submissions. (Projected time left: {time_formater(projected_time - avg_api_call_time * counter)})', end='\r')
            ai = Auto_Grader_AI(self.Rubric.rubric_by_question(question), question)
            for (responseId, response) in self.Submissions.responses_by_header(question): # this for-loop should be replaced with multithreading
                ai_grade, ai_reasoning = ai.grade_splitter(response) # this takes about 3.5 seconds per api-call
                score: int = self._num(ai_grade)
                name = to_csv_safe(self.Submissions.user_lookup(responseId))
                std_out += f'{name},{to_csv_safe(question)},{to_csv_safe(response)},{value_to_score(score)},{to_csv_safe(ai_reasoning)}\n'
                counter += 1
                self._add_grade(name, score)
                print(f'AI has graded {counter} out of {total_iter} submissions. (Projected time left: {time_formater(projected_time - avg_api_call_time * counter)})', end='\r')
        print('')
        try_again: bool = True
        while try_again:
            try:
                with open(file_out, 'w') as graded:
                    graded.write(std_out)
                print('\n> Wrote grades to file successfully!\n')
                return
            except PermissionError as e:
                print(f"Encountered permission error while triing to write to '{file_out}'.")
                print("Some process may be using this file... please close the process before trying again.")
                if input("  > try again? (y/n) ") not in ['y', 'yes', 'ye', 'yeah']:
                    try_again = False
        print(f'> Failed to update "{file_out}"!')

    def _num(self, s: str) -> int:
        while len(s) > 0:
            if s[0].isdigit():
                return int(s[0])
            s = s[1:]
        return 0
    
    def _add_grade(self, user: str, grade: int) -> None:
        if user not in self.Gradebook.keys():
            self.Gradebook[user] = []
        self.Gradebook[user].append(grade)

    def run_grading_routine(
            self, 
            graded_submissions_file: str, 
            gradebook_report_file: str
        ) -> str:
        self.grade_submissions(graded_submissions_file)
        return self._gredebook_report(gradebook_report_file)

    def _gredebook_report(self, path: str) -> str:
        header: str = ['Name', 'email', 'phone number', 'AI Leter Grade', 'AI Percentage', 'Avg AI Score', 'Volatility', 'Classification', 'Scores']
        csv_str: str = ','.join(header) + '\n'
        for user in self.Gradebook.keys():
            grades: list = self.Gradebook[user]
            letter, percentage = self._letter_grade(sum(grades), len(grades))
            email, phone_number = self.Submissions.get_email_and_phone(user)
            Volatility: float = calc_volatility(grades, 0, 9)
            csv_str += ','.join(
                [
                    to_csv_safe(user),
                    to_csv_safe(email),
                    to_csv_safe(phone_number),
                    to_csv_safe(letter),
                    f'{percentage / 100}',
                    f'{round(percentage * 0.09, 1)}',
                    f'{Volatility}',
                    f'{classification(Volatility)}',
                    to_csv_safe(f'[{",".join([str(g) for g in grades])}]')
                ]
            ) + '\n'
        with open(path, 'w') as f:
            f.write(csv_str)

    def _letter_grade(self, number: int, times: int) -> tuple[str, float]:
        grade: float = number / (times * 9)
        if grade >= 0.9:
            return ('A', round(grade * 100, 1))
        elif grade >= 0.8:
            return ('B', round(grade * 100, 1))
        elif grade >= 0.7:
            return ('C', round(grade * 100, 1))
        elif grade >= 0.6:
            return ('D', round(grade * 100, 1))
        return ('F', round(grade * 100, 1))


if __name__ == "__main__":
    raise InvalidUsageError("This file should not be run. Only import this file and its contents. Do not run this file directly.")
