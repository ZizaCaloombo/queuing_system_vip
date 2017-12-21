def tm(func):
    def wrapper():
      a = timer.time()
      func()
      b = timer.time() - a
      return b
    return wrapper

