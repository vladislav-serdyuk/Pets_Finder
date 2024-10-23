"""
Copyright 2024 Vladislav Serdyuk

Этот файл — часть Pets Finder.

Pets Finder — свободная программа: вы можете перераспространять ее и/или изменять ее на условиях Стандартной
общественной лицензии GNU в том виде, в каком она была опубликована Фондом свободного программного обеспечения; либо
версии 3 лицензии, либо (по вашему выбору) любой более поздней версии.

Pets Finder распространяется в надежде, что она будет полезной, но БЕЗО ВСЯКИХ ГАРАНТИЙ; даже без неявной гарантии
ТОВАРНОГО ВИДА или ПРИГОДНОСТИ ДЛЯ ОПРЕДЕЛЕННЫХ ЦЕЛЕЙ. Подробнее см. в Стандартной общественной лицензии GNU.

Вы должны были получить копию Стандартной общественной лицензии GNU вместе с этой программой. Если это не так,
см. <https://www.gnu.org/licenses/>.
"""

from datetime import datetime

import pytz
from threading import Thread, Lock

from differ import Differ
from vk_helper import VKHelper
from config import user_token, walls_domain
from loger import Logger

utc = pytz.UTC

vk_helper = VKHelper(user_token)
differ = Differ()

logger = Logger('./log.txt')


class Finder:
    def __init__(self):
        self.walls = walls_domain
        self.find_lock = Lock()
        self.run_th_num = 0

    def find(self, statement: dict[str, datetime | str], top):
        logger.log(f'Start finding top {top}: {statement}', 'INFO')
        find: list[tuple[float, dict[str, datetime | list[str] | str]]] = []
        posts = vk_helper.post_list_from_walls(self.walls)
        logger.log(f'Get {len(posts)} posts', 'INFO')
        for post in posts:
            if post['date'].replace(tzinfo=utc) < statement['date'].replace(tzinfo=utc):
                continue
            if 'пропал' in post['text'].lower():
                continue
            self.run_th_num += 1
            logger.log('Start diff thread', 'INFO')
            Thread(target=self._th_diff, args=(post, statement, find)).start()
        while self.run_th_num > 0:
            pass
        find.sort(key=lambda x: x[0], reverse=True)
        return find[0:top]

    def _th_diff(self, post: dict[str, datetime | list[str] | str], statement: dict[str, datetime | str], find):
        res = differ.diff(post, statement)
        self.find_lock.acquire()
        find.append((res, post))
        self.find_lock.release()
        logger.log(f'Diffed {statement}', 'INFO')
        self.run_th_num -= 1
