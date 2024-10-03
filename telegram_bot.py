import logging
import signal
import threading
import time
from datetime import datetime, timedelta
import calendar

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler, CommandHandler,
                          filters, MessageHandler, ApplicationBuilder)

from cobaBaca import parse_form, forms
import schedule

# Replace with your actual bot token
BOT_TOKEN = '7620722312:AAFru3845VhDRj3dz-691ZSDjMLZYv6xlhE'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

application = ApplicationBuilder().token(BOT_TOKEN).build()

scheduled_tasks = {}
stop_flag = threading.Event()

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Welcome! Use /fill_form to start filling a form.")

async def fill_form(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton(form_data['name'], callback_data=f"form_{form_number}")]
        for form_number, form_data in forms.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose a form to fill:", reply_markup=reply_markup)

async def form_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    form_number = query.data.split("_")[1]
    if form_number in forms:
        context.user_data['form_number'] = form_number
        await query.message.reply_text(f"You've chosen {forms[form_number]['name']}. Please choose a date for submission:")
        await show_calendar(update, context)
    else:
        await query.message.reply_text("Invalid form number. Please choose again.")

async def show_calendar(update: Update, context: CallbackContext, year=None, month=None) -> None:
    now = datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month

    keyboard = []
    for week in calendar.monthcalendar(year, month):
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(" ", callback_data="ignore"))
            else:
                row.append(InlineKeyboardButton(str(day), callback_data=f"day_{year}_{month}_{day}"))
        keyboard.append(row)

    keyboard.append([
        InlineKeyboardButton("<", callback_data=f"prev_{year}_{month}"),
        InlineKeyboardButton(">", callback_data=f"next_{year}_{month}")
    ])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(f"Select a date: {calendar.month_name[month]} {year}", reply_markup=reply_markup)

async def calendar_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data

    try:
        if data.startswith("day_"):
            _, year, month, day = map(int, data.split("_")[1:])
            selected_date = datetime(year, month, day)
            context.user_data['submit_date'] = selected_date
            await query.message.reply_text(f"You selected {selected_date.strftime('%Y-%m-%d')}. Please enter the time in HH:MM format:")
            context.user_data['waiting_for_time'] = True
        elif data.startswith("prev_"):
            _, year, month = map(int, data.split("_")[1:])
            prev_month = datetime(year, month, 1) - timedelta(days=1)
            await show_calendar(update, context, prev_month.year, prev_month.month)
        elif data.startswith("next_"):
            _, year, month = map(int, data.split("_")[1:])
            next_month = datetime(year, month, 28) + timedelta(days=4)
            await show_calendar(update, context, next_month.year, next_month.month)
        else:
            await query.answer()
    except ValueError as e:
        logging.error(f"Error processing calendar data: {data} - {str(e)}")
        await query.answer("An error occurred while processing your selection. Please try again.")

async def message_handler(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('waiting_for_time'):
        try:
            submit_time = datetime.strptime(update.message.text, "%H:%M").time()
            submit_datetime = datetime.combine(context.user_data['submit_date'], submit_time)
            if submit_datetime <= datetime.now():
                await update.message.reply_text("Please choose a future time.")
                return

            form_number = context.user_data['form_number']
            form_data = forms[form_number]
            scheduled_tasks[form_number] = schedule.every().day.at(submit_datetime.strftime("%H:%M")).do(submit_form, form_number, update.message.chat_id)
            
            await update.message.reply_text(f"Form {form_number} scheduled for submission at {submit_datetime.strftime('%Y-%m-%d %H:%M')}")
            context.user_data['waiting_for_time'] = False
        except ValueError:
            await update.message.reply_text("Invalid time format. Please use HH:MM")

def submit_form(form_number, chat_id):
    form_data = forms[form_number]
    try:
        parse_form(form_data['url'], form_data['field_mapping'], form_data['field_input'])
        application.bot.send_message(chat_id, f"Form {form_number} submitted successfully!")
    except Exception as e:
        application.bot.send_message(chat_id, f"Error submitting Form {form_number}: {str(e)}")
    
    # Remove the scheduled task after execution
    schedule.cancel_job(scheduled_tasks[form_number])
    del scheduled_tasks[form_number]

def run_scheduled_tasks():
    while not stop_flag.is_set():
        schedule.run_pending()
        time.sleep(1)

def signal_handler(sig, frame):
    logging.info("Termination signal received. Shutting down...")
    stop_flag.set()
    application.stop()
    application.is_idle = False

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("fill_form", fill_form))
    application.add_handler(CallbackQueryHandler(form_callback, pattern="^form_"))
    application.add_handler(CallbackQueryHandler(calendar_handler, pattern="^(day_|prev_|next_)"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    scheduler_thread = threading.Thread(target=run_scheduled_tasks)
    scheduler_thread.start()

    application.run_polling()