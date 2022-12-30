from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# конпки основного меню
btnProfile = KeyboardButton('Профиль')
btnSub = KeyboardButton('Подписка')
btnList = KeyboardButton('Главное меню')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.add(btnProfile, btnSub, btnList)

# конпки для оплаты подписки
sub_inline_markup = InlineKeyboardMarkup(row_width=1)
btnSubWeek = InlineKeyboardButton(text="Неделя - 100 рублей", callback_data="subweek")
btnSubMonth = InlineKeyboardButton(text="Месяц - 230 рублей", callback_data="submonth")
btnSubMonthYear = InlineKeyboardButton(text="Год - 370 рублей", callback_data="subyear")
sub_inline_markup.add(btnSubWeek, btnSubMonth, btnSubMonthYear)

# конпки меню функций
functions_button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
official_site = KeyboardButton('Сайт школы')
main_info = KeyboardButton('Музыка для танцев')
show_video_vip = KeyboardButton('Поиск видео')
show_video = KeyboardButton('Поиск видео')
show_wiki = KeyboardButton('Поиск в WIKI')
back_main = KeyboardButton('Назад')
functions_button.add(official_site, main_info, show_video, show_wiki,  back_main)

# конпка для перехода на официальный сайт
go_site = InlineKeyboardMarkup(row_width=1)
site = InlineKeyboardButton("Перейти на сайт", url="https://trinity-dance.ru/")
go_site.add(site)


# конпка для перехода плэйлисту
go_music_list = InlineKeyboardMarkup(row_width=1)
music_playlist = InlineKeyboardButton("Музыка для танцев",
                                      url="https://music.yandex.ru/users/alex181103@mail.ru/playlists/1002")
go_music_list.add(music_playlist)

