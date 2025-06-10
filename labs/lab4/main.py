import ctypes

libcalcprimes = ctypes.CDLL('./libcalcprimes.so')

libcalcprimes.calculate_primes.argtypes = [
    ctypes.POINTER(ctypes.c_int),
    ctypes.c_int
]

libcalcprimes.calculate_primes.restype = None


def calculate_primes(n):
    primes = (ctypes.c_int * (n + 1))()
    libcalcprimes.calculate_primes(primes, n)

    return primes


if __name__ == '__main__':
    n = input('Введите нижнюю границу промежутка: ')
    m = input('Введите верхнюю границу промежутка: ')

    n = int(n)
    m = int(m)
    primes = calculate_primes(m)

    while n <= m:
        counts = 0
        bottom_x = None
        for i in range(2, n // 2 + 1):
            if primes[i] and primes[n - i]:
                counts += 1

                if counts == 1:
                    bottom_x = i

        if counts > 0:
            print(n, counts, bottom_x, n - bottom_x)
        else:
            print(f'Для числа {n} разложения не найдено')
        n += 2
