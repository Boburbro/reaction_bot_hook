def check_func(func):
    def wrapper_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            print(f"Error in {func.__name__}: {error}")
            # Return the error so it can be handled by the caller
            return error

    return wrapper_func