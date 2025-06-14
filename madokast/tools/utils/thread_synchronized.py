import threading
from functools import wraps
from typing import Callable, Any, TypeVar, Dict

# 全局锁池 + 保护锁
_lock_pool:Dict[str, threading.Lock] = {}
_lock_pool_lock = threading.Lock()

AnyCallable = TypeVar('AnyCallable', bound=Callable[..., Any])

def Synchronized(key:str):
    """
    带参数的装饰器，根据 key_func 返回的 key（必须可哈希）来加锁。
    实现不同方法间共享 key 对应的锁。
    """
    def decorator(func:AnyCallable) -> AnyCallable:
        @wraps(func)
        def wrapper(*args:Any, **kwargs:Any) -> Any:
            # 加锁确保 _lock_pool 的安全访问
            with _lock_pool_lock:
                if key not in _lock_pool:
                    _lock_pool[key] = threading.Lock()
                lock = _lock_pool[key]

            # 使用 key 对应的锁
            with lock:
                return func(*args, **kwargs)

        return wrapper # type: ignore
    return decorator