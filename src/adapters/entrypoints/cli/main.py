import argparse

from src.configurator.containers import container


def main():
    parser = argparse.ArgumentParser(description='Process files based on task size.')
    parser.add_argument('task_size', nargs='?', help='Size of the task (integer value)')
    args = parser.parse_args()

    def validate_task_size(n):
        try:
            return int(n)
        except ValueError:
            print(f'Error: {n} is not a valid integer.')
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

    metadata_cli_controller = container.metadata_cli_controller()

    task_size = args.task_size // 2

    metadata_cli_controller.execute(task_size)


if __name__ == '__main__':
    main()
