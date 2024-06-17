import ai
from update_token import set_environ
from securepassing import safe_logger as get_token
# from RubricStructures import __PLACEHOLDER__


class Auto_Grader_AI:
    def __init__(self, rubric: str, question: str):
        self.rubric: str = rubric
        self.question: str = question
        self._combiner = Auto_Grader_AI.combiner

    def override_combiner(self, combiner) -> None:
        self._combiner = combiner

    def grade_splitter(self, submission: str, splix: str = '\n', quantity: int = 2) -> list:
        return self.grade(submission).split(splix, quantity - 1)

    def grade(
        self,
        submission: str,
        max_new_tokens: int = 250
    ) -> str:
        set_environ(get_token())
        return ai.response(self._combiner(self.question, submission, self.rubric))
        # print(self._combiner(self.question, submission, self.rubric))
        # exit()

    @staticmethod
    def combiner(question: str, submission:str,  rubric: str, prefix_file: str = 'background.txt') -> str:
        with open(prefix_file, 'r') as f:
            prefix = f.read()
        tripple_quote = '"""'
        return f'{prefix}' \
               f'*RUBRIC*\n{tripple_quote}\n{csv_unsafe(rubric)}\n{tripple_quote}\n\n\n'\
               f'*QUESTION*\n{tripple_quote}\n{csv_unsafe(question)}\n{tripple_quote}\n\n\n'\
               f'*SUBMISSION*\n{tripple_quote}\n{csv_unsafe(submission)}\n{tripple_quote}'
    


def csv_unsafe(s: str) -> str:
    return s.replace('<INSERT_COMMA>', ',')