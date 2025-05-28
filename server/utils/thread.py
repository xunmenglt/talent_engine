import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager

from typing import (
    List,
    Callable,
    Generator,
    Dict,
)


def run_in_thread_pool(
        func: Callable,
        params: List[Dict] = [],
) -> Generator:
    '''
    在线程池中批量运行任务，并将运行结果以生成器的形式返回。
    请确保任务中的所有操作是线程安全的，任务函数请全部使用关键字参数。
    '''
    tasks = []
    with ThreadPoolExecutor() as pool:
        for kwargs in params:
            thread = pool.submit(func, **kwargs)
            tasks.append(thread)

        for obj in as_completed(tasks):
            yield obj.result()
            



@contextmanager
def xthread(worker_num:int=6) -> ThreadPoolExecutor: # type: ignore
    """上下文管理器用于自动获取 ThreadPoolExecutor, 避免错误"""
    worker_num=min(os.cpu_count()*2,worker_num)
    pool = ThreadPoolExecutor(max_workers=worker_num)
    try:
        yield pool
    except:
        pool.shutdown(wait=True, cancel_futures=True)
        raise
    finally:
        pool.shutdown()