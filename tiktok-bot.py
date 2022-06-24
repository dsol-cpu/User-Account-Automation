import os
import datetime
import time
import random

from selenium import webdriver
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

	def __init__(self, jsondata, csvdata=[], zoho=False):

		self.csvdata = csvdata
		self.email = jsondata["mainEmail"]
		self.password = jsondata["password"]
		self.logIn = False

		#TODO: turn off the SameSite cookie for lastmx
		opts = Options()
		opts.add_argument("user-agent=Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41")
		self.browser = uc.Chrome(options = opts)
		self.browser.delete_all_cookies()
		
		self.zoho = zoho

	def saveSuccessfulInfo(self, successList):
		f = open(os.getcwd() + "/emailListInformation "+ datetime.date.today() + ".csv", 'w')
		writer = csv.writer(f)
		writer.writerows(successList)
		#tiktok and linked gmail account info
		#tiktok user and password
		#gmail user and password
		f.close()
		return

	def tiktokAccountCreate(self):
		# for i in (0, len(self.csvdata)):
		self.browser.get("https://www.tiktok.com/signup/phone-or-email/email")
		self.browser.implicitly_wait(10)
		time.sleep(2)

		#csrf token where

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
					self.browser.find_element(By.NAME, "email").send_keys(email)
					e = True

				if not p:
					print("inputting password")				
					self.browser.find_element(By.CSS_SELECTOR, "input[type = 'password']").send_keys(passw)
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
				pass

		self.browser.find_element(By.XPATH, '//button[text() = "Send code"]').click()

		# Get the code
		tikTokCode = self.getRecentCode()
		print("found code: " + str(tikTokCode))

		#self.browser.close()
		self.browser.switch_to.window(self.browser.window_handles[0])
		time.sleep(5)
		self.browser.find_element(By.XPATH, '//*[@placeholder = "Enter 6-digit code"]').send_keys(tikTokCode)
		self.browser.find_element(By.CSS_SELECTOR, "button[type = 'submit']").click()

		qrcode = WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.XPATH, '//img')))
		if(qrcode):
			print("placeholder scan")
			
		

		# self.saveSuccessfulInfo({email, passw})
 
	#Google Signin
	def googleSignIn(self):
		if self.zoho:
			self.zohoSignIn()
			zohoOTPCode = self.zohoSignIn()
					
			self.browser.switch_to.window(self.browser.window_handles[1])

			self.browser.find_element(By.NAME, 'OTP').send_keys(zohoOTPCode)
			self.browser.find_element(By.ID, 'nextbtn').click()

		# self.browser.execute_script("window.open('https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin');") 
		# #proceed with new tab
		# self.browser.switch_to.window(self.browser.window_handles[1])
		
		self.browser.execute_script("window.open('https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin');") 
		#proceed with new tab
		self.browser.switch_to.window(self.browser.window_handles[1])

		WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.XPATH, '//input[@id="identifierId"]')))
		gmailUserBox = self.browser.find_element(By.XPATH, '//input[@id="identifierId"]')
		gmailUserBox.send_keys(self.email)
		gmailUserBox.send_keys(Keys.ENTER)

		WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.ID, 'identifierId')))
		gmailPasswBox = self.browser.find_element(By.NAME, 'password')
		gmailPasswBox.send_keys(self.password)
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
		gmailUserBox = self.browser.find_element(By.XPATH, '//input[@name="username"]')
		gmailUserBox.send_keys(self.email)
		gmailUserBox.send_keys(Keys.ENTER)

		WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.XPATH, '//input[@id = "login-passwd"]')))
		gmailPasswBox = self.browser.find_element(By.XPATH, '//input[@id = "login-passwd"]')
		gmailPasswBox.send_keys(self.password)
		time.sleep(1)
		gmailPasswBox.send_keys(Keys.ENTER)
		print("signed into google!")

		pass

	#Zoho Signin
	def zohoSignIn(self, email):
		self.browser.execute_script("window.open('https://accounts.zoho.com/signin?servicename=VirtualOffice&signupurl=https://www.zoho.com/mail/zohomail-pricing.html&serviceurl=https://mail.zoho.com', 'zohoSignIN');")
		#proceed with new tab
		self.browser.switch_to.window('zohoSignIN')

		WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.NAME, 'LOGIN_ID')))
		self.browser.find_element(By.NAME, 'LOGIN_ID').send_keys(email)
		self.browser.find_element(By.ID, 'nextbtn').click()   

	#Wait for Google Signin and grab code from email
	def getRecentCode(self):
		# stalling = input("stalling before google signin")
		if not self.logIn:
			return self.googleSignIn()


	def main(self):
		# self.browser.maximize_window()
		self.tiktokAccountCreate()

	
if __name__ == "__main__":

	data = open("settings.json", "r+", encoding="utf8")
	jsondata = json.load(data)
	data.close()
	csvdata = []

	with open(os.getcwd() + '/emails.csv', mode ='r') as file:
		# reading the CSV file
		csvFile = csv.reader(file)

		# displaying the contents of the CSV file
		for row in csvFile:
			csvdata.append(row)

	newChrome = My_Chrome(jsondata, csvdata)
	newChrome.main()

	hangingStall = input("Hanging")