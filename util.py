import time


# 시간 측정 데코레이터 정의
def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"-> {func.__name__} 소요 시간: {end_time - start_time:.6f}초")
        return result

    return wrapper
