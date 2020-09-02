import time
from log import logger
import global_configs
from dependence.utils import hwnd_util
from dependence.utils.hwnd_util import *
from gui.hwnd_select_gui import *
from PIL import Image

from tasks import hunting_in_alberta

import init

task_list = []

if __name__ == '__main__':
    while True:
        if len(task_list) == 0:
            task_list.append(hunting_in_alberta.run)

        for i in task_list:
            logger.info("Running function: {}.{}.".format(i.__module__, i.__name__))
            i()
