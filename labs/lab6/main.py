from pathlib import Path
from collections import defaultdict
from utils import parse_args, get_file_hash
import os


def scan_directory(directory):
    size_groups = defaultdict(list)
    try:
        for item in Path(directory).rglob('*'):
            size = item.stat().st_size
            if item.is_file() and size > 0:
                size_groups[size].append(item)
    except:
        print('Ошибка чтения каталога')
    return size_groups


def handle_duplicates(hash_groups):
    is_any_duplicates = False
    for file_hash, files in hash_groups.items():
        if len(files) > 1:
            is_any_duplicates = True
            print(f"Найдены следующие дубликаты")
            for i, file in enumerate(files):
                print(f"{i+1}. {file}")

            choise = input(f"Введите номер файла, который необходимо оставить\n"
                  f"Если нужно сохранить все файлы, введите \"save all\"\n")
            if choise.lower() == 'save all':
                print('Все файлы сохранены')
            else:
                try:
                    if int(choise) - 1 not in range(len(files)):
                        print('Некорректный номер')
                    else:
                        for i, file in enumerate(files):
                            if i != int(choise) - 1:
                                os.remove(file)
                                print(f'{file}: удален')
                except Exception as e:
                    print('Ошибка удаления', e)

    if not is_any_duplicates:
        print("Дубликатов не найдено")


def calculate_hash(size_groups):
    hash_groups = defaultdict(list)
    for size, files in size_groups.items():
        if len(files) > 1:
            for file in files:
                file_hash = get_file_hash(file)
                hash_groups[file_hash].append(file)
    return hash_groups


if __name__ == '__main__':
    directory = parse_args()

    if not directory.exists():
        print(f"Директория {directory} не существует!")
    else:
        print("Сканирование ...")

        size_groups = scan_directory(directory)
        hash_groups = calculate_hash(size_groups)
        handle_duplicates(hash_groups)
