from human_manager import Human
import logging
import sys

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

def main() -> None:
    Human().start_engine()

if __name__ == '__main__':
    main()