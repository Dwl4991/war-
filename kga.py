# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# import time

# # Setup WebDriver dengan webdriver-manager untuk ChromeDriver
# driver = webdriver.Chrome(ChromeDriverManager().install())

# # URL Google Form yang ingin kamu isi (ganti dengan URL form yang kamu gunakan)
# form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSd2KhKOkWDXqK9mDMZy5CUaUcZ3Arcw2HvIG_V3vkaWdrLukw/viewform?usp=sf_link'
# driver.get(form_url)

# # Tunggu beberapa detik agar halaman selesai dimuat
# time.sleep(3)

# # Field 1: Isi dengan "Putri Dewi"
# first_field = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[1]/div/div[1]/div/div[1]/input')
# first_field.send_keys("Putri Dewi")

# # Field 2: Multiple choice - Pilih pilihan ketiga
# second_choice = driver.find_element_by_xpath('//div[@role="radio" and @aria-label="//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div/span/div/div[3]/label/div/div[2]/div/span"]')
# second_choice.click()

# # Field 3: Multiple choice - Pilih pilihan pertama
# third_choice = driver.find_element_by_xpath('//div[@role="radio" and @aria-label="//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div/span/div/div[1]/label/div/div[2]/div/span"]')
# third_choice.click()

# # Field 4: Isi dengan "0"
# fourth_field = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[4]/div/div[1]/div/div[1]/input')
# fourth_field.send_keys("0")

# # Field 5: Multiple choice - Pilih pilihan pertama
# fifth_choice = driver.find_element_by_xpath('//div[@role="radio" and @aria-label="//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div/span/div/div[1]/label/div/div[2]/div/span"]')
# fifth_choice.click()

# # Field 6: Isi dengan "dx biasa"
# sixth_field = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[6]/div/div[1]/div/div[1]/input')
# sixth_field.send_keys("dx biasa")

# # Field 7: Isi dengan "0"
# seventh_field = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[7]/div/div[1]/div/div[1]/input')
# seventh_field.send_keys("0")

# # Klik tombol submit
# submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[8]/div[1]/div/div')
# submit_button.click()

# # Tunggu beberapa detik sebelum menutup browser
# time.sleep(3)

# # Tutup browser
# driver.quit()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Google Form URL
form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSd2KhKOkWDXqK9mDMZy5CUaUcZ3Arcw2HvIG_V3vkaWdrLukw/viewform?usp=sf_link'
driver.get(form_url)

# Wait for the form to load
wait = WebDriverWait(driver, 20)

# Fill out the form
import time
time.sleep(2)  # Add a 2-second delay before interacting with the first field
first_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='text']")))
first_field.send_keys("Putri Dewi")
# Select the third option in the second fielddriver.find_elements(By.CSS_SELECTOR, "div[role='radio']")[2].click()

# Select the first option in the third field
driver.find_elements(By.CSS_SELECTOR, "div[role='radio']")[2].click()

driver.find_elements(By.CSS_SELECTOR, "div[role='radio']")[3].click()

# Fill out the fourth field
driver.find_elements(By.CSS_SELECTOR, "input[type='text']")[1].send_keys("0")

# Select the first option in the fifth field
driver.find_elements(By.CSS_SELECTOR, "div[role='radio']")[6].click()

# Fill out the sixth field
driver.find_elements(By.CSS_SELECTOR, "input[type='text']")[2].send_keys("dxaasd biasa")

# Fill out the seventh field
driver.find_elements(By.CSS_SELECTOR, "input[type='text']")[3].send_keys("11110")

# Submit the form
submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='button']")))
submit_button.click()

try:
  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.freebirdFormviewerViewResponseConfirmationMessage")))
  print("Form successfully submitted!")
except:
  try:
      WebDriverWait(driver, 10).until(EC.url_contains("formResponse"))
      print("Form likely submitted - URL changed to response page.")
  except:
      print("Form submission could not be confirmed. Please check manually.")

driver.save_screenshot("form_submission_result.png")
print("Screenshot saved. Please check 'form_submission_result.png' to verify submission status.")

# Wait for a moment
time.sleep(3)

# Close the browser
driver.quit()