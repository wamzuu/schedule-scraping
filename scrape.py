# Importing necessary modules for web scraping and automation using Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from config import userName, password  # Separate module containing private login info
from time import sleep # Sleep module for adding delays



def scrape_data():
    # Defining the URLs for login and the schedule page of the website to be scraped
    login_url = 'https://kerasotes.movieteam.co/Account/Login?ReturnUrl=%2F'
    schedule_url = 'https://kerasotes.movieteam.co/Schedule'

    # Initializing a Chrome webdriver instance
    driver = webdriver.Chrome()

    # Opening the login URL in the Chrome webdriver
    driver.get(login_url)

    # Finding the username and password field using XPath and entering the details from the credentials module
    driver.find_element(By.XPATH, '//input[@name="userName"]').send_keys(userName)
    driver.find_element(By.XPATH, '//input[@name="password"]').send_keys(password)

    # Finding the login button field using XPath and clicking to log in
    driver.find_element(By.XPATH, '//button[@type="submit"]').click() 

    # Print check to see if login worked
    print('Logged In Successfully')
    sleep(1)

    # Open Schedule page and wait for it to load
    driver.get('https://kerasotes.movieteam.co/Schedule')
    sleep(7)

    # Click on the "My Schedule" tab
    element = driver.find_element(By.XPATH, '//div[@class="truncate ng-scope" and text()="My Schedule"]')
    element.click()
    
    sleep(10)

    # Wait for the table to be present
    table = WebDriverWait(driver,   10).until(EC.presence_of_element_located((By.ID, 'my-shifts')))

    # Get all the rows within the tbody
    rows = table.find_elements(By.TAG_NAME, 'tr')

    # Initialize an empty list to store the shift data
    shifts = []

    # Get the date headers
    date_headers = driver.find_elements(By.XPATH, '//tr/th[@class="cal-col shift-col init-hide ng-binding"]')

    # Iterate over each row
    for row in rows:
        # Find all td elements with the class 'shift-col'
        shift_columns = row.find_elements(By.CLASS_NAME, 'shift-col')
        for index, column in enumerate(shift_columns):
            # Find all divs with the class 'cell-container' within the current td
            shift_containers = column.find_elements(By.CLASS_NAME, 'cell-container')
            for container in shift_containers:
                try:
                    # Try to find the title and time elements within the cell-container
                    job_name_element = container.find_element(By.CLASS_NAME, 'title')
                    time_element = container.find_element(By.CLASS_NAME, 'time')
                    # Extract the job name, start time, end time, and date
                    job_name = job_name_element.text
                    start_time, end_time = time_element.text.split(' - ')
                    raw_date = date_headers[index].text if index < len(date_headers) else ''
                    # Remove the day of the week abbreviation and leading space
                    cleaned_date = ' '.join(raw_date.split()[1:])
                    # Append the extracted data to the shifts list
                    shifts.append({'date': cleaned_date, 'job_name': job_name, 'start_time': start_time, 'end_time': end_time})
                except NoSuchElementException:
                    # If the required elements are not found, append an empty dictionary
                    shifts.append({})

    # Print the shifts data
    print("Scraped shifts:")
    for shift in shifts:
        print(shift)

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(shifts)

    # Define the CSV file path
    csv_file_path = 'raw_data.csv'

    # Write the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)

    print(f"Shift data has been written to {csv_file_path}")
    if True:
        pass