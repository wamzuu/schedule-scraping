from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

url = 'https://kerasotes.movieteam.co/Account/Login?ReturnUrl=%2F'

driver = webdriver.Chrome()
driver.get(url)

driver.find_element(By.CLASS_NAME, 'userName').send_keys()
driver.find_element(By.CLASS_NAME, 'password').send_keys()
login = driver.find_element(By.XPATH, '//button[@type="submit"]')
login.click()