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

from datetime import datetime, UTC, timedelta
from json import JSONDecoder, JSONEncoder

import vk_api
from vk_api import VkApi

from loger import Logger

logger = Logger('./log.txt')


def _get_general_data_from_post(post):
    date = datetime.fromtimestamp(post['date'], UTC)
    text: str = post['text']
    photo_urls = []
    for attachment in post['attachments']:
        if attachment['type'] == 'photo':
            photo_url: str = attachment['photo']['orig_photo']['url']
            photo_urls.append(photo_url)
    general_data = {
        'date': date,
        'text': text,
        'photo_urls': photo_urls
    }
    return general_data


class VKHelper:
    def __init__(self, token):
        self.token = token
        self.vk_session = VkApi(token=token)
        self.vk = self.vk_session.get_api()

    def get_wall_post_list(self, domain, use_cache=True, cache_live_time_h=5):
        update_cache = True
        if use_cache:
            try:
                with open(f'cache/vk_walls/{domain}.json') as file:
                    cache_data = JSONDecoder().decode(file.read())
            except FileNotFoundError:
                logger.log(f'getting from  vk.com/{domain}', 'INFO')
                wall: dict = self.vk.wall.get(domain=domain, count=20)
                logger.log(f'get from vk.com/{domain}', 'INFO')
            # except JSONDecodeError as e:
            #     print(e)
            #     logger.log(f'getting from  vk.com/{domain}', 'INFO')
            #     wall: dict = self.vk.wall.get(domain=domain, count=20)
            #     logger.log(f'get from vk.com/{domain}', 'INFO')
            else:
                if datetime.now() - datetime.strptime(cache_data['date'], '%d.%m.%Y %S:%M:%H') \
                        < timedelta(seconds=cache_live_time_h * 60 * 60):
                    logger.log(f'Using vk posts cache', 'INFO')
                    wall = cache_data['wall']
                    update_cache = False
                else:
                    logger.log(f'getting from  vk.com/{domain}', 'INFO')
                    wall: dict = self.vk.wall.get(domain=domain, count=20)
                    logger.log(f'get from vk.com/{domain}', 'INFO')
        else:
            logger.log(f'getting from  vk.com/{domain}', 'INFO')
            wall: dict = self.vk.wall.get(domain=domain, count=20)
            logger.log(f'get from vk.com/{domain}', 'INFO')

        post_list = []
        for post in wall['items']:
            general_data = _get_general_data_from_post(post)
            general_data['wall_domain'] = domain
            post_list.append(general_data)

        if use_cache and update_cache:
            logger.log(f'Update vk posts cache', 'INFO')
            cache_data = {'date': datetime.now().strftime('%d.%m.%Y %S:%M:%H'), 'wall': wall}
            with open(f'cache/vk_walls/{domain}.json', 'w') as file:
                file.write(JSONEncoder().encode(cache_data))

        return post_list

    def post_list_from_walls(self, domains):
        post_list: list[dict[str, datetime | list[str] | str]] = []
        for domain in domains:
            try:
                post_list += self.get_wall_post_list(domain)
            except vk_api.ApiError:
                logger.log(f'Could not get data from the post vk.com/{domain}', 'WARNING')
                # raise RuntimeWarning(f'Could not get data from the post vk.com/{domain}'") from e

        return post_list
