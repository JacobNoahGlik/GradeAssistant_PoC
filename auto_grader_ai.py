import package_manager

import replicate
from presets import InvalidUsageError, Presets
from secureparsing import SecureParsing
from util import Counter, from_csv_safe, set_environ



class Auto_Grader_AI:
    def __init__(self, rubric: str, question: str):
        self.rubric: str = rubric
        self.question: str = question
        self._combiner: callable = Auto_Grader_AI.default_combiner
        self._REPLICATE_TOKEN = SecureParsing.safe_logger()

    def override_combiner(self, combiner: callable) -> None:
        self._combiner = combiner

    def safe_grade_splitter(self, submission: str, splix: str = '\n', quantity: int = 2, retry: int = 3) -> list:
        retry_count = 0
        while True:
            try:
                return self.grade_splitter(submission, splix=splix, quantity=quantity)
            except Exception as e:
                retry_count += 1
                if retry < retry_count:
                    print('')
                    return ['Score 0', 'Could not reach Replicate Servers. THIS WAS NOT GRADED BY THE AI - THIS IS A DEFAULT RESPONSE']
                if retry_count == 1:
                    print('')
                print(f'<WARNING> Caught exception ({e.__repr__()}). Retrying connection for the {self._format(retry_count)} time.')

    def _format(self, time: int) -> str:
        if time == 0:
            return '0'
        if time == 1:
            return '1st'
        if time == 2:
            return '2nd'
        if time == 3:
            return '3rd'
        return f'{time}th'

    def grade_splitter(self, submission: str, splix: str = '\n', quantity: int = 2) -> list:
        ai_response: str = self.grade(submission)
        if '\n' not in ai_response:
            return [
                'Score: 0', 
                f'Abusive action detected. Type: Possible AI injection attack. Initial assessment: "{ai_response}"'
            ]
        return ai_response.split(splix, quantity - 1)

    def grade(self, submission: str, max_new_tokens: int = 250) -> str:
        set_environ(self._REPLICATE_TOKEN)
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
               f'**RUBRIC**\n{tripple_quote}\n{from_csv_safe(rubric)}\n{tripple_quote}\n\n\n'\
               f'**QUESTION**\n{tripple_quote}\n{from_csv_safe(question)}\n{tripple_quote}\n\n\n'\
               f'**SUBMISSION**\n{tripple_quote}\n{from_csv_safe(submission)}\n{tripple_quote}'



class ai:
    api_calls: Counter = Counter('ai_api_calls.counter')
    @staticmethod
    def generate_response(prompt, max_new_tokens: int = 250) -> str:
        concat: str = ''
        for event in replicate.stream(
                Presets.AI_MODEL,
                input={
                    "prompt": prompt,
                    "max_new_tokens": max_new_tokens
                },
        ):
            concat += str(event)
        ai.api_calls.increment()
        return concat



if __name__ == "__main__":
    raise InvalidUsageError("This file should not be run. Only import this file and its contents. Do not run this file directly.")
