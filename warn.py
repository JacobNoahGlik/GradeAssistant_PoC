import warnings

def deprecated(func):
    def wrapper(*args, **kwargs):
        warnings.warn(f"{func.__name__} is deprecated", category=DeprecationWarning)
        return func(*args, **kwargs)
    return wrapper