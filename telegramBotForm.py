# import logging
# from datetime import datetime
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import Updater, ApplicationBuilder,CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
# from cobaBaca import schedule_form_submission

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# departments = ["IKGA", "BM", "Periodonsia", "Prostodonsia", "Konservasi", "IPM", "Ortodonsia"]
# shifts = ["1", "2", "3", "4", "5"]

# def start(update: Update, context: CallbackContext) -> None:
#     keyboard = [[InlineKeyboardButton(dept, callback_data=f"dept_{dept}")] for dept in departments]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     update.message.reply_text('Please choose a department:', reply_markup=reply_markup)

# def button(update: Update, context: CallbackContext) -> None:
#     query = update.callback_query
#     query.answer()

#     if query.data.startswith("dept_"):
#         department = query.data.split("_")[1]
#         context.user_data['department'] = department
#         keyboard = [[InlineKeyboardButton(shift, callback_data=f"shift_{shift}")] for shift in shifts]
#         reply_markup = InlineKeyboardMarkup(keyboard)
#         query.edit_message_text(text=f"Selected department: {department}\nNow choose a shift:", reply_markup=reply_markup)

#     elif query.data.startswith("shift_"):
#         shift = query.data.split("_")[1]
#         context.user_data['shift'] = shift
#         query.edit_message_text(text=f"Selected shift: {shift}\nPlease enter your desired submission time (HH:MM):")

# def submission_time(update: Update, context: CallbackContext) -> None:
#     try:
#         submission_time = datetime.strptime(update.message.text, "%H:%M").time()
#         department = context.user_data.get('department')
#         shift = context.user_data.get('shift')
#         schedule_form_submission('1', submission_time, department)
#         update.message.reply_text(f"Submission scheduled for department: {department}, shift: {shift} at {submission_time}")
#     except ValueError:
#         update.message.reply_text("Invalid time format. Please enter the time in HH:MM format.")



# def main():
#     # Replace 'YOUR_TOKEN' with your actual Telegram bot token
#     application = ApplicationBuilder().token("7620722312:AAFru3845VhDRj3dz-691ZSDjMLZYv6xlhE").build()

#     application.add_handler(CommandHandler('start', start))
#     application.add_handler(CallbackQueryHandler(button))
#     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, submission_time))

#     application.run_polling()

# if __name__ == '__main__':
#     main()
# import logging
# from datetime import datetime
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
# from cobaBaca import schedule_form_submission

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# departments = ["IKGA", "BM", "Periodonsia", "Prostodonsia", "Konservasi", "IPM", "Ortodonsia"]
# shifts = ["1", "2", "3", "4", "5"]

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     keyboard = [[InlineKeyboardButton(dept, callback_data=f"dept_{dept}")] for dept in departments]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.message.reply_text('Please choose a department:', reply_markup=reply_markup)

# async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     query = update.callback_query
#     await query.answer()

#     if query.data.startswith("dept_"):
#         department = query.data.split("_")[1]
#         context.user_data['department'] = department
#         keyboard = [[InlineKeyboardButton(shift, callback_data=f"shift_{shift}")] for shift in shifts]
#         reply_markup = InlineKeyboardMarkup(keyboard)
#         await query.edit_message_text(text=f"Selected department: {department}\nNow choose a shift:", reply_markup=reply_markup)

#     elif query.data.startswith("shift_"):
#         shift = query.data.split("_")[1]
#         context.user_data['shift'] = shift
#         await query.edit_message_text(text=f"Selected shift: {shift}\nPlease enter your desired submission time (HH:MM):")

# async def submission_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     try:
#         submission_time = datetime.strptime(update.message.text, "%H:%M").time()
#         department = context.user_data.get('department')
#         shift = context.user_data.get('shift')
#         schedule_form_submission('1', submission_time, department)
#         await update.message.reply_text(f"Submission scheduled for department: {department}, shift: {shift} at {submission_time}")
#     except ValueError:
#         await update.message.reply_text("Invalid time format. Please enter the time in HH:MM format.")

