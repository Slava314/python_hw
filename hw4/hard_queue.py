import time
from datetime import datetime
from multiprocessing import Queue, Process
import codecs


def a_func(main_to_a, a_to_b):
    while True:
        while not main_to_a.empty():
            a_to_b.put(main_to_a.get_nowait().lower())
            time.sleep(5)


def b_func(a_to_b, b_to_main):
    while True:
        b_to_main.put(codecs.encode(a_to_b.get(), "rot_13"))


if __name__ == '__main__':
    main_to_a = Queue()
    a_to_b = Queue()
    b_to_main = Queue()
    Process(target=a_func, args=(main_to_a, a_to_b), daemon=True).start()
    Process(target=b_func, args=(a_to_b, b_to_main), daemon=True).start()
    with open("artifacts/hard_queue.txt", "w") as file:
        while True:
            time = datetime.now().strftime("%H:%M:%S") + "> "
            msg = input(time)
            file.write(time + msg + '\n')
            main_to_a.put(msg)
            res = b_to_main.get()
            time = datetime.now().strftime("%H:%M:%S") + "> "
            print(time + res)
            file.write(time + res + '\n')
