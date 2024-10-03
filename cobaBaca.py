import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

forms = {
    '1': {
        'name': 'Form WAR DU PERIO 82',
        'url': 'https://docs.google.com/forms/d/e/1FAIpQLSejgwHKHkbwZzWs9gU8iFvucIVu1i7yJRi1ddw2zcj3CwEkRA/viewform',
        'field_mapping': {
            "nama": "Devaaa",
            "kelompok": "1",
            "rencana kerja": "Scalling",
            "pilihan 1": "Senin Shift 2",
            "pilihan 2": "Kamis shift1",
            "sudah berapa kali": "1"
        },
        'field_input': ['text_input', 'radio', 'text_input', 'radio', 'radio', 'text_input']
    },
    '2': {
        'name': 'Form WAR DU KGA KOAS 82',
        'url': 'https://docs.google.com/forms/d/e/1FAIpQLSd2KhKOkWDXqK9mDMZy5CUaUcZ3Arcw2HvIG_V3vkaWdrLukw/viewform',
        'field_mapping': {
            "nama": "DU KGA",
            "kloter kerumahsakitan": "kloter 2",
            "pilihan 1 kerja shift": "Jum'at Shift 1 (08.00 - 10.00)",
            "total kerja": "25",
            "pilihan 2": "Senin Shift 1 (08.00 - 10.00)",
            "tindakan": "lalala",
            "Akumulasi DU Angkatan": "100"
        },
        'field_input': ['text_input', 'radio', 'radio', 'text_input', 'radio', 'text_input', 'text_input']
    },
    '3': {
        'name': 'Form WAR DU PROSTHO 82',
        'url': 'https://docs.google.com/forms/d/e/1FAIpQLSfzviUqHdnod2r2eW7Wk2PriGxDRVjRyg6u2TklAjY79vfkgA/viewform',
        'field_mapping': {
            "operator": 'Deva Mahendra Prostoh',
            "Klinik": "Non Aerosol",
            "tindakan": "Pencetakan",
            "Requirement": "GTL",
            "Dosen Pembimbing": "Dr. drg. Titik Ismiyati, MS., Sp.Pros(K)",
            "hari kerja": "kamis",
            "shift": 'Shift 2 (10.00 - 12.00)'
        },
        'field_input': ['text_input', 'radio', 'text_input', 'radio', 'radio', 'radio', 'radio']
    },
    '4': {
        'name': 'Form WAR DU KONSERVASI 82',
        'url': 'https://docs.google.com/forms/d/e/1FAIpQLSf3Ag2Bx5f4SWX7Oh6cGXzdlBS7FztcSHk8uA5c3Aj_xpHtqA/viewform',
        'field_mapping': {
            "nama": "madya kurnia",
            "Kelompok kerumahsakitan": '2',
            "Rencana KErja": "Restorasi RK Kelas 2",
            "Pilihan 1": "Kamis Shift 1 (08.00 - 11.00)",
            "Pilihan 2": "Selasa Shift 2 (11.00 -14.00)",
            "Akumulasi DU KONSERVASI": "20"
        },
        'field_input': ["text_input", "radio", 'text_input', "radio", "radio", "text_input"]
    }
}

def random_delay(min_seconds=1, max_seconds=5):
    time.sleep(random.uniform(min_seconds, max_seconds))

def parse_form(url, field_mapping, field_input):
    options = uc.ChromeOptions()
    options.add_argument("--user-data-dir=./chrome_profile")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

    driver = uc.Chrome(options=options)
    driver.get(url)
    random_delay()

    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[role='listitem']")))
    except Exception as e:
        logging.error(f"Failed to load form: {str(e)}")
        driver.save_screenshot("form_load_failure.png")
        driver.quit()
        return

    random_delay(0.1, 0.7)

    form_items = driver.find_elements(By.CSS_SELECTOR, "div[role='listitem']")

    title_selectors = [
        ".freebirdFormviewerComponentsQuestionBaseHeader",
        ".freebirdFormviewerComponentsQuestionBaseTitle",
        "div[role='heading']"
    ]

    for index, item in enumerate(form_items, start=1):
        try:
            title = next((item.find_element(By.CSS_SELECTOR, selector).text for selector in title_selectors if item.find_elements(By.CSS_SELECTOR, selector)), "Unable to find title")
            
            input_type = "Text Input" if item.find_elements(By.CSS_SELECTOR, "input[type='text']") else "Radio Buttons"
            logging.info(f"Field {index}: {title} - Type: {input_type}")
            
            for key, value in field_mapping.items():
                if key.lower() in title.lower():
                    if input_type == "Text Input":
                        input_field = item.find_element(By.CSS_SELECTOR, "input[type='text']")
                        input_field.send_keys(value)
                        logging.info(f"Filled '{key}' field with '{value}'")
                    else:  # Radio Buttons
                        options = item.find_elements(By.CSS_SELECTOR, '[role="radio"]')
                        for option in options:
                            option_text = option.get_attribute("aria-label") or option.text
                            if value.lower() in option_text.lower():
                                driver.execute_script("arguments[0].click();", option)
                                logging.info(f"Selected '{option_text}' for '{key}'")
                                break
                        else:
                            logging.warning(f"No matching option found for '{key}' with value '{value}'")
                    break
            
            if input_type == "Radio Buttons":
                options = [option.text for option in item.find_elements(By.CSS_SELECTOR, "label[role='radio']")]
                for i, option in enumerate(options, start=1):
                    logging.info(f"  Option {i}: {option}")
            
            logging.info("")
        except Exception as e:
            logging.error(f"Field {index}: Unable to parse - Error: {str(e)}")
            logging.info("")

    # Attempt to submit the form
    try:
        submit_button = driver.find_element(By.CSS_SELECTOR, "div[role='button']")
        submit_button.click()
        logging.info("Form submitted successfully.")
    except Exception as e:
        logging.error(f"Failed to submit form: {str(e)}")
        driver.save_screenshot("form_submission_failure.png")

    driver.quit()