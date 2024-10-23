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

import requests

import imageio
from g4f.client import Client


def url_to_numpy_img(url: str):
    return imageio.v2.imread(requests.get(url).content)


class Differ:
    def __init__(self):
        self.client = Client()
        self.text_model = "gpt-4o"
        self.template_prompt = """
        Человек потерял свего любимого питомца и написал описание питомца.
        Описание питомца может содержать место потери, цвет ошейника и т.д.
        Также есть пост с ВК о потеряном животном.
        Тебе необходимо оценить числом от 0 до 10 насколько описание питомца в посте соотвествует описанию человека.
        0 - полнастью не соотвествует
        10 - полнастью соотвествует
        ТЫ УМЕЕШЬ ЭТО ДЕЛАТЬ!
        ОТВЕЧАЙ ТОЛЬКО ЧИСЛО ОТ 0 ДО 10 БЕЗ КАКОГО ЛИБО ТЕКСТА!

        Текст владельца питомца
        "
        {statement_text}
        "
        Текст поста
        "
        {post_text}
        "
        """

    def _chat_gpt(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.text_model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content

    def diff(self, post: dict, statement: dict):
        # post_images = list(map(url_to_numpy_img, post['photo_urls']))
        post_text: str = post['text']
        # statement_img = statement['image']
        statement_text = statement['text']

        for _ in range(3):
            res = self._chat_gpt(self.template_prompt.format(statement_text=statement_text, post_text=post_text))
            try:
                text_cor = int(res)
                break
            except ValueError:
                pass
        else:
            text_cor = 0

        # TODO pets face recognition

        return text_cor / 10
