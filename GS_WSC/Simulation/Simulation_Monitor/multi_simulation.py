from multi_simulation_manager import SimMonitor
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

def main() -> None:
    SimMonitor().start_engine()

if __name__ == '__main__':
    main()