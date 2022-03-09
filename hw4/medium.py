import functools
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import cpu_count
import math
import os


def integrate_range(f, n_iter, log, range):
    a, b = range
    if log:
        print("Integrate range {} using process {}".format((a, b), os.getpid()))
    sum = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        sum += f(a + i * step) * step
    return sum


def integrate(f, a, b, *, n_jobs=1, n_iter=1000, pool_executor_f, log=True):
    if log:
        pool_type = ''
        if pool_executor_f is ProcessPoolExecutor:
            pool_type = "processes"
        if pool_executor_f is ThreadPoolExecutor:
            pool_type = "threads"
        print("Integrate function in range {} using {} jobs in {} with {} iters:".format((a, b), n_jobs, pool_type,
                                                                                         n_iter))
    job_range = (b - a) / n_jobs
    job_n_iter = int(n_iter / n_jobs)
    partial_integrate = functools.partial(integrate_range, f, job_n_iter, log)
    range_list = []
    for i in range(n_jobs):
        range_list.append((a + job_range * i, a + job_range * (i + 1)))
    with pool_executor_f(max_workers=n_jobs) as executor:
        return sum(executor.map(partial_integrate, range_list))


if __name__ == '__main__':
    start = time.time()
    res = integrate(math.cos, 0, math.pi / 2, n_jobs=10, n_iter=10000000, pool_executor_f=ProcessPoolExecutor)
    end = time.time()
    print("Done: {} in {}".format(res, end - start))
    res_process = []
    for i in range(1, cpu_count() * 2 + 1):
        start = time.time()
        integrate(math.cos, 0, math.pi / 2, n_jobs=i, n_iter=10000000, pool_executor_f=ProcessPoolExecutor, log=False)
        end = time.time()
        res_process.append((i, end - start))

    res_thread = []
    for i in range(1, cpu_count() * 2 + 1):
        start = time.time()
        integrate(math.cos, 0, math.pi / 2, n_jobs=i, n_iter=10000000, pool_executor_f=ThreadPoolExecutor, log=False)
        end = time.time()
        res_thread.append((i, end - start))

    with open("artifacts/medium.txt", "w") as file:
        file.write("Multiprocessing:\n")
        for item in res_process:
            file.write("n_jobs={} time={}\n".format(*item))
        file.write("\nThreading:\n")
        for item in res_thread:
            file.write("n_jobs={} time={}\n".format(*item))
