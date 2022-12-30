from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType

from bs4 import BeautifulSoup
import requests
from selenium import webdriver

import datetime
import logging
import markups as nav
from textofmess import *
from database import Database

import time
from time import sleep

driver = webdriver.Chrome()

# Токен телеграм бота
TOKEN = "5982694895:AAGOTT18YXrxZnXl15L3asl5HZ3eKbmzrTc"
# Токен Юкассы
YOOTOKEN = "381764678:TEST:47643"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

db = Database('database.db')


def time_sub_day(get_time):
    """Оставшееся врямя подписки"""
    time_now = int(time.time())
    middle_time = int(get_time) - time_now
    if middle_time <= 0:
        return False
    else:
        dt = str(datetime.timedelta(seconds=middle_time))
        # Перевод дней на русский
        dt = dt.replace("days", "дней")
        dt = dt.replace("day", "день")
        return dt


def days_to_seconds(days):
    """Перевод дней в секунды"""
    return days * 24 * 60 * 60

# Создаём команду старт
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """Проверка регистрации в БД"""
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, "Укажите ваш ник!")
    else:
        await bot.send_message(message.from_user.id, "Вы уже зарегестрированны", reply_markup=nav.mainMenu)

# Создаём команду для рассылки сообщений пользоаателям
@dp.message_handler(commands=['sendtextall', 'sendphotoall'])
async def sendtextall(message: types.Message):
    """Рассылка сообщений пользоаателям"""
    if message.chat.type == 'private':
        # id, которые могут/может отправлять рассылку
        if message.from_user.id == 918855634:
            users = db.get_users()
            for row in users:
                if message.text[:12] == '/sendtextall':
                    text = message.text[13:]
                    # Проверка на платную подписку
                    if db.get_sub_status(row[0]):
                        await bot.send_message(row[0], text)
                else:
                    text_photo = message.text[14:]
                    # Проверка на платную подписку
                    if db.get_sub_status(row[0]):
                        await bot.send_photo(row[0], open('Photo_spam.jpg', 'rb'), text_photo)

