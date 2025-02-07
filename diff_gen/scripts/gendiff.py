import argparse
from diff_gen.gendiff import generate_diff


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.'
    )
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument('-f', '--format', default='stylish', type=str,
                        help='set format of output')
    args = parser.parse_args()
    diff: str = generate_diff(args.first_file, args.second_file, args.format)
    print(diff)


if __name__ == '__main__':
    main()
