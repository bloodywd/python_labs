class WrongCommandException(Exception):
    pass


class FileRedactor:
    def __init__(self, file_path):
        self.buffer = []
        self.file_state = ['']
        self.file_path = file_path

    def read_file(self):
        with open(self.file_path, 'r') as f:
            self.file_state = f.readlines()
            if not self.file_state:
                self.file_state = ['']

    def clear_file(self):
        self.buffer.append(self.file_state[:])
        self.file_state = ['']

    def save_file(self):
        with open(self.file_path, 'w') as f:
            f.write(''.join(self.file_state))

    def print_file(self):
        print(''.join(self.file_state))

    def delete_row(self, *args):
        if not args:
            raise WrongCommandException("Enter row number")

        try:
            delete_row_number = int(args[0]) - 1
            if delete_row_number < 0:
                raise WrongCommandException("Row must be greater that 0")
            if delete_row_number >= len(self.file_state):
                raise WrongCommandException(f"Row does not exist")
        except ValueError:
            raise WrongCommandException("Row must be integer")

        self.buffer.append(self.file_state[:])
        self.file_state = [self.file_state[row_number] for row_number
                           in range(len(self.file_state)) if
                           row_number != delete_row_number]

    def delete_column(self, *args):
        if not args:
            raise WrongCommandException("Enter column number")

        try:
            delete_column_number = int(args[0]) - 1
            if delete_column_number < 0:
                raise WrongCommandException("Column must be greater that 0")
        except ValueError:
            raise WrongCommandException("Column must be integer")

        self.buffer.append(self.file_state[:])
        for i in range(len(self.file_state)):
            new_row = self.file_state[i].rstrip('\n')
            if len(new_row) > delete_column_number:
                row_leftover = new_row[delete_column_number + 1:] if len(
                    new_row) - 1 != delete_column_number else ''
                self.file_state[i] = new_row[
                                     :delete_column_number] + row_leftover + '\n'

    def swap_rows(self, *args):
        if not args or len(args) != 2:
            raise WrongCommandException("Wrong arguments")

        try:
            first_row_number = int(args[0]) - 1
            second_row_number = int(args[1]) - 1
            if first_row_number < 0 or second_row_number < 0:
                raise WrongCommandException("Rows must be greater that 0")
            if first_row_number >= len(
                    self.file_state) or second_row_number >= len(
                    self.file_state):
                raise WrongCommandException("Row does not exist")
        except ValueError:
            raise WrongCommandException("Row must be integer")

        self.buffer.append(self.file_state[:])
        self.file_state[first_row_number], self.file_state[second_row_number] = \
        self.file_state[second_row_number], self.file_state[first_row_number]

    def undo_operation(self, *args):
        if not args:
            operation_count = 1
        else:
            try:
                operation_count = int(args[0])
                if operation_count < 1:
                    raise WrongCommandException("Enter valid operation number")
            except ValueError:
                raise WrongCommandException("Operation number must be integer")

        for _ in range(operation_count):
            if self.buffer:
                self.file_state = self.buffer.pop()

    def insert(self, *args):

        new_file_state = self.file_state[:]

        if not args:
            raise WrongCommandException("Enter arguments")
        else:
            insert_text = args[0]

        if len(args) >= 2:
            try:
                num_row = int(args[1])
                if num_row < 1:
                    raise WrongCommandException("Row must be greater that 0")
            except ValueError:
                raise WrongCommandException("Row must be integer")
        else:
            num_row = len(new_file_state)

        new_file_state.extend(['\n'] * (num_row - len(new_file_state)))

        current_line = new_file_state[num_row - 1].rstrip('\n')

        if len(args) == 3:
            try:
                num_col = int(args[2]) - 1
                if num_col < 0:
                    raise WrongCommandException(
                        "Column must be greater than 0")
            except ValueError:
                raise WrongCommandException("Column mast be integer")
        else:
            num_col = len(current_line)

        if num_col > len(current_line):
            current_line += ' ' * (num_col - len(current_line))

        new_line = current_line[:num_col] + insert_text + current_line[
                                                          num_col:] + '\n'
        new_file_state[num_row - 1] = new_line

        self.buffer.append(self.file_state[:])
        self.file_state = new_file_state

    def run_command(self, command, *args):
        COMMANDS = {
            'insert': self.insert,
            'del': self.clear_file,
            'delrow': self.delete_row,
            'delcol': self.delete_column,
            'swap': self.swap_rows,
            'undo': self.undo_operation,
            'show': self.print_file,
            'save': self.save_file,
        }
        try:
            COMMANDS[command](*args)
        except WrongCommandException as e:
            print(f"Command error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
