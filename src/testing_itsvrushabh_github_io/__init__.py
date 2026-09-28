"""Main CLI entrypoint for testing-itsvrushabh-github-io."""
import sys
from behave.__main__ import main as behave_main


def main() -> None:
    """Run Behave test runner with provided CLI arguments."""
    sys.exit(behave_main())


if __name__ == "__main__":
    main()
