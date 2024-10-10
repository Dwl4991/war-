import time
import schedule
import logging
from datetime import datetime, timedelta
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
	# 34.101.225.88
    # alert-rush-437514-b6
forms = {
    '1': {
        'name': 'Percobaan Form Cancel ',
        'url': 'https://docs.google.com/forms/d/e/1FAIpQLSei4uL_d_nBeDFGGmU743XILpKuklo0_tzmZYAZLp9j4HFahQ/viewform?vc=0&c=0&w=1&flr=0',
        'submission_day': 'thursday',
        'submission_time': '23:54',
        'field_mapping': {
            "nama": "Putri Dewi Angelina Coba",
            "Angkatan": "3",
            "Departemen": "BM",
            "Tindakan": "Selasa shift 3",
            "Jenis DU": "Aerosol",
            "hari kerja": "Rabu",
            "shift": "1"
        },
        'field_input': ['text_input', 'text_input','radio','text_input',  'radio', 'radio', 'radio']
    },
}
# forms = {
#     '1': {
#         'name': 'Form WAR DU PERIO 82 ',
#         'url': 'https://docs.google.com/forms/d/e/1FAIpQLSdXx_sefHEBnQi3EjO_eqVJEdj9AXeh2BxDSmES8JHmdRvN5A/viewform',
#         'submission_day': 'saturday',
#         'submission_time': '09:05',
#         'field_mapping': {
#             "nama": "Putri Dewi",
#             "kelompok kerumahsakitan": "3",
#             "rencana kerja": "Scalling Uss",
#             "pilihan 1": "Selasa shift 3",
#             "pilihan 2": "Senin shift 2",
#             "sudah berapa kali": "0"
#         },
#         'field_input': ['text_input', 'radio', 'text_input', 'radio', 'radio', 'text_input']
#     },
#     '2': {
#         'name': 'Form WAR DU KGA KOAS 82',
#         'url': 'https://docs.google.com/forms/d/e/1FAIpQLSc6UciRDNTe6vHwgcgBBN9yzc6N1C-8vDVkziMI2a9woq6OSA/viewform',
#         'submission_day':'saturday',
#         'submission_time':'09:10',
#         'field_mapping': {
#             "nama": "Putri Dewi",
#             "kloter kerumahsakitan": "Kloter 3",
#             "pilihan 1 kerja shift": "Senin Shift 1 (08.00 - 10.00)",
#             "total kerja": "0",
#             "pilihan 2": "Jum'at Shift 1 (08.00 - 10.00)",
#             "tindakan": "DX",
#             "Akumulasi DU Angkatan": "0"
#         },
#         'field_input': ['text_input', 'radio', 'radio', 'text_input', 'radio', 'text_input', 'text_input']
#     },
#     '3': {
#         'name': 'Form WAR DU PROSTHO 82',
#         'url': 'https://docs.google.com/forms/d/e/1FAIpQLSeymzMTOC-FYBgyr5kapkTxzalXCZtE8CWwbGICibW0Z1WHDw/viewform',
#         'submission_day':'saturday',
#         'submission_time':'09:20',
#         'field_mapping': {
#             "operator": 'Putri Dewi',
#             "Klinik": "Non Aerosol",
#             "tindakan": "Konsultasi GTC",
#             "Requirement": "GTC",
#             "Dosen Pembimbing": "drg. Pramudya Aditama, MDSc",
#             "hari kerja": "Jumat",
#             "shift": 'Shift 2 (10.00 - 12.00)'
#         },
#         'field_input': ['text_input', 'radio', 'text_input', 'radio', 'radio', 'radio', 'radio']
#     },
#     '4': {
#         'name': 'Form WAR DU KONSERVASI 82',
#         'url': 'https://docs.google.com/forms/d/e/1FAIpQLSeFGvuNImU7dlQ9aqBd0q2cz-rymqA1medBYLS-CTcPhBEI9Q/viewform',
#         'submission_day':'saturday',
#         'submission_time':'09:25',
#         'field_mapping': {
#             "nama": "Putri Dewi",
#             "Kelompok kerumahsakitan": '3',
#             "Rencana KErja": "Restorasi RK Kelas I",
#             "Pilihan 1": "Selasa Shift 2 (11.00 -14.00)",
#             "Pilihan 2": "Kamis Shift 2 (11.00 -14.00)",
#             "Akumulasi DU KONSERVASI": "20"
#         },
#         'field_input': ["text_input", "radio", 'text_input', "radio", "radio", "text_input"]
#     }
# }
def random_delay(min_seconds=1, max_seconds=5):
    time.sleep(random.uniform(min_seconds, max_seconds))

def fill_form(url, field_mapping, field_input):
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

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

    return driver  # Return the driver to keep the session open

def submit_form(driver):
    # Attempt to submit the form
    try:
        submit_button = driver.find_element(By.CSS_SELECTOR, "div[role='button']")
        submit_button.click()
        logging.info("Form submitted successfully.")
    except Exception as e:
        logging.error(f"Failed to submit form: {str(e)}")
        driver.save_screenshot("form_submission_failure.png")
    finally:
        driver.quit()

def schedule_form_submission(form_id):
    form = forms[form_id]
    driver = fill_form(form['url'], form['field_mapping'], form['field_input'])

    # Calculate the exact submission time
    submission_time = datetime.strptime(form['submission_time'], "%H:%M")
    submission_datetime = datetime.combine(datetime.now(), submission_time.time())

    # Adjust the submission time to 1 second before the desired time
    submission_datetime -= timedelta(seconds=0.01)

    # Wait until the adjusted submission time
    while datetime.now() < submission_datetime:
        time.sleep(0.01)  # Use a smaller sleep interval for better precision

    submit_form(driver)

def schedule_submissions():
    for form_id, form in forms.items():
        # Schedule the form filling 1 minute and 1 second before the submission time
        submission_time = datetime.strptime(form['submission_time'], "%H:%M")
        fill_time = (submission_time - timedelta(minutes=1, seconds=1)).strftime("%H:%M:%S")
        getattr(schedule.every(), form['submission_day']).at(fill_time).do(schedule_form_submission, form_id)
        # schedule.every(3).minutes.do(schedule_form_submission, form_id)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    schedule_submissions()