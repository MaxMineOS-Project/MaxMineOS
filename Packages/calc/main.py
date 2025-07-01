def main(argv:list[str]):
    condition = input("Введите выражение: ")
    try:
        print(eval(condition))
        return 0
    except ZeroDivisionError:
        print("Произошла ошибка! Делить на ноль нельзя!")
    except Exception:
        print("Произошла неизвестная ошибка!")
        return 1