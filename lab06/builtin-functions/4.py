import time
import math

num = int(input())  # Число, квадратный корень которого нужно найти
ms = int(input())   # Задержка в миллисекундах

time.sleep(ms / 1000)  # Задержка в секундах
print(f"Square root of {num} after {ms} milliseconds is {math.sqrt(num)}")
