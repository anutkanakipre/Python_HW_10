

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from c_calc import Calc_block as c_calc
from logger import result_logger as write_log
import data_transformation as d_t
# import console_ui as c_ui

def input_data():
    global data_type 
    global left_value
    global oper
    global right_value
    return (data_type, left_value, oper, right_value)
 
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
data_type = 0
left_value = 0
oper = ''
right_value = 0


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="КАЛЬКУЛЯТОР 1.0а С какими числами будем работать? ")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="[/0] - Показать логи  - содержимое Log.csv ")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="[/1] - для работы с комплексными числами, ")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="[/2] - для работы с рациональными числами')")
result='111'

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global result
    global data_type 
    global left_value
    global oper
    global right_value
    if result == "Комплексные1":
        left_value = complex(update.message.text)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите второе число (используйте формат: 5 + 3j):")
        result = "Комплексные2"
    
    elif result == "Комплексные2":
        right_value = complex(update.message.text)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Выберите операцию: + - * / ")
        result = "Комплексные3"  

    elif result == "Комплексные3":
        oper = update.message.text
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Считаем комплексные {left_value} {oper} {right_value}")
        j = d_t.data_formatting(input_data())
        calc_result = c_calc(j)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Результат = {calc_result}")
        write_log(j, calc_result)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"добавлена запись в файл log.csv")
        result = "Комплексные4"  

    elif result == "Рациональные1":
        left_value = int(update.message.text)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите второе число :")
        result = "Рациональные2"  
    elif result == "Рациональные2":
        right_value = int(update.message.text)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Выберите операцию: + - * / ")
        result = "Рациональные3" 
    elif result == "Рациональные3":
        oper = update.message.text
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Считаем рациональные {left_value} {oper} {right_value}")
        
        j = d_t.data_formatting(input_data())
        calc_result = c_calc(j)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Результат = {calc_result}")
        write_log(j, calc_result)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"добавлена запись в файл log.csv")
        result = "Рациональные4"     


async def start1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global result
    global data_type
    await  context.bot.send_message(chat_id=update.effective_chat.id, text="[/1] ВЫБРАНО 1: БУДЕМ РАБОТАТЬ С КОМПЛЕКСНЫМИ ЧИСЛАМИ ")
    await  context.bot.send_message(chat_id=update.effective_chat.id, text="Введите первое число (используйте формат: 5 + 3j):")
    result="Комплексные1"
    data_type=1


async def start2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global result 
    global data_type
    await  context.bot.send_message(chat_id=update.effective_chat.id, text="[/2] ВЫБРАНО 2: БУДЕМ РАБОТАТЬ С рациональными ЧИСЛАМИ ")
    await  context.bot.send_message(chat_id=update.effective_chat.id, text="Введите первое число :")
    result="Рациональные1"
    data_type=2

async def start0(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await  context.bot.send_message(chat_id=update.effective_chat.id, text="[/0] Показываю содержание файла log.csv ")
    await  context.bot.send_message(chat_id=update.effective_chat.id, text="=============================")
    f = open("log.csv")
    count = 0
    for line in f:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=line)
        count = count+1
    f.close()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"=== Всего {count} записей ===")


if __name__ == '__main__':
    application = ApplicationBuilder().token('6185766163:AAHyKX_B2oUQDYSTeXadbi-UXDIz-hWdU18').build()
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    start_handler = CommandHandler('start', start)
    start_handler1 = CommandHandler('1', start1)
    start_handler2 = CommandHandler('2', start2)
    start_handler0 = CommandHandler('0', start0) 


    application.add_handler(echo_handler)
    application.add_handler(start_handler)
    application.add_handler(start_handler1)
    application.add_handler(start_handler2)
    application.add_handler(start_handler0)
    application.run_polling()