@dp.message_handler()
async def bot_message(message: types.Message):
    """Функционал кнопок главного меню"""
    if message.chat.type == 'private':
        if message.text == "Профиль":
            user_nickname = "<b>Ваш никнейм:</b> " + db.get_nickname(message.from_user.id)
            user_sub = time_sub_day(db.get_time_sub(message.from_user.id))
            if not user_sub:
                user_sub = "Нет"
            user_sub = "\n<b>Подписка:</b> " + user_sub
            await bot.send_message(message.from_user.id,
                                   user_nickname + "\n<b>Пользователь:</b> " + message.from_user.full_name +
                                   user_sub + SubMemory, parse_mode='html')

        elif message.text == "Подписка":
            await bot.send_message(message.from_user.id, SubText, reply_markup=nav.sub_inline_markup)

        elif message.text == "Главное меню":
            await bot.send_message(message.from_user.id, "<b>Вы перешли в меню функций бота</b>",
                                   parse_mode='html', reply_markup=nav.functions_button)
            await bot.send_message(message.from_user.id, TextForStart)

        elif message.text == "Назад":
            await bot.send_message(message.from_user.id, "<b>Вы вернулись в основное меню бота</b>",
                                   parse_mode='html', reply_markup=nav.mainMenu)

        elif message.text == "Сайт школы":
            await bot.send_message(message.from_user.id,
                                   '<a href="https://trinity-dance.ru/">Сайт нашей школы танцев</a>',
                                   parse_mode="HTML",
                                   reply_markup=nav.go_site)

        elif message.text == "Назадㅤ":
            await bot.send_message(message.from_user.id, "<b>Вы вернулись в меню функций бота</b>",
                                   parse_mode='html', reply_markup=nav.functions_button)

        elif message.text == "Поиск видео":
            # Проверка на платную подписку
            if db.get_sub_status(message.from_user.id):
                await bot.send_message(message.from_user.id, "Что вы желаете найти?",
                                       reply_markup=types.ReplyKeyboardRemove())
                db.set_pars(message.from_user.id, "process")
            else:
                await bot.send_message(message.from_user.id, "\U000026A0Данная функция доступна при подписке\U000026A0"
                                                             "\nЖелаете приобрести?",
                                       reply_markup=nav.sub_inline_markup)

        elif message.text == "Музыка для танцев":
            await bot.send_message(message.chat.id, Playlist, reply_markup=nav.go_music_list)

        elif message.text == "Поиск в WIKI":
            # Проверка на платную подписку
            if db.get_sub_status(message.from_user.id):
                await bot.send_message(message.from_user.id, "Что бы вы хотели найти?",
                                       reply_markup=types.ReplyKeyboardRemove())
                db.set_pars(message.from_user.id, "process1")
            else:
                await bot.send_message(message.from_user.id, "\U000026A0Данная функция доступна при подписке\U000026A0"
                                                             "\nЖелаете приобрести?",
                                       reply_markup=nav.sub_inline_markup)

        else:
            if db.get_signup(message.from_user.id) == "setnickname":
                if len(message.text) > 15:
                    await bot.send_message(message.from_user.id, "Никнейм не должен превышать 15 символов")
                elif "@" in message.text:
                    await bot.send_message(message.from_user.id, "Вы ввели запрещённый символ")
                else:
                    db.set_nickname(message.from_user.id, message.text)
                    db.set_signup(message.from_user.id, "done")
                    await bot.send_message(message.chat.id, "Регистрация прошла успешно!", reply_markup=nav.mainMenu)
            else:
                # Парсинг ютуба
                if db.get_pars(message.from_user.id) == "process":
                    # Добавление к общей ссылке поиска в ютуб введённого пользователем текста
                    video = "https://www.youtube.com/results?search_query=" + message.text
                    driver.get(video)
                    # Остановка для более корректной работы selenium
                    sleep(2)
                    videos = driver.find_elements("id", "video-title")
                    number_of_videos = 0
                    # Вывод с картинкой о результатах поиска парсера
                    await bot.send_photo(message.chat.id,
                                         r'https://www.yandex.ru/images/search?from=tabbar&text=%D0%BF%D0%BE%D0%B8%D1'
                                         r'%81%D0%BA%D0%BE%D0%B2%D0%B8%D0%BA&pos=9&img_url=http%3A%2F%2Fi1.wp.com'
                                         r'%2Fsmm-gid.com%2Fwp-content%2Fuploads%2F2017%2F08%2Fpoisk-lyudey-v'
                                         r'-odnoklassnikah-bez-registratsii-besplatno.jpg&rpt=simage&lr=10765',
                                         caption="Вот, что я нашёл:")
                    # Цикл по парсингу видео
                    for i in range(len(videos)):
                        if not (("часа" or "часов") in videos[i].get_attribute('aria-label')):
                            await bot.send_message(message.chat.id, "Видео №" + str(number_of_videos + 1) + ":\n"
                                                   + videos[i].get_attribute('href'), reply_markup=nav.functions_button)
                            number_of_videos += 1
                            if number_of_videos == 3:
                                break
                    if number_of_videos == 0:
                        await bot.send_message(message.from_user.id, error_pars)
                    db.set_pars(message.from_user.id, "nopars")

                elif db.get_pars(message.from_user.id) == "process1":
                    url = "https://ru.wikipedia.org/w/index.php?go=%D0%9F%D0%B5%D1%80%D0%B5%D0%B9%D1%82%D0%B8&search=" \
                          + message.text
                    request = requests.get(url)
                    soup = BeautifulSoup(request.text, "html.parser")

                    # Ищем ссылки нужного класса
                    links = soup.find_all("div", class_="mw-search-result-heading")

                    # Проверка на наличие элементов ссылка и запоминание их в url
                    if len(links) > 0:
                        url = "https://ru.wikipedia.org" + links[0].find("a")["href"]

                    # Параметр чтобы драйвер не открывался на ПК или Хостинге
                    option = webdriver.ChromeOptions()
                    option.add_argument('headless')

                    driver1 = webdriver.Chrome(chrome_options=option)
                    driver1.get(url)

                    # Пролистать страницу браузера чуть ниже для более красивого вывода
                    driver1.execute_script("window.scrollTo(0, 200)")
                    # Сделать скрин страницы браузера
                    driver1.save_screenshot("img.png")
                    # Закрыть драйвер
                    driver1.close()

                    # Открыть скриншот
                    photo = open("img.png", "rb")
                    await bot.send_photo(message.chat.id, photo=photo, caption=f'Ссылка на статью: <a href="{url}">'
                                                                               f'перейти</a>', parse_mode="HTML",
                                         reply_markup=nav.functions_button)
                    db.set_pars(message.from_user.id, "nopars")

                else:
                    await bot.send_message(message.chat.id, '<b>Я тебя не понимаю.</b>', parse_mode='html')


