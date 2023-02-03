from datetime import datetime as dt
from time import time


def result_logger(data, result):
    left_value, oper, right_value = data
    data_str = f'{str(left_value)} {oper} {str(right_value)}'
    time = 'time is '+dt.now().strftime('%H:%M')
    # print('{}; операция : {} результат : {}\n'.format(time, data_str, data))
    with open('log.csv', 'a', encoding='UTF-8') as file:
        file.write('{}; Operation : {} Result :{}\n'.format(
            time, data_str, result))
