import argparse


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('url')
    # parser.add_argument('episodes', '-e')

    args = parser.parse_args()
    print(args.url)


if __name__ == '__main__':
    main()