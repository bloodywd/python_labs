import argparse
from pathlib import Path
import hashlib


def parse_args():
    parser = argparse.ArgumentParser(description="Находит и удаляет дубликаты файлов")
    parser.add_argument("directory",
                        nargs='?',
                        default=None,
                        help="Директория")

    args = parser.parse_args()

    if args.directory is None:
        directory = Path.cwd()
    else:
        directory = Path.cwd() / args.directory

    return directory


def get_file_hash(file_path):
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()
