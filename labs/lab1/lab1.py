class OutOfRangeException(Exception):
    pass


class WrongCommandException(Exception):
    pass


def get_commands():
    with open('commands.txt', 'r') as f:
        commands = f.read()
    return commands.strip().split('\n')


class Command:
    def __init__(self, direction, step, start_point, max_range):
        self.direction = direction
        self.step = int(step)
        self.start_point = [start_point[0], start_point[1]]
        self.max_range = max_range
        self.moves = []

    def run(self):
        [x, y] = self.start_point
        for _ in range(self.step):
            if self.direction == 'R':
                x += 1
            if self.direction == 'L':
                x -= 1
            if self.direction == 'U':
                y -= 1
            if self.direction == 'D':
                y += 1
            if x not in range(1, self.max_range) or y not in range(1, self.max_range):
                raise OutOfRangeException("Robot has reached field limit")
            self.moves.append([x, y])
        self.finish_point = [x, y]
        return self.finish_point

    def print_forward_steps(self):
        print(self.stringify_steps(self.moves))

    def print_reverse_steps(self):
        moves = self.moves[:-1][::-1] + [self.start_point]
        print(self.stringify_steps(moves))

    @staticmethod
    def stringify_steps(steps):
        return '\n'.join([f'{step[0]},{step[1]}' for step in steps])


class Robot:
    def __init__(self, max_range=100):
        self.commands = []
        self.max_range = max_range
        self.current_point = [1, 1]

    def move(self, direction, step):
        if int(step) < 1 or direction not in 'RLUDB':
            raise WrongCommandException("Wrong data")
        if direction == 'B':
            for _ in range(int(step)):
                if not self.commands:
                    raise WrongCommandException("No commands to undo")
                last_command = self.commands.pop()
                self.current_point = last_command.start_point
                last_command.print_reverse_steps()
        else:
            command = Command(direction, step, self.current_point, self.max_range)
            self.current_point = command.run()
            self.commands.append(command)
            command.print_forward_steps()


if __name__ == '__main__':
    commands = get_commands()
    robot = Robot()
    for command in commands:
        if command == 'B':
            direction = 'B'
            step = 1
        else:
            direction, step = command.split(',')
        try:
            robot.move(direction, step)
        except (WrongCommandException, OutOfRangeException) as e:
            print(f'Wrong command "{command}. reason: {e}')
