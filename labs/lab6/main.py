from pathlib import Path
from collections import defaultdict
from utils import parse_args, get_file_hash


def scan_directory(directory):
    hash_groups = defaultdict(list)
    try:
        for item in Path(directory).rglob('*'):
            if item.is_file() and item.stat().st_size > 0:
                file_hash = get_file_hash(item)
                hash_groups[file_hash].append(item)
    except:
        print('Ошибка чтения каталога')
    return hash_groups


def find_duplicates(hash_groups):
    is_any_duplicates = False
    for file_hash, files in hash_groups.items():
        if len(files) > 1:
            is_any_duplicates = True
            print(f"Найдены следующие дубликаты")
            for file in files:
                print(f"  - {file}")
    if not is_any_duplicates:
        print("Дубликатов не найдено")



if __name__ == '__main__':
    directory = parse_args()

    if not directory.exists():
        print(f"Директория {directory} не существует!")
    else:
        print("Сканирование ...")

        hash_groups = scan_directory(directory)
        find_duplicates(hash_groups)
