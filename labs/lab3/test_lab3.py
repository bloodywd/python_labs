from pathlib import Path

import pytest
import os
from .main import read_data_from_file, split_data, calculate_statistics, \
    WrongDataError


def create_temp_csv(content):
    file = "test.csv"
    with open(file, "w", newline="") as f:
        f.write(content)
    return file


def test_file_not_found():
    with pytest.raises(WrongDataError):
        read_data_from_file("nonexistent.csv")


def test_file_no_permission():
    file_path = create_temp_csv("time,value\n1.0,100\n")
    file = Path(file_path)
    file.chmod(0o000)
    with pytest.raises(WrongDataError):
        read_data_from_file(file_path)
    file.chmod(0o777)
    os.remove(file_path)


def test_invalid_csv_row():
    invalid_data = """
    time,value
    1.0,10
    2.0
    """
    file_path = create_temp_csv(invalid_data)
    with pytest.raises(WrongDataError):
        read_data_from_file(file_path)
    os.remove(file_path)


def test_invalid_data_types():
    invalid_data = 'testdata'
    file_path = create_temp_csv(invalid_data)
    with pytest.raises(WrongDataError):
        read_data_from_file(file_path)
    os.remove(file_path)


def test_split_data_correctly():
    data = [(0, 100), (299.01, 200), (299.55, 150), (599.50, 250)]
    segments = split_data(data)
    assert len(segments) == 2
    assert segments[0]['segment_start_time'] == 0
    assert segments[1]['segment_start_time'] == 599.50


def test_split_data_count():
    data = [(0, 100), (600, 200), (1200, 300)]
    segments = split_data(data)
    assert len(segments) == 3


def test_statistics():
    data = [{'data': [(1, 10), (2, 20), (3, 30)]}]
    result = calculate_statistics(data)
    assert result[0]['count'] == 3
    assert result[0]['mean'] == 20
    assert result[0]['mode'] == 10
    assert result[0]['median'] == 20


def test_empty_file():
    file_path = create_temp_csv("time,value\n")
    with pytest.raises(WrongDataError):
        read_data_from_file(file_path)
    os.remove(file_path)


def test_same_values_mode():
    data = [{'data': [(1, 50), (2, 50), (3, 50)]}]
    result = calculate_statistics(data)
    assert result[0]['mode'] == 51


def test_different_intervals():
    data = [(0, 100), (150, 200), (250, 150)]
    segments_5min = split_data(data, 300)
    segments_3min = split_data(data, 180)
    assert len(segments_5min) == 1
    assert len(segments_3min) == 2
