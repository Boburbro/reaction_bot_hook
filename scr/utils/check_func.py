def check_func(func):
    def wrapper_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            print(error)

    return wrapper_func