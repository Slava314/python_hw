from multiprocessing import Process
from threading import Thread
from time import time


def fib(n):
    res = [0, 1]
    for i in range(2, n + 1):
        res.append(res[i - 1] + res[i - 2])
    return res


if __name__ == '__main__':
    n = 100000
    n_jobs = 10
    start = time()
    for _ in range(n_jobs):
        fib(n)
    sync_time = time() - start

    start = time()
    threads = [Thread(target=fib, args=(n,)) for _ in range(n_jobs)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    threads_time = time() - start

    start = time()
    processes = [Process(target=fib, args=(n,)) for _ in range(n_jobs)]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    process_time = time() - start

    with open("artifacts/easy.txt", "w") as file:
        file.write("Synchronous: {}s\n".format(sync_time))
        file.write("Threading: {}s\n".format(threads_time))
        file.write("Multiprocessing: {}s\n".format(process_time))

