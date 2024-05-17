#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os.path
import pathlib


'''Дополнение к заданию из работы 2.17.
Теперь пользователь может работать с двумя каталогами:
домашним и текущим (Где хранится программа)'''


def new_human(people, name, surname, telephone, happy_birthday):
    """Добавить данные о человеке."""
    people.append({
        "name": name,
        "surname": surname,
        "telephone": telephone,
        "birthday": happy_birthday
    })
    return people


def display_people(people):
    """Отобразить список людей."""
    # Проверка, что в списке есть люди.
    if people:
        # Заголовок таблицы.
        line = "├-{}-⫟-{}⫟-{}-⫟-{}-⫟-{}-┤".format(
            "-" * 5, "-" * 25, "-" * 25, "-" * 25, "-" * 18)
        print(line)
        print("| {:^5} | {:^24} | {:^25} | {:^25} | {:^18} |".format(
            "№", "Name", "Surname", "Telephone", "Birthday"))
        print(line)
        for number, human in enumerate(people, 1):
            print("| {:^5} | {:<24} | {:<25} | {:<25} | {:<18} |".format(number, human.get(
                "name", ""), human.get("surname", ""),
                human.get("telephone", ""),
                human.get("birthday", "")))
        print(line)
    else:
        print("There are no people in list!")


def select_people(people, month):
    """Выбрать людей, родившихся в требуемом месяце."""
    born = []
    for human in people:
        human_month = human.get("birthday").split(".")
        if month == int(human_month[1]):
            born.append(human)
    return born


def save_people(file_name, staff):
    """Сохранить всех людей в файл JSON."""
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установлен ensure_ascii=False
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_people(file_name):
    """Загрузить всех людей из файла JSON."""
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None):
    """Главная функция программы."""
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The name of data file."
    )
    file_parser.add_argument(
        "--own",
        action="store_true",
        help="Save data file in own directory.",
    )
    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("people")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    subparsers = parser.add_subparsers(dest="command")
    # Создать субпарсер для добавления человека.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a record about new human."
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="The human's name."
    )
    add.add_argument(
        "-s",
        "--surname",
        action="store",
        required=True,
        help="The human's post."
    )
    add.add_argument(
        "-t",
        "--telephone",
        action="store",
        required=True,
        help="The human's telephone number."
    )
    add.add_argument(
        "-b",
        "--birthday",
        action="store",
        required=True,
        help="The human's birthday."
    )
    # Создать субпарсер для отображения всех людей.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all people."
    )
    # Создать субпарсер для выбора людей.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select people according to their birth's month."
    )
    select.add_argument(
        "-P",
        "--period",
        action="store",
        type=int,
        required=True,
        help="The needed month."
    )
    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)
    # Загрузить всех людей из файла, если файл существует.
    is_dirty = False
    if args.own:
        filepath = pathlib.Path.home() / args.filename
    else:
        filepath = pathlib.Path(args.filename)
    if os.path.exists(filepath):
        people = load_people(filepath)
    else:
        people = []
    # Добавить человека.
    if args.command == "add":
        people = new_human(
            people,
            args.name,
            args.surname,
            args.telephone,
            args.birthday
        )
        is_dirty = True
    # Отобразить всех людей.
    elif args.command == "display":
        display_people(people)
    # Выбрать требуемых людей.
    elif args.command == "select":
        display_people(select_people(people, args.period))
    # Сохранить данные в файл, если список людей был изменен.
    if is_dirty:
        save_people(filepath, people)


if __name__ == "__main__":
    main()
