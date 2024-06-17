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
            return None
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


# def question_for_ai(rubric: RubricTable, question: str, response, background_file: str = 'background.txt')
if __name__ == '__main__':
    rubric = RubricTable('rubric.csv')
    # print(rubric)
    print(rubric.rubric_by_question('What was the greatest challenge that you faced in mentoring?  How did you learn/grow from it?'))