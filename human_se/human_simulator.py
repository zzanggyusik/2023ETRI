import logging
import sys

from human_info_manager import HumanInfoManager


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def main() -> None:
    scenario = sys.argv[1]
    seed = sys.argv[2]



    HumanInfoManager().start_engine()

if __name__ == '__main__':
    main()
    
    
    
    