# from aiogram import Router, F, Bot
# from aiogram.filters import CommandStart
# from aiogram.fsm.context import FSMContext
# from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery
# from aiogram.utils.i18n import gettext as _
# from aiogram.utils.i18n import lazy_gettext as __
# from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
#
# from state import PartnerState, Hodim
#
# main_router = Router()
#
#
#
# @main_router.message(CommandStart())
# async def start_message(message: Message, bot: Bot):
#     ikb = InlineKeyboardBuilder()
#     ikb.add(
#         InlineKeyboardButton(text='Uz🇺🇿', callback_data='lang_uz'),
#         InlineKeyboardButton(text='En🇬🇧', callback_data='lang_en'),
#     )
#     await message.answer(_('Tilni tallang!'), reply_markup=ikb.as_markup(resize_keyboard=True))
#
#
# @main_router.callback_query(F.data.startswith('lang_'))
# async def languages(callback: CallbackQuery, state: FSMContext, bot: Bot, data=None):
#     lang_code = callback.data.split('lang_')[-1]
#     await state.update_data(locale=lang_code)
#     if lang_code == 'uz':
#         lang = _('Uzbek', locale=lang_code)
#     else:
#         lang = _('English', locale=lang_code)
#     await callback.answer(_('{lang} tili tanlandi', locale=lang_code).format(lang=lang))
#
#     rkb = ReplyKeyboardBuilder()
#     rkb.add(KeyboardButton(text=_('Sherik kerak', locale=lang_code)),
#             KeyboardButton(text=_('Ish joyi kerak', locale=lang_code)),
#             KeyboardButton(text=_('Hodim kerak', locale=lang_code)),
#             KeyboardButton(text=_('Ustoz kerak', locale=lang_code)))
#     rkb.adjust(2, repeat=True)
#     rkb.row(KeyboardButton(text=_('Shogird kerak', locale=lang_code)))
#     msg = (_("""Assalomu alaykum \nUstozShogird kanaliokning rasmiy botiga xush kelibsiz!\n
# /help yordam buyrugi orqali nimalarga qodir ekanligimni bilib oling!""", locale=lang_code))
#     await callback.message.delete()
#     await callback.message.answer(text=msg, reply_markup=rkb.as_markup(resize_keyboard=True))
#
#
# @main_router.message(F.text == '/help')
# async def register_help(message: Message):
#     await message.answer(_("""
#         UzGeeks faollari tomonidan tuzilgan Ustoz-Shogird kanali.\n\nBu yerda Programmalash bo`yicha\n#Ustoz,\n#Shogird,
#         #oquvKursi,\n#Sherik,\n#Xodim va\n#IshJoyi\ntopishingiz mumkin.\n\nE'lon berish: @UstozShogirdBot\n\n
#         Admin @UstozShogirdAdminBot
#     """))
#
#
# @main_router.message(F.text.in_((__('Sherik kerak'), __('Ish joyi kerak'), __('Ustoz kerak'), __('Shogird kerak'))))
# async def partner(message: Message, state: FSMContext):
#     await state.update_data(button_name=message.text)
#     data = await state.get_data()
#     if data['button_name'] == _('Ish joyi kerak'):
#         await message.answer(_(
#             """<b>Ish joyi topish uchun ariza berish</b>\n\nHozir sizga birnecha savollar beriladi.\n
# Har biriga javob bering. Oxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va\n
# arizangiz Adminga yuboriladi.""")
#         )
#     elif data['button_name'] == _('Ustoz kerak'):
#         await message.answer(_(
#             """<b>Ustoz topshirish uchun ariza berish</b>\n\nHozir sizga birnecha savollar beriladi.\n
# Har biriga javob bering. Oxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va\n
# arizangiz Adminga yuboriladi.""")
#         )
#     elif data['button_name'] == _('Sherik kerak'):
#         await message.answer(_(
#             """<b>Sherik topshirish uchun ariza berish</b>\n\nHozir sizga birnecha savollar beriladi.\n
# Har biriga javob bering. Oxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va\n
# arizangiz Adminga yuboriladi.""")
#         )
#     elif data['button_name'] == _('Shogird kerak'):
#         await message.answer(_(
#             """<b>Shogirt topshirish uchun ariza berish</b>\n\nHozir sizga birnecha savollar beriladi.\n
# Har biriga javob bering. Oxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va\n
# arizangiz Adminga yuboriladi.""")
#         )
#     await state.set_state(PartnerState.full_name)
#     await message.answer(_("<b>Ism, familiyangizni kiriting?</b>"))
#
#
# @main_router.message(PartnerState.full_name)
# async def full_name(message: Message, state: FSMContext):
#     await state.update_data(full_name=message.text)
#     data = await state.get_data()
#     if data["button_name"] == _('Sherik kerak'):
#         await state.set_state(PartnerState.texnology)
#         await message.answer(_("""<b>📚 Texnologiya:</b>\n\n
# Talab qilinadigan texnologiyalarni kiriting?\nTexnologiya nomlarini vergul bilan ajrating.
# <em>Masalan: Java, C++, C#</em>"""))
#     else:
#         await state.set_state(PartnerState.age)
#         await message.answer(_("""<b>🕑 Yosh: </b>\n\n
# Yoshingizni kiriting?
# Masalan: 19"""))
#
#
# @main_router.message(PartnerState.age)
# async def register(message: Message, state: FSMContext):
#     await state.update_data(age=message.text)
#     await state.set_state(PartnerState.texnology)
#     await message.answer(_("""<b>📚 Texnologiya:</b>\n\n
# Talab qilinadigan texnologiyalarni kiriting?\nTexnologiya nomlarini vergul bilan ajrating.
# <em>Masalan: Java, C++, C#</em>"""))
#
#
# @main_router.message(PartnerState.texnology)
# async def register_technology(message: Message, state: FSMContext):
#     await state.update_data(technology=message.text)
#     await state.set_state(PartnerState.phone_number)
#     await message.answer(_("""<b>📞 Aloqa:</b>\n\n"
# Bog`lanish uchun raqamingizni kiriting?\nMasalan: +998 90 123 45 67"""))
#
#
# @main_router.message(PartnerState.phone_number)
# async def register_phone(message: Message, state: FSMContext):
#     await state.update_data(phone_number=message.text)
#     await state.set_state(PartnerState.location)
#     await message.answer(_("""<b>🌐 Hudud: </b>\n\nQaysi hududdansiz?\n
# Viloyat nomi, Toshkent shahar yoki Respublikani kiriting."""))
#
#
# @main_router.message(PartnerState.location)
# async def register_location(message: Message, state: FSMContext):
#     await state.update_data(location=message.text)
#     await state.set_state(PartnerState.price)
#     await message.answer(_("""<b>💰 Narxi:</b>\n\nTolov qilasizmi yoki Tekinmi??\nKerak bo`lsa, Summani kiriting?"""))
#
#
# @main_router.message(PartnerState.price)
# async def register_price(message: Message, state: FSMContext):
#     await state.update_data(price=message.text)
#     await state.set_state(PartnerState.job)
#     await message.answer(_("""<b>👨🏻‍💻 Kasbi: </b>\n\nIshlaysizmi yoki o`qiysizmi?\nMasalan: Talaba"""))
#
#
# @main_router.message(PartnerState.job)
# async def register_job(message: Message, state: FSMContext):
#     await state.update_data(job=message.text)
#     await state.set_state(PartnerState.time)
#     await message.answer(
#         _("""<b>🕰 Murojaat qilish vaqti: </b>\n\nQaysi vaqtda murojaat qilish mumkin?\nMasalan: 9:00 - 18:00"""))
#
#
# @main_router.message(PartnerState.time)
# async def register_time(message: Message, state: FSMContext):
#     await state.update_data(time=message.text)
#     await state.set_state(PartnerState.goal)
#     await message.answer(_("<b>🔎 Maqsad: </b>\n\nMaqsadingizni qisqacha yozib bering."))
#
#
# @main_router.message(PartnerState.goal)
# async def register_goal(message: Message, state: FSMContext):
#     await state.update_data(goal=message.text)
#     data = await state.get_data()
#     text = ""
#     if data['button_name'] == _('Ish joyi kerak'):
#         text += f"<b>Ish joyi kerak:</b>\n\n👨‍💼 Xodim: {data.get('full_name')}\n"
#     elif data['button_name'] == _('Ustoz kerak'):
#         text += f"<b>Ustoz kerak:</b>\n\n👨‍💼 Ustoz: {data.get('full_name')}\n"
#     else:
#         text += f"<b>Shogird kerak:</b>\n\n👨‍💼 Shogird: {data.get('full_name')}\n"
#
#         text = _("""🕑 Yosh: {age}
# 📚 Texnologiya: {technology}
# 🇺🇿 Telegram: @{user_name}
# 📞 Aloqa: {phone_number}
# 🌐 Hudud: {location}
# 💰 Narxi: {price}
# 👨🏻‍💻 Kasbi: {job}
# 🕰 Murojaat qilish vaqti: {time}
# 🔎 Maqsad: {goal}
#   """).format(age=data.get('age'), texnology=data.get('technology'),user_name=data.get('user_name'),
#               phone_number=data.get('phone_number'),  location=data.get('location'), price=data.get('price'),
#                job=data.get('job'), time=data.get('time'), goal=data.get('goal'))
#
#     if data['button_name'] == _('Sherik kerak'):
#         text = _("""<b>Sherik kerak:</b>\n\n👨‍💼 Sherik: {full_name}
# 📚 Texnologiya: {technology}
# 🇺🇿 Telegram: @{user_name}
# 📞 Aloqa: {phone_number}
# 🌐 Hudud: {location}
# 💰 Narxi: {price}
# 👨🏻‍💻 Kasbi: {job}
# 🕰 Murojaat qilish vaqti: {time}
# 🔎 Maqsad: {goal}\n
# #shogird #ustoz #ish
# """).format(full_name=data.get('full_name'), technology=data.get('technology'), user_name=data.get('user_name'),
#             phone_numbe=data.get('phone_number'), location=data.get('location'), price=data.get('price'),
#             job=data.get('job'), time=data.get('time'), goal=data.get('goal'))
#
#     await message.answer(text)
#     await state.clear()
#     await message.answer("Barcha ma'lumotlaringiz tog'rimi?")
#     rkb = ReplyKeyboardBuilder()
#     rkb.row(KeyboardButton(text=_('HA')), KeyboardButton(text=_('YOQ')))
#     if data['button_name'] == _('HA'):
#         await message.answer(_('Saqlandi'))
#     elif data['button_name'] == _('YOQ'):
#         await message.answer(_('Qabul qilinmadi'))
#
#
# @main_router.message(F.text == __('Hodim kerak'))
# async def partner(message: Message, state: FSMContext):
#     await message.answer(_(
#         """<b>Xodim topish uchun ariza berish</b>\n\nHozir sizga birnecha savollar beriladi.\n"
# Har biriga javob bering. Oxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va\narizangiz Adminga yuboriladi.""")
#     )
#     await state.update_data(button_name=message.text)
#     await state.set_state(Hodim.idora)
#     await message.answer(_("<b>🎓 Idora nomi?</b>"))
#
#
# @main_router.message(Hodim.idora)
# async def register(message: Message, state: FSMContext):
#     await state.update_data(idora=message.text)
#     await state.set_state(Hodim.technology)
#     await message.answer(_("""<b>📚 Texnologiya:</b>\n\n
# Talab qilinadigan texnologiyalarni kiriting?\nTexnologiya nomlarini vergul bilan ajrating.\n
# <em>Masalan: Java, C++, C#</em>"""))
#
#
# @main_router.message(Hodim.technology)
# async def register_technology(message: Message, state: FSMContext):
#     await state.update_data(technology=message.text)
#     await state.set_state(Hodim.phone_number)
#     await message.answer(
#         _("""<b>📞 Aloqa:</b>\n\nBog`lanish uchun raqamingizni kiriting?\nMasalan: +998 90 123 45 67"""))
#
#
# @main_router.message(Hodim.phone_number)
# async def register_phone(message: Message, state: FSMContext):
#     await state.update_data(phone_number=message.text)
#     await state.set_state(Hodim.location)
#     await message.answer(_("""<b>🌐 Hudud: </b>\n\nQaysi hududdansiz?
# \nViloyat nomi, Toshkent shahar yoki Respublikani kiriting."""))
#
#
# @main_router.message(Hodim.location)
# async def register_location(message: Message, state: FSMContext):
#     await state.update_data(location=message.text)
#     await state.set_state(Hodim.time)
#     await message.answer(_("""<b>🕰 Murojaat qilish vaqti: </b>\n\nQaysi vaqtda murojaat qilish mumkin?
# \nMasalan: 9:00 - 18:00"""))
#
#
# @main_router.message(Hodim.time)
# async def register_price(message: Message, state: FSMContext):
#     await state.update_data(time=message.text)
#     await state.set_state(Hodim.time_worked)
#     await message.answer(_("<b>🕰 Ish vaqtini kiriting? </b>"))
#
#
# @main_router.message(Hodim.time_worked)
# async def register_job(message: Message, state: FSMContext):
#     await state.update_data(time_worked=message.text)
#     await state.set_state(Hodim.price)
#     await message.answer(_("""<b>💰 Narxi:</b>\n\nTolov qilasizmi yoki Tekinmi??\nKerak bo`lsa, Summani kiriting?"""))
#
#
# @main_router.message(Hodim.price)
# async def register_price(message: Message, state: FSMContext):
#     await state.update_data(price=message.text)
#     await state.set_state(Hodim.another)
#     await message.answer(_("<b>‼️ Qo`shimcha ma`lumotlar? </b>\n\n"))
#
#
# @main_router.message(Hodim.another)
# async def register_goal(message: Message, state: FSMContext):
#     await state.update_data(anpther=message.text)
#     data = await state.get_data()
#     if data['button_name'] == _('Hodim kerak'):
#         name = _("""
# <b>Xodim kerak:</b>\n
# 🏢 Idora: {idora}
# 📚 Texnologiya: {technology}
# 🇺🇿 Telegram: @{user_name}
# 📞 Aloqa: {phone_number}
# 🌐 Hudud: {location}
# ✍️ Mas'ul: {masul}
# 🕰 Murojaat qilish vaqti: {time}
# 🕰 Ish vaqti: {time_worked}
# 💰 Maosh: {price}
# ‼️ Qo`shimcha: {another}
# \n#hodim
# """).format(idora=data.get('idora'), technology=data.get('technology'), user_name=data.get(message.from_user.username),
#             phone_number=data.get('phone_number'), location=data.get('location'),
#             masul=data.get('masul'), time=data.get('time'), time_worked=data.get('time_worked'),
#             price=data.get('price'), another=data.get('another'))
#
#     await message.answer(name)
#     await message.answer("Barcha ma'lumotlaringiz tog'rimi?")
#     rkb = ReplyKeyboardBuilder()
#     rkb.row(KeyboardButton(text=_('HA')), KeyboardButton(text=_('YOQ')))
#     if data['button_name'] == _('HA'):
#         await message.answer(_('Saqlandi'))
#     elif data['button_name'] == _('YOQ'):
#         await message.answer(_('Qabul qilinmadi'))
#
#
# @main_router.message()
# async def register_message(message: Message):
#     await message.answer(_("/start so`zini bosing. E'lon berish qaytadan boshlanadi"))
#
#
