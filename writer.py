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
    if display_outcome: print(f'❌ Failed to update "{path}"!')
    return False