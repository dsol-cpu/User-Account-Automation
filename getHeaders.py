import requests
url = "https://www.tiktok.com/signup/phone-or-email/email"
response = requests.get(url, allow_redirects=False)

print(response.headers)
print(response.cookies)
