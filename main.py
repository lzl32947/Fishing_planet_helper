from log import logger

from tasks import hunting_in_michigan

import init

task_list = []

if __name__ == '__main__':
    init.init_config()
    while True:
        if len(task_list) == 0:
            task_list.append(hunting_in_michigan.run)

        for i in task_list:
            logger.info("Running function: {}.{}.".format(i.__module__, i.__name__))
            i()
