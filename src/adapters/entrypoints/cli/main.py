import argparse

from src.configurator.config import CATALOGS
from src.configurator.containers import container


def main() -> None:
    parser = argparse.ArgumentParser(description='Process files based on task size.')
    parser.add_argument('task_size', nargs='?', help='Size of the task (integer value)')
    args = parser.parse_args()

    def validate_task_size(n):
        try:
            n = int(n)
            if n <= 0:
                raise ValueError('Number must be positive')
            if n % len(CATALOGS) != 0:
                raise ValueError(
                    f'Warning: {n} is not divisible by 2. This may result in uneven distribution.'
                )
            return n
        except ValueError as e:
            print(f'Error: {n} is not a valid positive integer. {str(e)}')
            exit(1)

    if args.task_size is None:
        while True:
            try:
                task_size_input = input('Enter task size: ')
                args.task_size = validate_task_size(task_size_input)
                break
            except ValueError:
                print('Please enter a valid integer.')
    else:
        args.task_size = validate_task_size(args.task_size)

    print(f'Task size received: {args.task_size}')

    task_size = args.task_size // len(CATALOGS)

    metadata_cli_controller = container.metadata_cli_controller()
    metadata_cli_controller.execute(task_size)


if __name__ == '__main__':
    main()
