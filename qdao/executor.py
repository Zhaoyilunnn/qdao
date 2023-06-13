import asyncio
import concurrent.futures
import multiprocessing as mp
import time
from multiprocessing.pool import ThreadPool
from threading import Thread
from typing import Optional


class ParallelExecutor:
    def __init__(self, func, args) -> None:
        self._func = func
        self._args = args

    def execute(self):
        threads = [Thread(target=self._func, args=arg) for arg in self._args]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()


class BatchParallelExecutor:
    def execute(self, func, args_list):
        cpu_cnt = mp.cpu_count()

        def split_list(lst, size):
            return [lst[i : i + size] for i in range(0, len(lst), size)]

        args_lists = split_list(args_list, cpu_cnt)

        for args_lst in args_lists:
            threads = [Thread(target=func, args=args) for args in args_lst]

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()


class PoolParallelExecutor:
    def execute(self, func, args_list):
        res = []

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=mp.cpu_count()
        ) as executor:
            res = []
            for args in args_list:
                res.append(executor.submit(func, *args))

            for r in concurrent.futures.as_completed(res):
                try:
                    data = r.result()
                except Exception as e:
                    print(f"exception! {e}")


class ConstantPoolParallelExecutor:

    """
    When NQ is much larger than NL, there will be excessive overhead
    Try to run thread pool group by group with each group of CPU_COUNT size
    """

    CPU_CNT = mp.cpu_count()

    def _execute(self, func, args_list):
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.CPU_CNT
        ) as executor:
            res = []
            for args in args_list:
                res.append(executor.submit(func, *args))

            for r in concurrent.futures.as_completed(res):
                try:
                    data = r.result()
                except Exception as e:
                    print(f"exception! {e}")

    def execute(self, func, args_list):
        res = []

        def split_list(lst, size):
            return [lst[i : i + size] for i in range(0, len(lst), size)]

        args_lists = split_list(args_list, self.CPU_CNT)

        for args_lst in args_lists:
            self._execute(func, args_lst)
            time.sleep(1)


class AsyncIoExecutor:

    """
    When NQ is much larger than NL, there will be excessive overhead
    Try to run thread pool group by group with each group of CPU_COUNT size

    """

    CPU_CNT = mp.cpu_count()

    async def _execute_one_task(self, func, args):
        func(*args)

    async def _execute_one_batch(self, func, args_list):
        tasks = []

        for args in args_list:
            tasks.append(asyncio.create_task(self._execute_one_task(func, args)))

        results = await asyncio.gather(*tasks)

    def execute(self, func, args_list):
        asyncio.run(self._execute_one_batch(func, args_list))
