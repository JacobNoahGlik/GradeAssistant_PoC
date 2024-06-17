import sys

# https://docs.google.com/forms/d/1EyG-2N0zkbaBya67Qc2sPv7ZF7YngLyGOm8brPgOyps/edit
def update_form(form_url: str):
    form_id = form_url.split('/d/', 1)[1]
    form_id = form_id.split('/', 1)[0]
    main_lines: str = ''
    with open('main.py', 'r') as main:
        lines = main.readlines()
    for i, line in enumerate(lines):
        if line.startswith('FORM_ID: ') or line.startswith('FORM_ID '):
            main_lines += f'FORM_ID : str = "{form_id}"\n'
            continue
        main_lines += line
    with open('main.py', 'w') as main:
        main.write(main_lines)
    print(f'updated with {form_id}')


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



if __name__ == '__main__':
    if len(sys.argv) == 1:
        functions = {
            'update_form': update_form
        }
        choice: callable = selection(functions)
        if choice == update_form:
            update_form(input('Enter the URL of the google form: '))
            exit(0)
    elif len(sys.argv) != 3 or sys.argv[1] != 'form_update':
        print('Argument missmatch')
        print('Usage: python3 update.py form_update [form_url]')
    else:
        update_form(sys.argv[2])
