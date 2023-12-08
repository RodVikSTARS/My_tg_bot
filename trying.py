import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

logging.basicConfig(level=logging.INFO)

bot = Bot(token="6420088892:AAGEUuE7tCMyQ-DaZSMQQBXCd_P5avuQe-Y")
dp = Dispatcher()

to_main_menu_btn = KeyboardButton(text='Главное меню')
to_main_menu_keyboard = ReplyKeyboardMarkup(keyboard=[[to_main_menu_btn]], resize_keyboard=True)

main_menu_btns = [[KeyboardButton(text='Бонус за отзыв'), KeyboardButton(text='Задать вопрос')],
                  [KeyboardButton(text='Бонус за отметку в inst')],
                  [KeyboardButton(text='Акционные товары'), KeyboardButton(text='Наши ресурсы')]]
main_menu_keyboard = ReplyKeyboardMarkup(keyboard=main_menu_btns, resize_keyboard=True)

bonus_btns = [[KeyboardButton(text='Я отавил(-а) отзыв')],
              [to_main_menu_btn]]
bonus_keyboard = ReplyKeyboardMarkup(keyboard=bonus_btns, resize_keyboard=True)

bonus_inst_btns = [[KeyboardButton(text='Я опублтковал(-а) сторис')],
                   [to_main_menu_btn]]
bonus_inst_keyboard = ReplyKeyboardMarkup(keyboard=bonus_inst_btns, resize_keyboard=True)


class BonusGroup(StatesGroup):
    waiting_feetback_img = State()
    waiting_inst_img = State()


@dp.message(F.text == 'Главное меню')
async def main_menu(message: types.Message):
    message_text = ('Здравствуйте! Спасибо, что обратились в службу поддержки.\n\n'
                    'Выберите, пожалуйста, один из вариантов.\n\n'
                    'Eсли у вас пропало меню выбора ответа, нажмите справа на значок клавиатуры рядом со значком микрофона.')
    await message.answer(message_text, reply_markup=main_menu_keyboard)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await main_menu(message)


@dp.message(F.text == 'Бонус за отзыв')
async def bonus(message: types.Message):
    message_text = ('Чтобы получить бонус, выполните несколько простых действий.\n\n'
                    '1. Откройте приложение Wildberries на телефоне.\n'
                    '2. Нажмите на иконку профиля в нижнем правом углу.\n'
                    '3. Выберите категорию «Покупки».\n'
                    '4. Выберите товар, на который хотите оставить отзыв.\n'
                    '5. Найдите строчку «Отзывы», находится обычно под описанием товара.\n'
                    '6. Нажмите кнопку «Написать отзыв».\n'
                    '7. Поставьте товару 5 звезд.\n'
                    '8. Напишите текстовый комментарий.')
    await message.answer(message_text, reply_markup=bonus_keyboard)


@dp.message(F.text == 'Я отавил(-а) отзыв')
async def bonus_done(message: types.Message, state: FSMContext):
    await state.set_state(BonusGroup.waiting_feetback_img)
    message_text = (
        'Сделайте скриншот оставленного отзыва и пришлите его сюда (отправляйте, пожалуйста, только скриншот, без текста).\n\n'
        '❗️ Скриншот необходимо сделать из личного раздела Ваших отзывов «Отзывы и вопросы» по ссылке '
        'https://www.wildberries.ru/lk/discussion/feedback, предварительно выполнив вход в аккаунт.\n'
        '❗️ Скриншоты отзыва из карточки товара и любые другие не принимаются.')
    await message.answer(message_text, reply_markup=to_main_menu_keyboard)


@dp.message(BonusGroup.waiting_feetback_img)
async def handling_bonus(message: types.Message, state: FSMContext):
    img = message.photo
    await state.update_data(waiting_feetback_img=img)
    await bot.send_photo(chat_id=-4005785609, photo=img[0].file_id)
    await state.clear()


@dp.message(F.text == 'Задать вопрос')
async def question(message: types.Message):
    message_text = 'Расскажите, какой у Вас вопрос и мы быстро поможем решить Вашу проблему.'
    await message.answer(message_text, reply_markup=to_main_menu_keyboard)


@dp.message(F.text == 'Бонус за отметку в inst')
async def bonus_inst(message: types.Message):
    message_text = (
        'Мы дарим 300₽ за отметку в сторис или посте Instagram каждому клиенту с АКТИВНЫМ аккаунтом от 50 подписчиков. (1 товар = 1 бонус)\n\n'
        'Чтобы получить бонус, сделайте несколько простых действий.\n'
        '\t1. Опубликуйте фото в сторис или посте.\n'
        '\t2. На фото должны быть Вы с товаром или Ваше фото одежды, аксессуара, которые Вы приобрели у нас.\n'
        '\t3. Отметьте аккаунт @brnks_store. Отметка должна быть ЗАМЕТНОЙ для Ваших подписчиков, а сторис или пост должны находиться на странице не меньше 10-12 часов.\n\n'
        'Ссылка на Инстаграм:')
    await message.answer(message_text, reply_markup=bonus_inst_keyboard)


@dp.message(F.text == 'Я опублтковал(-а) сторис')
async def bonnus_inst_done(message: types.Message):
    message_text = (
        'Пришлите в диалог скриншот после того, как сторис или пост «провисит» указанное время (10-12 часов) '
        '(отправляйте, пожалуйста, только скриншот, без текста).')
    await message.answer(message_text, reply_markup=to_main_menu_keyboard)


@dp.message(F.text == 'Акционные товары')
async def sales_products(message: types.Message):
    message_text = 'Каталог товаров можно глянуть на странице: \nhttps://bmulti.store/'
    await message.answer(message_text, reply_markup=to_main_menu_keyboard)


@dp.message(F.text == 'Наши ресурсы')
async def urls_to_store(message: types.Message):
    message_text = ('Спасибо за интерес, проявленный к нашему бренду!🥰\n\n\n'
                    'Следите за нами в Instagram\n'
                    'https://www.instagram.com/brnks_store\n\n'
                    'Приобретайте наши товары на WB:\n'
                    'https://www.wildberries.by/brands/bronks\n'
                    'https://www.wildberries.by/brands/off-drop\n'
                    'https://www.wildberries.ru/brands/9490241-FLOW%20LAB\n\n'
                    'Всегда рады вам!')
    await message.answer(message_text, reply_markup=to_main_menu_keyboard, disable_web_page_preview=True)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
