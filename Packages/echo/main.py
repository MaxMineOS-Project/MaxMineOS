def main(argv: list[str]):
    if len(argv) < 2:
        print("Передайте все, что хотите вывести в аргументы!")
        return 1

    newline = True
    args = argv[1:]

    if args[0] == "-n":
        newline = False
        args = args[1:]

    output = " ".join(args)
    print(output, end="" if not newline else "\n")
    return 0
