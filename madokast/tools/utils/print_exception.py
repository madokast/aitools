r"""
装饰器，将异常直接 return 返回

uv --directory C:\Users\57856\Documents\GitHub\aitools\madokast\tools\utils run print_exception.py
"""

def print_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Error: {e}"
    return wrapper

if __name__ == '__main__':
    @print_exception
    def test(a, b):
        return str(a/b)
    
    print(test(1, 1))
    print(test(1, 0))

