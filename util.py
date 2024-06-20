import warnings
import getpass
import os
import math
from presets import Presets



def get_pass(message: str) -> str:
    password = getpass.getpass(message)
    return password


def deprecated(func):
    def wrapper(*args, **kwargs):
        warnings.warn(f"{func.__name__} is deprecated", category=DeprecationWarning)
        return func(*args, **kwargs)
    return wrapper


def set_environ(token: str) -> None:
    os.environ["REPLICATE_API_TOKEN"] = token


def selection(listing: dict[str, callable]) -> callable:
    print('Please select one of the following')
    for i, key in enumerate(listing.keys()):
        print(f'    {i + 1}. {key}')
    selection = input('> ')
    valid, response = validate(selection, _isnumber=True, _max_size=i + 1, whitelist=list(listing.keys()))
    while (not valid):
        print(f"Could not select. ERROR: '{response}'")
        print('Please select one of the following')
        for i, key in enumerate(listing.keys()):
            print(f'    {i + 1}. {key}')
        selection = input('> ')
        valid, response = validate(selection, _isnumber=True, _max_size=i + 1, whitelist=list(listing.keys()))
    if type(response) == int:
        return listing[
            list(listing.keys())[response]
        ]
    return listing[response]


def validate(inp: str, _isnumber: bool = False, _max_size: int = -1, whitelist: list = []) -> tuple[bool, str]:
    if inp.lower() in whitelist:
        return True, inp
    if _isnumber:
        try:
            if _max_size >= int(inp):
                return True, int(inp)
            return False, f'{inp} is too large, expected 1 - {_max_size}'
        except ValueError:
            return False, f'"{inp}" is not a member of the list [{",".join(whitelist)}] and cannot be converted to a number'
    return False, f'"{inp}" is not a member of the list [{",".join(whitelist)}]'


def safe_write(action: callable, param: tuple, path: str, display_outcome: bool = True) -> bool:
    try_again: bool = True
    while try_again:
        try:
            action(param[0], param[1])
            return True
        except PermissionError as e:
            print(f"Encountered permission error while triing to write to '{path}'.")
            print("Some process may be using this file... please close the process before trying again.")
            if input("  > try again? (y/n) ") not in ['y', 'yes', 'ye', 'yeah']:
                try_again = False
    if display_outcome: print(f'Failed to update "{path}"!')
    return False


def get_sheet_values(sheet) -> tuple[str, str]:
    return (sheet['properties']['title'], sheet['properties']['sheetId'])


def to_csv_safe(s: str) -> str:
    return s.replace(',', Presets.COMMA_PLACEHOLDER).replace('“', '"').replace('”', '"').replace('’', "'").replace('\n', ' ')


def from_csv_safe(s: str) -> str:
    return s.replace(Presets.COMMA_PLACEHOLDER, ',')


def value_to_score(val: int) -> str:
    return f'Score {val}'


def update_adendum(adendum_location: str = 'adendum.gd', rubric_location: str = 'rubric.csv', length: int = 6):
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
    return s.replace('“', '"').replace('”', '"').replace('’', "'").replace(",", Presets.COMMA_PLACEHOLDER)


def calc_volatility(scores: list[int], min: int, max: int, rounding: int = 2) -> float:
    if not scores:
        return 0
    mean = sum(scores) / len(scores)
    variance = sum((x - mean) ** 2 for x in scores) / len(scores)
    std_dev = math.sqrt(variance)
    max_std_dev = (max - min) / 2
    volatility = (std_dev / max_std_dev) * 100
    return round(volatility, rounding)


def classification(Volatility: float) -> str:
    if Volatility < 15:
        return 'Very Consistent'
    if Volatility < 32:
        return 'Consistent'
    if Volatility < 55:
        return 'Somewhat Inconsistent'
    if Volatility < 70:
        return 'Very Inconsistent'
    return 'HIGHLY VOLATILE'


def comma_swap(s: str) -> str:
    """Replaces commas with the presets.Presets.COMMA_PLACEHOLDER string."""
    return s.replace(',', Presets.COMMA_PLACEHOLDER)


def time_formater(seconds: float) -> str:
    hours: int = math.floor(seconds / 3600)
    seconds -= hours * 3600
    minutes: int = math.floor(seconds / 60)
    seconds -= minutes * 60
    return f'{hours}:{minutes}:{seconds}'



class InvalidUsageError(Exception):
    pass



class Counter:
    def __init__(self, file: str = 'counter.txt'):
        self.file: str = file
        self.count: int = 0
        if not os.path.exists(self.file) or not os.path.isfile(self.file):
            self._reset()
        else:
            self._pull()
    
    def increment(self, incement_by: int = 1) -> None:
        self.count += incement_by
        self._update()

    def overwrite(self, value: int) -> None:
        self.count = value
        self._update()

    def _reset(self) -> None:
        self.count = 0
        self._update()

    def _pull(self) -> int:
        with open(self.file, 'r') as f:
            self.count = int(f.read())
    
    def _update(self) -> None:
        with open(self.file, 'w') as f:
            f.write(f'{self.count}')



if __name__ == '__main__':
    raise InvalidUsageError("This file should not be run. Only import this file and its contents. Do not run this file directly.")
