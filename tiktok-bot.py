import os
import datetime
import time
import random

import requests

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys

import undetected_chromedriver as uc
import json, csv

class My_Chrome():
	def __del__(self):
		pass

	def __init__(self, jsondata, zoho=False):
		self.csvdata = []
		self.emailProvider = ""

		while self.emailProvider != "google" and self.emailProvider != "yahoo":
			self.emailProvider = input("Enter your email provider(google/yahoo)").lower()
		
		with open(os.getcwd() + "/" + self.emailProvider + "Aliases.csv", mode ='r') as file:
			# reading the CSV file
			csvFile = csv.reader(file)

			# displaying the contents of the CSV file
			for row in csvFile:
				self.csvdata.append(row)

		self.logIn = False
		
		self.email = jsondata[self.emailProvider + "Email"]
		self.password = jsondata[self.emailProvider +"Password"]

		# with open(os.getcwd() + "/" + self.emailProvider + "Aliases.csv", mode ='r') as file:
		# 	# reading the CSV file
		# 	csvFile = csv.reader(file)

		# 	# displaying the contents of the CSV file
		# 	for row in csvFile:
		# 		self.csvdata.append(row)


		# desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
		# desired_capabilities['phantomjs.page.customHeaders.User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) ' \
        #                                                           'AppleWebKit/537.36 (KHTML, like Gecko) ' \
        #                                                           'Chrome/39.0.2171.95 Safari/537.36'
		# driver = webdriver.PhantomJS(desired_capabilities=desired_capabilities)

		#TODO: turn off the SameSite cookie for lastmx
		opts = Options()
		# opts.add_experimental_option('excludeSwitches', ['enable-logging'])
		# opts.add_experimental_option('excludeSwitches', ['enable-automation'])
		# opts.add_experimental_option('useAutomationExtension', False)

		args = [
		# "user-agent=Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41",
		# " --incognito",
		# " --no-referrers",
		# "--no-first-run --no-service-autorun --password-store=basic",
		# "--disable-extensions",
		# "--profile-directory=Default",
		# "--disable-plugins-discovery",
		# "--start-maximized",
		# "no-sandbox",
		# "--disable-inforbars",
		# "--disable-gpu",
		# "--headless",
		# "--disable-blink-features=AutomationControlled",
		# "window-size=1920,1000",
		# "--user-data-dir=C:/Users/Admin/AppData/Local/Google/Chrome/User Data",
		]

		for arg in args:
			opts.add_argument(arg)

		# opts.headless = True
		# s = Service(os.getcwd() + "/chromedriver.exe",)
		# self.browser = webdriver.Chrome(os.getcwd() + "/chromedriver.exe", options = opts)

		self.browser = uc.Chrome(options=opts)
		self.browser.get("about:blank")
		self.browser.get("https://www.tiktok.com/signup/phone-or-email/email")
		time.sleep(2)
		#csrf token where
		# try:
		# 	cookies = [
		# 		{"name":"MONITOR_DEVICE_ID", "value":"83f2a32c-e1bb-4f12-bb7d-738337ace68a","domain":"www.tiktok.com", ' httpOnly ' : True},
		# 		{"name":"MONITOR_WEB_ID", "value":"4dd6413e-0004-4295-90a8-3ca3f05b67ce","domain":"www.tiktok.com", ' httpOnly ' : True},
		# 		{"name":"odin_tt", "value":"4cbddea8615660cd4d8f2aac72020c88f81f84543414b9092e23b135438d9bce3c52b8b3d586719076c8965c91c10ee2db823e96577d92def744dd8261b49fc4dcb8119d446341430d6657d564722471","domain":"www.tiktok.com", ' httpOnly ' : True},
		# 		{"name":"passport_auth_status", "value":"d747cae4366730551d03dad13b7c4ea8","domain":"www.tiktok.com", ' httpOnly ' : True},
		# 		{"name":"passport_auth_status_ss", "value":"d747cae4366730551d03dad13b7c4ea8","domain":"www.tiktok.com", ' httpOnly ' : True}
		# 	]
			
		# 	for cookie in cookies:
		# 		self.browser.add_cookie(cookie)
		# 	print("cookies successfully added to browser!")
		# except exceptions.InvalidCookieDomainException as e:
		# 	print(e.msg)
			
		# self.browser = uc.Chrome(options = opts)
		self.zoho = zoho

	def send_keys_delay_random(self,element,keys,min_delay=0.05,max_delay=0.25):
		for key in keys:
			element.send_keys(key)
			time.sleep(random.uniform(min_delay,max_delay))

	def saveSuccessfulInfo(self, successList):
		f = open(os.getcwd() + "/emailListInformation "+ datetime.date.today() + ".csv", 'w')
		writer = csv.writer(f)
		writer.writerows(successList)
		#tiktok and linked gmail account info
		#tiktok user and password
		#gmail user and password
		f.close()
		return

	def get_successful_connect_cookies(self, url):
		self.browser.get(url)

		request_cookies_browser = self.browser.get_cookies()

		params = {'tt_csrftoken':requests.request(url=url)}
		s = requests.Session()

		c = [s.cookies.set(c['name'], c['value']) for c in request_cookies_browser]
		resp = s.post(url, params) #get successful 200 response

		#passing the cookie of the response to the browser
		dict_resp_cookies = resp.cookies.get_dict()
		response_cookies_browser = [{'name':name, 'value':value} for name, value in dict_resp_cookies.items()]
		c = [self.browser.add_cookie(c) for c in response_cookies_browser]
		#the browser now contains the cookies generated from the authentication    
	
	def tiktokAccountCreate(self):
		# for i in (0, len(self.csvdata)):
		url = "https://www.tiktok.com/signup/phone-or-email/email"
		self.browser.get(url)
		# self.get_successful_connect_cookies(url)

		self.browser.implicitly_wait(10)
		time.sleep(3560350)

		# <div type="error" class="	tiktok-1ucf5ae-DivDescription e18rms3f2">invalid csrf token</div>

		# input("Hanging")
		email = self.csvdata[0]

		#TODO: make random password generation
		# passw = randomPasswordGenerate()
		passw = "Backpack123$" #dummy password

		# booleans checking if input correctly
		e = False
		p = False
		m = False
		d = False
		y = False
		success = False

		while success == False: 
			try: 
				if not e:		
					print("inputting email")				
					WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.NAME, "email")))
					emailBox = self.browser.find_element(By.NAME, "email")
					print("email box found")
					emailBox.click()
					self.send_keys_delay_random(emailBox, email)
					e = True

				if not p:
					print("inputting password")				
					passwBox = self.browser.find_element(By.CSS_SELECTOR, "input[type = 'password']")
					passwBox.click()
					self.send_keys_delay_random(passwBox, passw)
					p = True

				if not m:
					month = WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[contains(text(), "Month")]')))
					print("selecting month")
					if month:
						self.browser.find_element(By.XPATH, '//*[contains(text(), "Month")]').click()
						#Randomize month
						self.browser.find_element(By.XPATH, '//*[contains(text(), "March")]').click()
						m = True
				
				if not d:
					day = WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[contains(text(), "Day")]')))
					print("selecting day")
					if day: 
						self.browser.find_element(By.XPATH, '//*[contains(text(), "Day")]').click()
						self.browser.find_element(By.XPATH, '//*[text() = "31"]').click()
						d = True

				if not y:
					year = WebDriverWait(self.browser, 20).until(ec.visibility_of_element_located((By.XPATH, '//*[contains(text(), "Year")]')))
					print("selecting year")
					if year:
						self.browser.find_element(By.XPATH, '//*[contains(text(), "Year")]').click()

						#randomize year selection
						randomInt = random.randint(1980, 2000)
						self.browser.find_element(By.XPATH, '//*[contains(text(), ' + str(randomInt) + ')]').click()
						y = True
				
				success = True
				print("success!")
			except Exception as e: 
				print("error!")
				self.browser.refresh()
				time.sleep(1)

		self.browser.find_element(By.XPATH, '//button[text() = "Send code"]').click()

		# Get the code
		tikTokCode = self.getRecentCode()
		print("found code: " + str(tikTokCode))

		#self.browser.close()
		self.browser.switch_to.window(self.browser.window_handles[0])
		time.sleep(5)
		codeBox = self.browser.find_element(By.XPATH, '//*[@placeholder = "Enter 6-digit code"]')
		self.send_keys_delay_random(codeBox, tikTokCode)
		self.browser.find_element(By.CSS_SELECTOR, "button[type = 'submit']").click()

		try:
			self.browser.find_element(By.XPATH, '//*[text() = "Skip"]').click()
		except Exception as e:
			print(e.msg)
		# qrcode = WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.XPATH, '//img')))
		# if(qrcode):
		# 	print("placeholder scan on qrcode")
			
		# self.saveSuccessfulInfo({email, passw})

	#Google Signin
	def googleSignIn(self):
		if self.zoho:
			self.zohoSignIn()
			zohoOTPCode = self.zohoSignIn()
					
			self.browser.switch_to.window(self.browser.window_handles[1])

			otpBox = self.browser.find_element(By.NAME, 'OTP')
			self.send_keys_delay_random(otpBox, zohoOTPCode)
			self.browser.find_element(By.ID, 'nextbtn').click()

		# self.browser.execute_script("window.open('https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin');") 
		# #proceed with new tab
		# self.browser.switch_to.window(self.browser.window_handles[1])

		# self.options.add_argument('user-data-dir=c:\Users\' username '\AppData\Local\Google\Chrome\User Data\');
		self.browser.execute_script("window.open('https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin');") 
		#proceed with new tab
		self.browser.switch_to.window(self.browser.window_handles[1])

		WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.XPATH, '//input[@id="identifierId"]')))
		gmailUserBox = self.browser.find_element(By.XPATH, '//input[@id="identifierId"]')
		self.send_keys_delay_random(gmailUserBox, self.email)
		gmailUserBox.send_keys(Keys.ENTER)

		WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.ID, 'identifierId')))
		gmailPasswBox = self.browser.find_element(By.NAME, 'password')
		self.send_keys_delay_random(gmailPasswBox, self.password)
		time.sleep(1)
		gmailPasswBox.send_keys(Keys.ENTER)
		print("signed into google!")

		print("Please wait a minute before the code is sent to your email")
		
		time.sleep(1)

		gmails = self.browser.find_elements(By.XPATH, '//*[@class="bog"]')
		while(True):
			for gmail in gmails:
				if "verification code" in gmail.text:
					print(gmail.text[:6])
					return str(gmail.text[:6])
			print("No code found!")
			time.sleep(5)
			self.browser.refresh()
		
	def yahooSignIn(self):
		self.browser.execute_script("window.open('https://login.yahoo.com/?.intl=us&.lang=en-US&src=ym&activity=mail-direct&pspid=159600001&done=https%3A%2F%2Fmail.yahoo.com%2Fd&add=1');") 
		#proceed with new tab
		self.browser.switch_to.window(self.browser.window_handles[1])

		WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.XPATH, '//input[@name="username"]')))
		yahooUserBox = self.browser.find_element(By.XPATH, '//input[@name="username"]')
		yahooUserBox.send_keys(self.send_keys_delay_random(self.email))
		yahooUserBox.send_keys(Keys.ENTER)

		WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.XPATH, '//input[@id = "login-passwd"]')))
		yahooPasswBox = self.browser.find_element(By.XPATH, '//input[@id = "login-passwd"]')
		yahooPasswBox.send_keys(self.send_keys_delay_random(self.password))
		time.sleep(1)
		yahooPasswBox.send_keys(Keys.ENTER)

		# WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.XPATH, "//span[text() = 'Continue']")))
		# continueBtn = self.browser.find_element(By.XPATH, "//span[text() = 'Continue']")
		# continueBtn.click()

		print("signed into yahoo!")

		yahooMails = self.browser.find_elements(By.XPATH, '//*[@data-test-id = "subject"]/a')
		while(True):
			for yahooMail in yahooMails:
				print(yahooMail.text)
				if "verification code" in yahooMail.text:
					print(yahooMail.text[:6])
					return str(yahooMail.text[:6])
			print("No code found!")
			time.sleep(5)
			self.browser.refresh()

	#Zoho Signin
	def zohoSignIn(self, email):
		self.browser.execute_script("window.open('https://accounts.zoho.com/signin?servicename=VirtualOffice&signupurl=https://www.zoho.com/mail/zohomail-pricing.html&serviceurl=https://mail.zoho.com', 'zohoSignIN');")
		#proceed with new tab
		self.browser.switch_to.window('zohoSignIN')

		WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.NAME, 'LOGIN_ID')))
		self.browser.find_element(By.NAME, 'LOGIN_ID').send_keys(self.send_keys_delay_random(email))
		self.browser.find_element(By.ID, 'nextbtn').click()   

	#Wait for Google Signin and grab code from email
	def getRecentCode(self):
		# stalling = input("stalling before google signin")
		if not self.logIn:
			if self.emailProvider == 'google':
				return self.googleSignIn()
			elif self.emailProvider == 'yahoo':
				return self.yahooSignIn()

	def main(self):
		# self.browser.maximize_window()
		self.tiktokAccountCreate()

	
if __name__ == "__main__":
	
	data = open("settings.json", "r+", encoding="utf8")
	jsondata = json.load(data)
	data.close()
	
	newChrome = My_Chrome(jsondata)
	newChrome.main()

	hangingStall = input("Hanging")