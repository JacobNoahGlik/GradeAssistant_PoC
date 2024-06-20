import replicate
from securepassing import SecureData
from util import InvalidUsageError, from_csv_safe, set_environ, Counter



class Auto_Grader_AI:
    def __init__(self, rubric: str, question: str):
        self.rubric: str = rubric
        self.question: str = question
        self._combiner: callable = Auto_Grader_AI.default_combiner

    def override_combiner(self, combiner: callable) -> None:
        self._combiner = combiner

    def grade_splitter(self, submission: str, splix: str = '\n', quantity: int = 2) -> list:
        if '\n' not in submission:
            return ['Score: 0', 'Abusive action detected. Type: Possible AI injection attack.']
        return self.grade(submission).split(splix, quantity - 1)

    def grade(
        self,
        submission: str,
        max_new_tokens: int = 250
    ) -> str:
        set_environ(SecureData.safe_logger())
        return ai.generate_response(
            self._combiner(self.question, submission, self.rubric),
            max_new_tokens=max_new_tokens
        )

    @staticmethod
    def default_combiner(question: str, submission:str,  rubric: str, prefix_file: str = 'background.txt') -> str:
        with open(prefix_file, 'r') as f:
            prefix = f.read()
        tripple_quote = '"""'
        return f'{prefix}' \
               f'*RUBRIC*\n{tripple_quote}\n{from_csv_safe(rubric)}\n{tripple_quote}\n\n\n'\
               f'*QUESTION*\n{tripple_quote}\n{from_csv_safe(question)}\n{tripple_quote}\n\n\n'\
               f'*SUBMISSION*\n{tripple_quote}\n{from_csv_safe(submission)}\n{tripple_quote}'



class ai:
    api_calls: Counter = Counter('ai_api_calls.counter')
    @staticmethod
    def generate_response(prompt, max_new_tokens: int = 250) -> str:
        try:
            concat: str = ''
            for event in replicate.stream(
                    "meta/llama-2-70b-chat",
                    input={
                        "prompt": prompt,
                        "max_new_tokens": max_new_tokens
                    },
            ):
                concat += str(event)
            ai.api_calls.increment()
            return concat
        except httpx.ConnectTimeout as hct:
            print(concat)
            raise hct



if __name__ == "__main__":
    raise InvalidUsageError("This file should not be run. Only import this file and its contents. Do not run this file directly.")