# def main():
#     # Replace 'YOUR_TOKEN' with your actual Telegram bot token
#     application = ApplicationBuilder().token("7620722312:AAFru3845VhDRj3dz-691ZSDjMLZYv6xlhE").build()

#     application.add_handler(CommandHandler('start', start))
#     application.add_handler(CallbackQueryHandler(button))
#     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, submission_time))

#     application.run_polling()

# if __name__ == '__main__':
#     main()


import logging
import time
import random
from datetime import datetime
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define forms and departments
forms = {
    '1': {
        'name': 'Percobaan Form Cancel',
        'url': 'https://docs.google.com/forms/d/e/1FAIpQLSei4uL_d_nBeDFGGmU743XILpKuklo0_tzmZYAZLp9j4HFahQ/viewform?vc=0&c=0&w=1&flr=0',
        'field_mapping': {
            "nama": "Putri Dewi Angelina",
            "Angkatan": "3",
            "Departemen": "IKGA",
            "Tindakan": "Selasa shift 3",
            "Jenis DU": "Non Aerosol",
            "hari kerja": "Kamis",
            "shift": "1"
        },
        'field_input': ['text_input', 'text_input', 'radio', 'text_input', 'radio', 'radio', 'radio']
    },
}

departments = ["IKGA", "BM", "Periodonsia", "Prostodonsia", "Konservasi", "IPM", "Ortodonsia"]
shifts = ["1", "2", "3", "4", "5"]

# Function to introduce random delay
def random_delay(min_seconds=1, max_seconds=5):
    time.sleep(random.uniform(min_seconds, max_seconds))

# Function to fill the form
def fill_form(url, field_mapping, field_input, selected_department):
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
                if key.lower() == "departemen":
                    value = selected_department
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

# Function to submit the form
def submit_form(driver):
    try:
        submit_button = driver.find_element(By.CSS_SELECTOR, "div[role='button']")
        submit_button.click()
        logging.info("Form submitted successfully.")
    except Exception as e:
        logging.error(f"Failed to submit form: {str(e)}")
        driver.save_screenshot("form_submission_failure.png")
    finally:
        driver.quit()

# Function to schedule form submission
def schedule_form_submission(form_id, submission_time, selected_department):
    form = forms[form_id]
    driver = fill_form(form['url'], form['field_mapping'], form['field_input'], selected_department)

    submission_datetime = datetime.combine(datetime.now(), submission_time)

    while datetime.now() < submission_datetime:
        time.sleep(0.01)

    submit_form(driver)

# Telegram bot handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton(dept, callback_data=f"dept_{dept}")] for dept in departments]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose a department:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data.startswith("dept_"):
        department = query.data.split("_")[1]
        context.user_data['department'] = department
        keyboard = [[InlineKeyboardButton(shift, callback_data=f"shift_{shift}")] for shift in shifts]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"Selected department: {department}\nNow choose a shift:", reply_markup=reply_markup)

    elif query.data.startswith("shift_"):
        shift = query.data.split("_")[1]
        context.user_data['shift'] = shift
        await query.edit_message_text(text=f"Selected shift: {shift}\nPlease enter your desired submission time (HH:MM):")
async def submission_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        submission_time = datetime.strptime(update.message.text, "%H:%M").time()
        department = context.user_data.get('department')
        shift = context.user_data.get('shift')
        schedule_form_submission('1', submission_time, department)
        await update.message.reply_text(f"Submission scheduled for department: {department}, shift: {shift} at {submission_time}")
    except ValueError:
        await update.message.reply_text("Invalid time format. Please enter the time in HH:MM format.")

def main():
    # Replace 'YOUR_TOKEN' with your actual Telegram bot token
    application = ApplicationBuilder().token("7620722312:AAFru3845VhDRj3dz-691ZSDjMLZYv6xlhE").build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, submission_time))

    application.run_polling()

if __name__ == '__main__':
    main()

