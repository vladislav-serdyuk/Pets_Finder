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

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

user_token = os.getenv('user_token')

walls_domain = [
    'gefundendog',              # vk.com/gefundendog
    'poiskzhivotnykh',          # vk.com/poiskzhivotnykh
    'obyavleniyaozhivotnykh',   # vk.com/obyavleniyaozhivotnykh
    'poteryashkamoskva',        # vk.com/poteryashkamoskva
]

tg_token = os.getenv('tg_token')  # telegram bot token

wallet_addr = os.getenv('wallet_addr')  # cripto wallet address
