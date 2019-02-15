from sensors import sensors_read
from numcompress import compress
from time import strftime
from sql import write_db, update_db, init_db
from api import send_to_api
import threading


work_array = init_db()  # наполняем рабочий массив неотправленными данными из базы


def update_work_array(input_stream, case):  # функция обновления рабочего массива
    if case == 'delete':  # удаляем отправленные данные из рабочего массива
        for i in input_stream:
            if i in work_array:
                work_array.pop(work_array.index(i))
    if case == 'update':  # в случае успешной отправки помечаем данные статусом 1 (отправлено)
        work_array.pop(work_array.index(input_stream))
        work_array.append([input_stream[0], input_stream[1], 1, input_stream[3]])


def main_loop():
    time_memory = 0
    while True:
        cur_sec = int(strftime('%S'))
        # начало каждого такта с новой секунды
        if cur_sec != time_memory:
            time_memory = cur_sec

            obd_data = compress(sensors_read())
            # записываем false потому что данные только пришли и еще не было попыток отправить данные на сервер
            state = 0
            timestamp = strftime('%d%m%y%H%M%S')
            # пишем в базу и узнаем pk присвоенный записи
            base_id = write_db([obd_data, state, timestamp])
            # пишем в рабочий массив
            work_array.append([base_id, obd_data, state, timestamp])
            # смотрим рабочий массив на предмет измененных данных (отправленных) и удаляем из него
            update_work_array(update_db(work_array), 'delete')


def sending_loop():
    while True:
        for i in work_array:
            if i[2] == 0:  # ищем в рабочем массиве данные до статусом 0 (неотправленные)
                if send_to_api(i):  # если отправка удалась
                    update_work_array(i, 'update')  # апдейтим базу
                else:
                    print('id {} ERROR TRANSMISSION'.format(i[0]))


main_thread = threading.Thread(target=main_loop, name="read ecu and write to base", daemon=False)
main_thread.start()
sending_thread = threading.Thread(target=sending_loop, name="send to server", daemon=False)
sending_thread.start()
