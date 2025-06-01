"""
线程本地存储

测试方法 python -m madokast.utils.thread_local
"""

import threading
from typing import TypeVar, Callable, Generic, List

T = TypeVar('T')

class ThreadLocal(Generic[T]):

    def __init__(self, factory:Callable[[], T]) -> None:
        self.__factory = factory
        self.__local = threading.local()

    def __getattr__(self, name: str) -> T:
        if not hasattr(self.__local, 'value'):
            self.__local.value = self.__factory()
        return getattr(self.__local, name)

if __name__ == '__main__':
    threads:List[threading.Thread] = []
    for i in range(10):
        t = threading.Thread(target=lambda: print(ThreadLocal(lambda: f"i")))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    print("All threads finished.")

