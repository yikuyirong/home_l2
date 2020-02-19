
import functools

def log(text):
    def wrapper1(func):
        @functools.wraps(func)
        def wrapper2():
            print("call %s(): %s" % (func.__name__, text))
            return func()
        return wrapper2
    return wrapper1


@log("text")
def now():
    print("2020-02-01")


now()

print(now.__name__)

# log(now)

