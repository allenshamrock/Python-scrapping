from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import os

# Initialize ChromeDriver using WebDriver Manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Website URL
driver.get("http://quotes.toscrape.com/")

tag_lists = []
data_list = []

# Scraping loop
while True:
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    quotes = soup.find_all('div', class_='quote')

    if not quotes:
        print("No quotes found on the current page. Exiting the loop.")
        break

    for quote in quotes:
        description = quote.find('span', class_='text').get_text()
        author = quote.find('small', class_='author').get_text()
        tags = quote.find_all('a', class_='tag')
        tag_list = [tag.get_text() for tag in tags]
        data_list.append([description, author, ' '.join(tag_list)])

    # Check for the "Next" page link
    next_link = soup.find('li', class_='next')
    if next_link:
        next_page_url = next_link.find('a')['href']
        if not next_page_url.startswith('http'):
            base_url = 'http://quotes.toscrape.com'
            next_page_url = base_url + next_page_url

        driver.get(next_page_url)
    else:
        print("No 'Next' link found. Exiting the loop.")
        break

# Close the browser
driver.quit()

# Correct CSV file path
directory = r"/home/allen/Desktop/python-scraping"
os.makedirs(directory, exist_ok=True)  
csv_file = os.path.join(directory, 'quotes_data.csv')

# Write data to CSV
with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Author', 'Quote', 'Tags'])
    for item in data_list:
        csv_writer.writerow([item[1], item[0], item[2]])

print(f'Data has been successfully written to {csv_file}')
