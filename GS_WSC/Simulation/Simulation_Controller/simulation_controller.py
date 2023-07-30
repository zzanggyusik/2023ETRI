from simulation_controller_manager import SimController
import logging
import sys

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

def main() -> None:
    SimController().start_engine()

if __name__ == '__main__':
    main()