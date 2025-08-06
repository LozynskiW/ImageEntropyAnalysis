import sys

def parse_args(args):
    parsed = {}
    for arg in args:
        if arg.startswith("-") and "=" in arg:
            key, value = arg.lstrip("-").split("=", 1)
            parsed[key] = value
    return parsed

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    for key, value in args.items():
        print(f"Argument {key} = {value}")
