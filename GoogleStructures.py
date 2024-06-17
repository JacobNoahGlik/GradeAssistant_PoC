# from RubricStructures import __PLACEHOLDER__

class SubmissionTable:
    def __init__(self, questions: list['GoogleFormsQuestion']):
        self.header = [
            'responseId',
            'createTime',
            'lastSubmittedTime'
        ]
        self.default_name_col: int = 4
        for question in questions:
            self.header.append(csv_safe(question.text))
        self._questions = questions
        self._id_to_q = {q.id: q.text for q in questions}
        self.submissions: dict[str, list] = {}

    def responses_by_header(self, question: str) -> list[tuple[str, str]]:
        wh_index = self.header.index(question)
        output: list[tuple[str, str]] = []
        for subID, submission in self.submissions.items():
            output.append((subID, submission[wh_index]))
        return output

    def get_questions(self) -> list[str]:
        return self.header[3:]

    def user_lookup(self, responseId: str) -> str:
        candidate = self._find_name_index()
        if candidate == -1:
            return self.submissions[responseId][self.default_name_col]
        return self.submissions[responseId][candidate]
    
    def _find_name_index(self) -> int:
        for i, question in enumerate(self.get_questions()):
            if question.lower() in ['name', 'enter your name', 'first name', 'last name']:
                return i + 3
        return -1

    def add_submission(self, submission):
        temp: list = [submission['responseId'], submission['createTime'], submission['lastSubmittedTime']] + ([''] * (len(self.header) - 3))
        # counter: int = 3
        for question_id, answer in submission['answers'].items():
            question_text: str = csv_safe(self._id_to_q[question_id])
            if question_text not in self.header:
                raise Exception(f'Could not find Question({question_text}) in table({self.header})')
            temp[self.header.index(question_text)] = answer['textAnswers']['answers'][0]['value'].replace('“', '"').replace('”', '"').replace('’', "'")
            # while self.header[counter] != self._id_to_q[question_id]:
            #     counter += 1
            #     if counter >= len(self.header):
            #         print('\n\n\n')
            #         print(f'{self.header=}')
            #         print(f'{question_id=}')
            #         print(f'{self._id_to_q[question_id]=}')
            #         raise Exception(f'Question {answer["questionId"]} not found')
            #     temp.append('')
            # temp.append(answer['textAnswers']['answers'][0]['value'])
            # counter += 1
        self.submissions[submission['responseId']] = temp
        
    def to_csv(self, path, display_outcome: bool = True) -> bool:
        try_again: bool = True
        while try_again:
            try:
                with open(path, 'w') as csv:
                    csv.write(','.join(self.header))
                    for submission in self.submissions.values():
                        csv.write('\n')
                        s = (','.join(submission)).replace('\n', ' ')
                        csv.write(s)
                if display_outcome: print(f'> Updated "{path}" successfully')
                return True
            except PermissionError as e:
                print(f"Encountered permission error while triing to write to '{path}'.")
                print("Some process may be using this file... please close the process before trying again.")
                if input("  > try again? (y/n) ") not in ['y', 'yes', 'ye', 'yeah']:
                    try_again = False
        if display_outcome: print(f'> Failed to update "{path}"!')
        return False



def csv_safe(s: str) -> str:
    return s.replace(',', '<INSERT_COMMA>').replace('“', '"').replace('”', '"').replace('’', "'").replace('\n', ' ')



class GooglePageBreakException(Exception):
    pass


                
class GoogleFormsQuestion:
    def __init__(self, question_json):
        if 'pageBreakItem' in question_json:
            raise GooglePageBreakException
        try:
            self.id = question_json['questionItem']['question']['questionId']
            self.text = question_json['title']
            self.itemID = question_json['itemId']
        except Exception as e:
            print(f'{question_json=}')
            raise e