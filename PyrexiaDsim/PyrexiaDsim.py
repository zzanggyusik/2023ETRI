# from .pyrexiaDsim_manager import PyrexiaDsim
from pyrexiaDsim_manager import PyrexiaDsim
import logging
import sys

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

def main() -> None:
    PyrexiaDsim().start_engine()

if __name__ == '__main__':
    main()