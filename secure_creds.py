with open('credentials.json', 'r') as cj:
    lines = cj.readlines()

secured_credentials = ''
for line in lines:
    lt = line.strip()
    if lt.startswith('"client_id"') or lt.startswith('"client_secret"'):
        known, secret = line.split(':')
        prefix, secret, postfix = secret.split('"')
        secured_credentials += known + ':' + prefix + '"' + ('*' * len(secret)) + '"' + postfix
    else:
        secured_credentials += line
    secured_credentials += "\n"
with open('credentials_secured.json', 'w') as csj:
    csj.write(secured_credentials)