def readFile(source, mode):
    file = open(source, mode)
    content = file.read()
    file.close()
    return content


def main():
    print(readFile("./resources/titanic.txt", "r"))


if __name__ == '__main__':
    main()
