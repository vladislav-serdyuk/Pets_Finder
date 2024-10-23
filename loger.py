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

from typing import Literal
import sys
from datetime import datetime


class Logger:
    def __init__(self, file=None, use_stdout=True, use_stderr=True):
        self.log_path = file
        self.use_stdout = use_stdout
        self.use_stderr = use_stderr

    def log(self, message, log_level: Literal['INFO', 'WARNING', 'ERROR', 'CRITICAL ERROR']):
        text = f'[{datetime.now().strftime('%d.%m.%Y %H:%M:%S')} | {log_level}] {message}'

        if self.log_path is not None:
            with open(self.log_path, 'a') as file:
                file.write(text + '\n')

        if self.use_stdout and not self.use_stderr:
            print(text)

        if self.use_stderr and not self.use_stdout:
            print(text, file=sys.stderr)

        if self.use_stdout and self.use_stderr:
            if log_level == 'INFO':
                print(text)
            else:
                print(text, file=sys.stderr)
