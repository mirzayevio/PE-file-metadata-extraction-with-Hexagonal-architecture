import argparse


def main():
    parser = argparse.ArgumentParser(description='Process files based on task size.')
    parser.add_argument('task_size', nargs='?', help='Size of the task (integer value)')
    args = parser.parse_args()

    def validate_task_size(task_size):
        try:
            return int(task_size)
        except ValueError:
            print(f'Error: {task_size} is not a valid integer.')
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

    # Now you can proceed with your application logic using `args.task_size`
    # For example:
    # process_files(args.task_size)


if __name__ == '__main__':
    main()