@dp.callback_query_handler(text="subweek")
async def subday(call: types.CallbackQuery):
    """Обработчик для подписки на неделю"""
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_invoice(chat_id=call.from_user.id, title="Оформление подписки",
                           description=SubText, payload="week_sub", provider_token=YOOTOKEN,
                           currency="RUB", start_parameter="test_bot", prices=[{"label": "Руб", "amount": 10000}])


@dp.callback_query_handler(text="submonth")
async def submonth(call: types.CallbackQuery):
    """Обработчик для подписки на месяц"""
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_invoice(chat_id=call.from_user.id, title="Оформление подписки",
                           description=SubText, payload="month_sub", provider_token=YOOTOKEN,
                           currency="RUB", start_parameter="test_bot", prices=[{"label": "Руб", "amount": 23000}])


@dp.callback_query_handler(text="subyear")
async def subyear(call: types.CallbackQuery):
    """Обработчик для подписки на год"""
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_invoice(chat_id=call.from_user.id, title="Оформление подписки",
                           description=SubText, payload="year_sub", provider_token=YOOTOKEN,
                           currency="RUB", start_parameter="test_bot", prices=[{"label": "Руб", "amount": 37000}])


# Подтверждение возможности услуги
@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    """Обработчик подтверждающий наличие товара"""
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


# Обработчик после оплаты
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    """Обработчик, выдающий подписку"""

    # Обработчик выдачи подписки на неделю
    if message.successful_payment.invoice_payload == "week_sub":
        if db.get_time_sub(message.from_user.id) >= int(time.time()):
            time_sub = db.get_time_sub(message.from_user.id) + days_to_seconds(7)
        # Обработчик выдачи подписки на неделю
        else:
            time_sub = int(time.time()) + days_to_seconds(7)
        db.set_time_sub(message.from_user.id, time_sub)
        await bot.send_message(message.from_user.id, "Вам выдана подписка на неделю!!!")

    # Обработчик выдачи подписки на год
    elif message.successful_payment.invoice_payload == "month_sub":
        if db.get_time_sub(message.from_user.id) >= int(time.time()):
            time_sub = db.get_time_sub(message.from_user.id) + days_to_seconds(30)
        else:
            time_sub = int(time.time()) + days_to_seconds(30)
        db.set_time_sub(message.from_user.id, time_sub)
        await bot.send_message(message.from_user.id, "Вам выдана подписка на месяц!!!")

    elif message.successful_payment.invoice_payload == "year_sub":
        if db.get_time_sub(message.from_user.id) >= int(time.time()):
            time_sub = db.get_time_sub(message.from_user.id) + days_to_seconds(365)
        else:
            time_sub = int(time.time()) + days_to_seconds(365)
        db.set_time_sub(message.from_user.id, time_sub)
        await bot.send_message(message.from_user.id, "Вам выдана подписка на год!!!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
