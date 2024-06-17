import GoogleStructures
from auto_grader_ai import Auto_Grader_AI
from writer import safe_write

__PLACEHOLDER__: str = '<INSERT_COMMA>'

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
        global __PLACEHOLDER__
        with open(self.filename, "r") as table:
            lines = table.read().split('\n')
        self._cols = [
            col.replace(__PLACEHOLDER__, ',') 
            for col in lines[0].split(',')
        ]
        self._search_for_question_id()
        for line in lines[1:]:
            if line in ['', ' ', '\t']:
                continue
            row = line.split(',')
            self.rubric[
                row[self.qid].replace(__PLACEHOLDER__, ',')
            ] = self._dictify_row(row)

    def rubric_by_question(self, question: str) -> None | str:
        if question not in self.rubric.keys():
            keys = [csv_safe_text(key) for key in self.rubric.keys()]
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
        kyes = [csv_safe_text(key) for key in self.Rubric.rubric.keys()] # CHANGE
        for q in self.Submissions.get_questions():
            question = csv_safe_text(q)
            if question in kyes:
                self.Gradeable_questions.append(question)
            # else:
            #    print(f'Question "{question}" not found in rubric table {self.Filename}')
            #     for i, key in enumerate(self.Rubric.rubric.keys()):
            #         print(f'\t"{i + 2}. {key}"')

    def _get_total_iter(self) -> int:
        counter: int = 0
        for question in self.Gradeable_questions:
            counter += len(self.Submissions.responses_by_header(question))
        return counter

    def grade_submissions(self, file_out: str = './output/graded_submissions.csv') -> None:
        std_out: str = 'Name,Question,Response,AI Grade,AI Reasoning\n'
        total_iter: int = self._get_total_iter()
        counter: int = 0
        for question in self.Gradeable_questions:
            print(f'AI has graded {counter} out of {total_iter} submissions', end='\r')
            ai = Auto_Grader_AI(self.Rubric.rubric_by_question(question), question)
            for (responseId, response) in self.Submissions.responses_by_header(question):
                ai_grade, ai_reasoning = ai.grade_splitter(response) #  'Score 3', 'made up' 
                score: int = self._num(ai_grade)
                name = csv_safe_text(self.Submissions.user_lookup(responseId))
                std_out += f'{name},{csv_safe_text(question)},{csv_safe_text(response)},{value_to_score(score)},{csv_safe_text(ai_reasoning)}\n'
                counter += 1
                self._add_grade(name, score)
                print(f'AI has graded {counter} out of {total_iter} submissions', end='\r')
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

    def _gredebook_report(self) -> str:
        out: str = ''
        for user in self.Gradebook.keys():
            grades: list = self.Gradebook[user]
            letter, percentage = self._letter_grade(sum(grades), len(grades))
            out += f'{user}: {letter}\n    Reasoning:\n\t > AI Scores: [' + ','.join([str(g) for g in grades]) + f']\n\t > Avg Score: {percentage * 0.03} ({percentage}%)\n'
        return out

    def _letter_grade(self, number: int, times: int) -> tuple[str, float]:
        grade: float = number / (times * 3)
        if grade >= 0.9:
            return ('A', round(grade * 100, 1))
        elif grade >= 0.8:
            return ('B', round(grade * 100, 1))
        elif grade >= 0.7:
            return ('C', round(grade * 100, 1))
        elif grade >= 0.6:
            return ('D', round(grade * 100, 1))
        return ('F', round(grade * 100, 1))

def value_to_score(val: int) -> str:
    return f'Score {val}'


def update_adendum(adendum_location: str = 'adendum.gd', rubric_location: str = 'rubric.csv', length: int = 6):
    global __PLACEHOLDER__
    with open(adendum_location, 'r') as adendum:
        lines = adendum.read().split('\n')
    csv_add: str = '\n'
    for i, line in enumerate(lines):
        csv_add += f'{correct_string(line)},'
        if i % length == length - 1:
            csv_add = csv_add[:-1] + '\n'
    with open(rubric_location, 'a') as rubric:
        rubric.write(csv_add)


def correct_string(s: str) -> str:
    return s.replace('“', '"').replace('”', '"').replace('’', "'").replace(",", __PLACEHOLDER__)


def csv_safe_text(s: str) -> str:
    return s.replace('“', '"').replace('”', '"').replace('’', "'").replace(",", __PLACEHOLDER__).replace('\n', ' ')

# def question_for_ai(rubric: RubricTable, question: str, response, background_file: str = 'background.txt')
if __name__ == '__main__':
    rubric = RubricTable('rubric.csv')
    # print(rubric)
    print(rubric.rubric_by_question('What was the greatest challenge that you faced in mentoring?  How did you learn/grow from it?'))
    