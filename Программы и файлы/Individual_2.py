#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import sys
import pathlib

# Аналог команде tree в Linux.


def tree(directory, args, prefix="", level=0):
    """Рекурсивный вывод содержимого каталога."""
    # Проверка глубины рекурсии. Если задан -p и текущая глубина превышает его, то прекращается дальнейшее выполнение.
    if args.p is not None and level > args.p:
        return
    # Получение содержимого текущего каталога.
    contents = list(directory.iterdir())
    # Если не задан -a, то НЕ учитываются скрытые файлы (Те, у которых в начале точка. Пример - .idea).
    if not args.a:
        filtered_contents = []
        for file in contents:
            if not file.name.startswith("."):
                filtered_contents.append(file)
        contents = filtered_contents

    # Если задан -d, то выводятся только каталоги.
    if args.d:
        filtered_contents = []
        for file in contents:
            if file.is_dir():  # Проверка, каталог ли.
                filtered_contents.append(file)
        contents = filtered_contents

    # Если задан -f, выводятся только не каталоги.
    if args.f:
        filtered_contents = []
        for file in contents:
            if file.is_file():  # Проверка, файл ли.
                filtered_contents.append(file)
        contents = filtered_contents

    ''' Для отображения наподобие оригинальной tree, используются такие декорации.
    Подсчитывается количество файлов в текущем каталоге. Перед последним ставится └──.
    Примечание: так как может быть необходимость раскрывания
    каталога, чуть дальше ещё идёт работа с просто |.'''

    decoration = ["├── "] * (len(contents) - 1) + ["└── "]

    # Начат анализ и вывод полученных данных. pointer - тип украшения.
    for pointer, path in zip(decoration, contents):
        # Если задан -t, выводится полный путь. Иначе только имя файла или каталога.
        if args.t:
            print(prefix + pointer + str(path))
        else:
            print(prefix + pointer + path.name)
        # Если текущий элемент - каталог, то вызывается функция tree для этого каталога.
        if path.is_dir():
            # Определение украшения для вложенных элементов (| или отступ).
            if pointer == "├── ":
                extension = "│   "
            else:
                extension = "    "
            tree(path, args, prefix=prefix + extension, level=level + 1)


def main(command_line=None):
    """Главная функция программы."""
    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "directory",
        type=str,
        help="The directory to list."
    )
    # Выводятся даже скрытые файлы.
    parser.add_argument(
        "-a",
        # Подобное хранение означает, что при использовании ключа, он будет эквивалентен True
        action="store_true",
        help="All files are listed."
    )
    # -f и -d взаимосключащие, так что их нужно запретить вводить одновременно.
    choose = parser.add_mutually_exclusive_group()
    # Выводятся лишь каталоги.
    choose.add_argument(
        "-d",
        action="store_true",
        help="List directories only."
    )
    # Выводятся лишь файлы.
    choose.add_argument(
        "-f",
        action="store_true",
        help="List files only."
    )
    # Программа не заходит в папки, если достигнут лимит глубины.
    parser.add_argument(
        "-p",
        type=int,
        help="Max display depth of the directory tree."
    )
    # Не просто имя файла, а полное имя.
    parser.add_argument(
        "-t",
        action="store_true",
        help="Print the full path prefix for each file."
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.0.1"
    )
    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)
    directory = pathlib.Path(args.directory).resolve(strict=True)
    tree(directory, args)


if __name__ == "__main__":
    main()
