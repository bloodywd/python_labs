import argparse
import csv
import statistics

from labs.lab3.splitter import split_data


class WrongDataError(BaseException):
    pass

def read_data_from_file(file_path):
    if not file_path.endswith(".csv"):
        raise WrongDataError("Exception of file must be .csv")

    try:
        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            data = [(float(row[0]), int(row[1])) for row in reader]
            if not data:
                raise WrongDataError("No data to read")
            return header, data
    except FileNotFoundError:
        raise WrongDataError("File was not found")
    except PermissionError:
        raise WrongDataError("No permission to read file")
    except ValueError:
        raise WrongDataError("Failed to read data")


def calculate_statistics(data):
    for segment in data:
        values_list = [value for time, value in segment['data']]
        if values_list:
            segment["count"] = len(values_list)
            segment["mean"] = statistics.mean(values_list)
            segment["mode"] = statistics.mode(values_list)
            segment["median"] = statistics.median(values_list)
        else:
            segment["count"] = 0
            segment["mean"] = None
            segment["mode"] = None
            segment["median"] = None
    return data


def print_statistics(data):
    for segment in data:
        print('-----------------------------------------')
        print(
            f"Отрезок {segment['segment_start_time']} - {segment['segment_end_time']} секунд:")
        print(f"Количество значений: {segment['count']}")
        print(f"Среднее значение: {segment['mean']:.2f}")
        print(f"Мода: {segment['mode']}")
        print(f"Медиана: {segment['median']}")
    print('-----------------------------------------')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Обработка CSV-файла")
    parser.add_argument("file_path", help="Путь к файлу")
    parser.add_argument("interval", type=int, nargs="?", default=300,
                        help="Интервал разбиения в секундах")
    args = parser.parse_args()

    file_path = args.file_path
    interval = args.interval
    try:
        header, data = read_data_from_file(file_path)
        segments = split_data(data, interval)
        stats = calculate_statistics(segments)
        print_statistics(stats)
    except WrongDataError as e:
        print(e)
