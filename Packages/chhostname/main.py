import _bootedit

def main(argv:list[str], abspath:str):
    if len(argv) < 2:
        print("Передайте новое имя ПК в аргументы!")
        return 1
    _bootedit.boot_edit(argv[1], abspath)
    print("Имя ПК изменено успешно!")
    return 0