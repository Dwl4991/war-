from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup WebDriver dengan webdriver-manager untuk ChromeDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# URL Google Form yang ingin kamu isi
form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSd2KhKOkWDXqK9mDMZy5CUaUcZ3Arcw2HvIG_V3vkaWdrLukw/viewform?usp=sf_link'
driver.get(form_url)

# Tunggu hingga field pertama muncul
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div/div[2]/div[1]/div/div[1]/div/div[1]/input')))
# Field 1: Isi dengan "Putri Dewi"
first_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div/div[2]/div[1]/div/div[1]/div/div[1]/input')
first_field.send_keys("Putri Dewi")

# Field 2: Multiple choice - Pilih pilihan ketiga
second_choice = driver.find_element(By.XPATH, '(//div[@role="radio"])[3]')  # Asumsi pilihan ketiga adalah yang ke-3
second_choice.click()

# Field 3: Multiple choice - Pilih pilihan pertama
third_choice = driver.find_element(By.XPATH, '(//div[@role="radio"])[1]')  # Asumsi pilihan pertama adalah yang ke-1
third_choice.click()

# Field 4: Isi dengan "0"
fourth_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div/div[2]/div[4]/div/div[1]/div/div[1]/input')
fourth_field.send_keys("0")

# Field 5: Multiple choice - Pilih pilihan pertama
fifth_choice = driver.find_element(By.XPATH, '(//div[@role="radio"])[1]')  # Asumsi pilihan pertama adalah yang ke-1
fifth_choice.click()

# Field 6: Isi dengan "dx biasa"
sixth_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div/div[2]/div[6]/div/div[1]/div/div[1]/input')
sixth_field.send_keys("dx biasa")

# Field 7: Isi dengan "0"
seventh_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div/div[2]/div[7]/div/div[1]/div/div[1]/input')
seventh_field.send_keys("0")

# Klik tombol submit
submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div/div[2]/div[8]/div[1]/div/div')
submit_button.click()

# Tunggu beberapa detik sebelum menutup browser
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div/div[2]/div[9]')))  # Tunggu hingga submit berhasil

# Tutup browser
driver.quit()
