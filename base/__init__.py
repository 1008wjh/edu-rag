import os
import sys
module_dir=os.path.dirname(os.path.abspath(__file__))
project_root=os.path.dirname(module_dir)
if module_dir not in sys.path:
    sys.path.append(module_dir)
if project_root not in sys.path:
    sys.path.append(project_root)
#print(sys.path)
from config import config
from logger import logger
