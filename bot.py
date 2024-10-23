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
from time import sleep

import telebot

from config import tg_token, wallet_addr
from finder import Finder
from loger import Logger

bot = telebot.TeleBot(tg_token)
finder = Finder()
logger = Logger('./log.txt')


@bot.message_handler(['start'])
def start(message: telebot.types.Message):
    logger.log(
        'user ID: ' + str(message.from_user.id) + ' | user name: ' + str(message.from_user.username)
        + ' | message text: ' + message.text, 'INFO')

    start_text = """
    Этот бот может искать животных.
    Просто отправь картинку животного с текстом.
    В первой строке текста укажи дату пропажи в формате дд.мм.гггг

    Пример:
      10.10.2088
      Потерялся котопёс в г.Питер пр.Джо Байдана с ошейником со встроеной майнинг фермой. ...
      
    Для доната введи /donat
    """

    bot.send_message(message.chat.id, start_text)


@bot.message_handler(['donat'])
def donat(message: telebot.types.Message):
    logger.log(
        'user ID: ' + str(message.from_user.id) + ' | user name: ' + str(message.from_user.username)
        + ' | message text: ' + message.text, 'INFO')

    donat_message = f"""
    Просто переведи Bitcoin на этот кошелёк:
    {wallet_addr}
    """

    bot.send_message(message.chat.id, donat_message)


@bot.message_handler(content_types=['text', 'photo'])
def find(message: telebot.types.Message):
    logger.log(
        'user ID: ' + str(message.from_user.id) + ' | user name: ' + str(message.from_user.username)
        + ' | message text: ' + message.text, 'INFO')

    start_find_text = """
    Поиск зверей в VK
    """

    bot.send_message(message.chat.id, start_find_text)

    date_str, text = message.text.split('\n', maxsplit=1)

    if message.photo is None:
        img_url = None
    else:
        img_url = bot.get_file(message.photo[0].file_id).file_path

    statement = {
        'date': datetime.strptime(date_str, '%d.%m.%Y'),
        'photo': img_url,
        'text': text,
    }

    print(f'Start finding: {statement}')

    find_posts = finder.find(statement, 10)

    # print(f'Found: {find_posts}')

    for val, post in find_posts:
        text = (f'{val * 100}%\n'
                f'\n'
                f'{post['text']}\n'
                f'\n'
                f'{post['date'].strftime('%d.%m.%Y %H:%M:%S')}\n'
                f'Original: https://vk.com/{post['wall_domain']}')

        if post['photo_urls']:
            logger.log(f'Send message to {message.from_user.id}', 'INFO')
            if len(text) > 1024:
                for x in range(0, len(text), 1024):
                    if x > 0:
                        bot.send_message(message.chat.id, text[x:x + 1024])
                    else:
                        bot.send_photo(message.chat.id, photo=post['photo_urls'][0], caption=text[x:x + 1024])
            else:
                bot.send_photo(message.chat.id, photo=post['photo_urls'][0], caption=text)
        else:
            if len(text) > 1024:
                for x in range(0, len(text), 1024):
                    bot.send_message(message.chat.id, text[x:x + 1024])
            else:
                bot.send_message(message.chat.id, text)

        sleep(1)

    bot.send_message(message.chat.id, '[END]')


bot.infinity_polling()
