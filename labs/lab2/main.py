from redactor import FileRedactor
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Simple file redactor")
    parser.add_argument("file_path", help="Path to the file to edit")
    args = parser.parse_args()

    redactor = FileRedactor(args.file_path)
    redactor.read_file()
    while True:
        command_string = input('Enter command:\n')
        [command, *args] = command_string.split(' ')
        if command == 'exit':
            break
        else:
            redactor.run_command(command, *args)
