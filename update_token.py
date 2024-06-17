import os
import sys


def get_pass() -> str:
    import getpass
    password = getpass.getpass("Enter your token: ")
    return password


def get_token() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    return get_pass()
        

def set_environ(token: str) -> None:
    os.environ["REPLICATE_API_TOKEN"] = token


def main(token) -> None:
    try:
        import securepassing
        securepassing.update_password(token)
        print('Token updated successfully')
    except Exception as e:
        print(f'Error updating token: {e}')
    

if __name__ == "__main__":
    main(get_token())