import importlib.util
import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    parser.add_argument("--port", type=int, default=None)
    parser.add_argument("--host", type=str, default=None)
    args = parser.parse_args()

    file_path, class_name = args.target.rsplit(":", 1)

    spec = importlib.util.spec_from_file_location("_vivid_user_module", file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["_vivid_user_module"] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]

    cls = getattr(module, class_name)
    cls(port=args.port, host=args.host).run()


if __name__ == "__main__":
    main()