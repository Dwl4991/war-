from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup WebDriver dengan webdriver-manager untuk ChromeDriver
driver = webdriver.Chrome(ChromeDriverManager().install())

# URL Google Form yang ingin kamu isi (ganti dengan URL form yang kamu gunakan)
form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSd2KhKOkWDXqK9mDMZy5CUaUcZ3Arcw2HvIG_V3vkaWdrLukw/viewform?usp=sf_link'
driver.get(form_url)

# Tunggu beberapa detik agar halaman selesai dimuat
time.sleep(3)

# Field 1: Isi dengan "Putri Dewi"
first_field = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[1]/div/div[1]/div/div[1]/input')
first_field.send_keys("Putri Dewi")

# Field 2: Multiple choice - Pilih pilihan ketiga
second_choice = driver.find_element_by_xpath('//div[@role="radio" and @aria-label="//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div/span/div/div[3]/label/div/div[2]/div/span"]')
second_choice.click()

# Field 3: Multiple choice - Pilih pilihan pertama
third_choice = driver.find_element_by_xpath('//div[@role="radio" and @aria-label="//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div/span/div/div[1]/label/div/div[2]/div/span"]')
third_choice.click()

# Field 4: Isi dengan "0"
fourth_field = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[4]/div/div[1]/div/div[1]/input')
fourth_field.send_keys("0")

# Field 5: Multiple choice - Pilih pilihan pertama
fifth_choice = driver.find_element_by_xpath('//div[@role="radio" and @aria-label="//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div/span/div/div[1]/label/div/div[2]/div/span"]')
fifth_choice.click()

# Field 6: Isi dengan "dx biasa"
sixth_field = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[6]/div/div[1]/div/div[1]/input')
sixth_field.send_keys("dx biasa")

# Field 7: Isi dengan "0"
seventh_field = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[7]/div/div[1]/div/div[1]/input')
seventh_field.send_keys("0")

# Klik tombol submit
submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div[2]/div[8]/div[1]/div/div')
submit_button.click()

# Tunggu beberapa detik sebelum menutup browser
time.sleep(3)

# Tutup browser
driver.quit()
