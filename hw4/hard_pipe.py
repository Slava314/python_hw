import time
from datetime import datetime
from multiprocessing import Process, Pipe
import codecs


def a_func(get_connection, put_connection):
    while True:
        time.sleep(5)
        put_connection.send(get_connection.recv().lower())


def b_func(get_connection, put_connection):
    while True:
        put_connection.send(codecs.encode(get_connection.recv(), "rot_13"))


if __name__ == '__main__':
    main_to_a, main_to_a_end = Pipe(True)
    a_to_b, a_to_b_end = Pipe(True)
    b_to_main, b_to_main_end = Pipe(True)
    Process(target=a_func, args=(main_to_a_end, a_to_b), daemon=True).start()
    Process(target=b_func, args=(a_to_b_end, b_to_main), daemon=True).start()
    with open("artifacts/hard_pipe.txt", "w") as file:
        while True:
            time = datetime.now().strftime("%H:%M:%S") + "> "
            msg = input(time)
            file.write(time + msg + '\n')
            main_to_a.send(msg)
            res = b_to_main_end.recv()
            time = datetime.now().strftime("%H:%M:%S") + "> "
            print(time + res)
            file.write(time + res + '\n')
