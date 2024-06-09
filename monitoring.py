import requests
from datetime import datetime
import emoji
from PIL import Image, ImageDraw, ImageFont
from os import path
from config import read_ini_file


class Monitoring:

    URL = read_ini_file()['url']

    def __init__(self):
        self.pool = []
        self.counter = 0
        self.server_fall = False
        self.average_response_time = []
        self.assignee_id = 0
        self.assignee_message = False

    def get_average_response_time(self):
        if len(self.average_response_time) >= 5:
            art = sum(self.average_response_time) / len(self.average_response_time)
            self.average_response_time.pop(0)
            return art

        elif len(self.average_response_time) == 1:
            return self.average_response_time[0]
        elif len(self.average_response_time) == 0:
            return 1

        else:
            art = sum(self.average_response_time) / len(self.average_response_time)
            return art

    def generate_image(self, status_code, datetime, response_time):

        folder_path = path.join('.', 'img')
        message_header = {}

        if status_code == None:
            message_header['header_message'] = f"Сайт не доступен! Всё очень плохо..."
            message_header['ico'] = path.join(folder_path, 'rip.png')

        elif status_code != 200 and (self.get_average_response_time() > 1 and response_time > 1):
            message_header['header_message'] = "Обнаружены проблемы в работе сайта"
            message_header['ico'] = path.join(folder_path, 'atention.png')
        elif status_code != 200:
            message_header['header_message'] = "Обнаружены проблемы в работе сайта"
            message_header['ico'] = path.join(folder_path, 'atention.png')
        elif self.get_average_response_time() > 1 and response_time > 1:
            message_header['header_message'] = "Превышено среднее время отклика сайта"
            message_header['ico'] = path.join(folder_path, 'time.png')

        blank = Image.open(path.join(folder_path, 'blank.png'))
        ico = Image.open(message_header['ico'])
        font = ImageFont.truetype(path.join('fonts', 'font_Roboto.ttf'), size=40)

        draw_text = ImageDraw.Draw(blank)
        #  Тип события
        draw_text.text(
            (30, 40),
            message_header['header_message'],
            fill=('#282828'),
            font=font
            )
        #  Дата и время
        draw_text.text(
            (470, 150),
            str(datetime),
            fill=('#282828'),
            font=font
            )
        #  Сайт
        draw_text.text(
            (150, 245),
            self.URL,
            fill=('blue'),
            font=font
            )
        #  Время отклика
        draw_text.text(
            (510, 350),
            str(round(response_time, 2)) + "  сек." if response_time else 'Нет',
            fill=('green' if response_time and response_time <= 1 else 'red'),
            font=font
            )
        #  Среднее время отклика за 5 минут
        draw_text.text(
            (700, 450),
            str(round(self.get_average_response_time(), 2)) + "  сек.",
            fill=('green' if self.get_average_response_time() <= 1 else 'red'),
            font=font
            )
        #  Код ответа сервера
        draw_text.text(
            (420, 560),
            str(status_code) if status_code else 'Нет',
            fill=('green' if status_code == 200 else 'red'),
            font=font
            )

        blank.paste(ico, (850, 15), ico)
        blank_path = path.join('tmp', f'{str(len(self.pool))}.png')
        size = (500, 400)
        blank = blank.resize(size)
        blank.save(blank_path)

        return blank_path

    def get_text_notification(self, status_code, datetime, response_time):
        if status_code:
            rt = str(round(response_time, 2)) + " сек."
            if status_code == 200:
                sc = f'{status_code}  ({emoji.emojize(":check_mark:", language="en")}Всё ОК)'
            else:
                sc = f'{status_code}  ({emoji.emojize(":exclamation:", language="alias")}<a href="https://developer.mozilla.org/ru/docs/Web/HTTP/Status">расшифровка кодов</a>)'
        elif status_code == None:
            rt = 'Не удалось связаться с сервером!'
            sc = 'Не удалось связаться с сервером!'

        body_message = f"""<b>Дата и время события:</b>   {datetime}
<b>Сайт:</b>   {self.URL}
<b>Время текущего отклика:</b>   {rt} 
<b>Среднее время отклика за 5 минут:</b>   {round(self.get_average_response_time(), 2)} сек.
<b>Код ответа сервера:</b>   {sc}
    """
        if status_code == None:
            header_message = f"{emoji.emojize(':skull_and_crossbones:', language='en')} <b>Сайт не доступен! Всё очень плохо...</b>"
            return str(header_message + '\n' + body_message)

        elif status_code != 200 and (self.get_average_response_time() > 1 and response_time > 1):
            header_message = f"{emoji.emojize(':exclamation:', language='alias')} <b>Обнаружены проблемы в работе сайта</b>" + '\n' + f"{emoji.emojize(':clock7:', language='alias')} <b>Превышено среднее время отклика сайта</b>"
            return str(header_message + '\n' + body_message)
        elif status_code != 200:
            header_message = f"{emoji.emojize(':exclamation:', language='alias')} <b>Обнаружены проблемы в работе сайта</b>"
            return str(header_message + '\n' + body_message)
        elif self.get_average_response_time() > 1 and response_time > 1:
            header_message = f"{emoji.emojize(':clock7:', language='alias')} <b>Превышено среднее время отклика сайта</b>"
            return str(header_message + '\n' + body_message)

    def make_request(self):

        dt = datetime.now().replace(microsecond=0)
        try:
            r = requests.get(self.URL)
            self.average_response_time.append(r.elapsed.total_seconds())
            response_time = r.elapsed.total_seconds()

        except Exception as ex_:
            r = None

        if not self.server_fall:
            try:
                if r.status_code != 200 or (self.get_average_response_time() > 1 and response_time > 1):
                    self.server_fall = True
                    message = self.get_text_notification(status_code=r.status_code, datetime=dt,
                                                         response_time=response_time)
                    return message
                else:
                    return None

            except Exception:
                self.server_fall = True
                message = self.get_text_notification(status_code=None, datetime=dt, response_time=None)
                return message

        elif self.server_fall:
            self.counter += 1
            try:
                if r.status_code != 200 or (self.get_average_response_time() > 1 and response_time > 1):
                    img_path = self.generate_image(status_code=r.status_code, datetime=dt,
                                                         response_time=response_time)
                    self.pool.append(img_path)

            except Exception:
                img_path = self.generate_image(status_code=None, datetime=dt, response_time=None)
                self.pool.append(img_path)

            if self.counter >= 5 and self.pool:
                pool_copy = self.pool.copy()
                self.pool.clear()
                counter_copy = str(self.counter)
                self.counter = 0
                # media = types.MediaGroup()
                # text = f"<u>Из {counter_copy} последних запросов зафиксировано с проблемами</u> {len(pool_copy)}:"
                # for img in pool_copy:
                #     media.attach_photo(types.InputFile(img), caption=text)
                #
                # return media
                a = {'counter': counter_copy, 'pool': pool_copy}
                return a

            elif (self.counter >= 5) and (not self.pool):
                self.assignee_id = 0
                self.assignee_message = False
                self.server_fall = False
                self.counter = 0
                return f'Работа сайта восстановлена {emoji.emojize(":check_mark_button:", language="en")}'
