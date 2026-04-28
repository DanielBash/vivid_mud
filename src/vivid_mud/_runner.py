import importlib
import argparse
import sys
import os


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("target")
    parser.add_argument("--port", type=int, default=None)
    parser.add_argument("--host", type=str, default=None)

    args = parser.parse_args()

    module_name, class_name = args.target.split(":")

    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)

    app = cls(port=args.port, host=args.host)

    app.run()

if __name__ == "__main__":
    main()