r"""
装饰器，将异常直接 return 返回

uv --directory C:\Users\57856\Documents\GitHub\aitools\madokast\tools\utils run print_exception.py
"""

from functools import wraps
from typing import Callable, Any, Union


AnyCallable = Callable[..., Any]


def print_exception(func:AnyCallable) -> AnyCallable:
    @wraps(func)
    def wrapper(*args:Any, **kwargs:Any) -> Union[str, Any]:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Error: {e}"
    return wrapper

if __name__ == '__main__':
    @print_exception
    def test(a:int, b:int) -> str:
        return str(a/b)
    
    print(test(1, 1))
    print(test(1, 0))

