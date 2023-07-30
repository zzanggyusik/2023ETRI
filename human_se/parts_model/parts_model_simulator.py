import logging
import sys

from parts_model_manager import PartsModelManager


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def main() -> None:
    # scenario = sys.argv[1]
    # seed = sys.argv[2]

    PartsModelManager().start_engine()

if __name__ == '__main__':
    main()
    
    
    
    