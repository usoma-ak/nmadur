from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove, KeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from state import PartnerState, Hodim

main_router = Router()


@main_router.message(CommandStart())
async def start_handler(message: Message):
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(text='Uz🇺🇿', callback_data='lang_uz'),
            InlineKeyboardButton(text='En🇬🇧', callback_data='lang_en'))
    await message.answer(_("Tilni tanlang: "), reply_markup=ikb.as_markup(resize_keboard=True))

@main_router.callback_query(F.data.startswith('lang_'))
async def languages(callback: CallbackQuery, state: FSMContext, data=None):
    lang_code = callback.data.split('lang_')[-1]
    await state.update_data(locale=lang_code)
    if lang_code == 'uz':
        lang = _("O'zbek", locale=lang_code)
    else:
        lang = _('English', locale=lang_code)
    await callback.answer(_('{lang} tili tanlandi', locale=lang_code).format(lang=lang))

    rkb = ReplyKeyboardBuilder()
    rkb.add(KeyboardButton(text=_('Sherik kerak', locale=lang_code)),
            KeyboardButton(text=_('Ish joyi kerak', locale=lang_code)),
            KeyboardButton(text=_('Hodim kerak', locale=lang_code)),
            KeyboardButton(text=_('Ustoz kerak', locale=lang_code)))
    rkb.adjust(2, repeat=True)
    rkb.row(KeyboardButton(text=_('Shogird kerak', locale=lang_code)))
    await callback.message.answer(
        _("""Assalomu alaykum {first_name} \nUstozShogird kanalining rasmiy botiga xush kelibsiz!\n\n
/help yordam buyrugi orqali nimalarga qodir ekanligimni bilib oling!""",
          locale=lang_code).format(
            first_name=callback.from_user.first_name),
        reply_markup=rkb.as_markup(resize_keyboard=True))

@main_router.message(F.text.startswith('Hodim') | F.text.startswith('Worker'))
async def partner(message: Message, state: FSMContext):
    await message.answer(_(
        "<b>Hodim topshirish uchun ariza berish</b>\n\nHozir sizga birnecha savollar beriladi.\n"
        "Har biriga javob bering. Oxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va\n"
        "arizangiz Adminga yuboriladi."
    ))
    await state.update_data(button_name=message.text)
    await state.set_state(Hodim.idora)
    await message.answer(_("<b>🎓 Idora nomi??</b>"))

@main_router.message(F.text.endswith('kerak') | F.text.endswith('need'))
async def kerak_command(message: Message, state: FSMContext):
    await message.answer(
        _('<b>{category} topish uchun ariza berish</b>\nHozir sizga birnecha savollar beriladi.\nHar biriga javob bering.\nOxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.').format(
            category=' '.join(message.text.split()[:-1])))
    await state.update_data(button_name=message.text)
    await message.answer(_('<b>Ism, familiyangizni kiriting?</b>'))
    await state.set_state(PartnerState.full_name)
    await state.update_data(category=' '.join(message.text.split()[:-1]))


@main_router.message(PartnerState.full_name)
async def full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    data = await state.get_data()
    if data['category'].startswith('Sherik'):
        await message.answer(_("<b>📚 Texnologiya:</b>\n\n"
                               "Talab qilinadigan texnologiyalarni kiriting?\nTexnologiya nomlarini vergul bilan ajrating."
                               "\n\n"
                               "<em>Masalan: Java, C++, C#</em>"))
        await state.set_state(PartnerState.texnology)
    else:
        await state.set_state(PartnerState.age)
        await message.answer(_("<b>🕑 Yosh: </b>\n\n"
                               "Yoshingizni kiriting?\n"
                               "Masalan: 19"))



@main_router.message(PartnerState.age)
async def register(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(PartnerState.texnology)
    await message.answer(_("<b>📚 Texnologiya:</b>\n\n"
                           "Talab qilinadigan texnologiyalarni kiriting?\nTexnologiya nomlarini vergul bilan ajrating."
                           "\n\n"
                           "<em>Masalan: Java, C++, C#</em>"))


@main_router.message(PartnerState.texnology)
async def register_technology(message: Message, state: FSMContext):
    await state.update_data(technology=message.text)
    await state.set_state(PartnerState.phone_number)
    await message.answer(_("<b>📞 Aloqa:</b>\n\n"
                           "Bog`lanish uchun raqamingizni kiriting?"
                           "\nMasalan: +998 90 123 45 67"))


@main_router.message(PartnerState.phone_number)
async def register_phone(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await state.set_state(PartnerState.location)
    await message.answer(_("<b>🌐 Hudud: </b>\n\n"
                           "Qaysi hududdansiz?"
                           "\nViloyat nomi, Toshkent shahar yoki Respublikani kiriting."))


@main_router.message(PartnerState.location)
async def register_location(message: Message, state: FSMContext):
    await state.update_data(location=message.text)
    await state.set_state(PartnerState.price)
    await message.answer(_("<b>💰 Narxi:</b>\n\n"
                           "Tolov qilasizmi yoki Tekinmi??"
                           "\nKerak bo`lsa, Summani kiriting?"))


@main_router.message(PartnerState.price)
async def register_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(PartnerState.job)
    await message.answer(_("<b>👨🏻‍💻 Kasbi: </b>\n\n"
                           "Ishlaysizmi yoki o`qiysizmi?"
                           "\nMasalan: Talaba"))


@main_router.message(PartnerState.job)
async def register_job(message: Message, state: FSMContext):
    await state.update_data(job=message.text)
    await state.set_state(PartnerState.time)
    await message.answer(_("<b>🕰 Murojaat qilish vaqti: </b>\n\n"
                           "Qaysi vaqtda murojaat qilish mumkin?"
                           "\nMasalan: 9:00 - 18:00"))


@main_router.message(PartnerState.time)
async def register_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await state.set_state(PartnerState.goal)
    await message.answer(_("<b>🔎 Maqsad: </b>\n\n"
                           "Maqsadingizni qisqacha yozib bering."))


@main_router.message(PartnerState.goal)
async def register_goal(message: Message, state: FSMContext):
    await state.update_data(goal=message.text)
    # await state.set_state(PartnerState.yegnd)
    data = await state.get_data()
    await state.clear()
    text = ""
    if data['button_name'].startswith(str(__('Sherik'))):
        text += _("👨‍💼 Sherik: {full_name}\n📚 Texnologiya: {technology}\n🇺🇿 Telegram: @{telegram}\n📞 Aloqa: {phone_number}\n🌐 Hudud: {hudud}\n💰 Narxi: {price}\n👨🏻‍💻 Kasbi: {job}\n🕰 Murojaat qilish vaqti: {time}\n🔎 Maqsad: {goal}").format(
            full_name=data.get('full_name'), age=data.get('age'), technology=data.get('technology'),
            telegram=str(message.from_user.username),
            phone_number=data.get('phone_number'), hudud=data.get('location'), price=data.get('price'),
            job=data.get('job'), time=data.get('time'),
            goal=data.get('goal'))
        await message.answer(text)
        await message.answer(_("Barcha ma'lumotlar to'g'rmi?"))
    else:
        if data['button_name'].startswith(str(__('Ish'))):
            text += "<b>Ish joyi kerak:</b>\n\n👨‍💼 Xodim: {full_name}\n".format(full_name=data.get('full_name'))
        elif data['button_name'].startswith(str(__('Ustoz'))):
            text += "<b>Ustoz kerak:</b>\n\n👨‍💼 Ustoz: {full_name}\n".format(full_name=data.get('full_name'))
        else:
            text += "<b>Shogird kerak:</b>\n\n👨‍💼 Shogird: {full_name}\n".format(full_name=data.get('full_name'))
        text += _("🕑 Yosh: {age}\n📚 Texnologiya: {technology}\n🇺🇿 Telegram: @{telegram}\n📞 Aloqa: {phone_number}\n🌐 Hudud: {hudud}\n💰 Narxi: {price}\n👨🏻‍💻 Kasbi: {job}\n🕰 Murojaat qilish vaqti: {time}\n🔎 Maqsad: {goal}").format(
            age=data.get('age'), technology=data.get('technology'), telegram=str(message.from_user.username),
            phone_number=data.get('phone_number'), hudud=data.get('location'), price=data.get('price'),
            job=data.get('job'),
            time=data.get('time'),
            goal=data.get('goal'))
        await message.answer(text)
        await message.answer(_('Saqlandi'))
        await state.clear()

        # await message.answer(_("Barcha ma'lumotlar to'g'rmi?"))


# @main_router.message(PartnerState.yegnd)
# async def register_handlers(message: Message, state: FSMContext):
#     await state.update_data(yegnd=message.text)
#     rkb = ReplyKeyboardBuilder()
#     rkb.row(KeyboardButton(text=_("HA")), KeyboardButton(text=_("YO'Q")))
#     if message.text == _("HA"):
#         await message.answer(_('Saqlandi'))
#     else:
#         await message.answer(_("Qa'bul qilinmadi"))


@main_router.message(Hodim.idora)
async def register(message: Message, state: FSMContext):
    await state.update_data(idora=message.text)
    await state.set_state(Hodim.texnology)
    await message.answer(_("<b>📚 Texnologiya:</b>\n\n"
                           "Talab qilinadigan texnologiyalarni kiriting?\nTexnologiya nomlarini vergul bilan ajrating."
                           "\n\n"
                           "<em>Masalan: Java, C++, C#</em>"))


@main_router.message(Hodim.texnology)
async def register_technology(message: Message, state: FSMContext):
    await state.update_data(technology=message.text)
    await state.set_state(Hodim.phone_number)
    await message.answer(_("<b>📞 Aloqa:</b>\n\n"
                           "Bog`lanish uchun raqamingizni kiriting?"
                           "\nMasalan: +998 90 123 45 67"))


@main_router.message(Hodim.phone_number)
async def register_phone(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await state.set_state(Hodim.location)
    await message.answer(_("<b>🌐 Hudud: </b>\n\n"
                           "Qaysi hududdansiz?"
                           "\nViloyat nomi, Toshkent shahar yoki Respublikani kiriting."))


@main_router.message(Hodim.location)
async def register_location(message: Message, state: FSMContext):
    await state.update_data(location=message.text)
    await state.set_state(Hodim.time)
    await message.answer(_("<b>🕰 Murojaat qilish vaqti: </b>\n\n"
                           "Qaysi vaqtda murojaat qilish mumkin?"
                           "\nMasalan: 9:00 - 18:00"))


@main_router.message(Hodim.time)
async def register_price(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await state.set_state(Hodim.time_worked)
    await message.answer(_("<b>🕰 Ish vaqtini kiriting? </b>"))


@main_router.message(Hodim.time_worked)
async def register_job(message: Message, state: FSMContext):
    await state.update_data(time_worked=message.text)
    await state.set_state(Hodim.price)
    await message.answer(_("<b>💰 Narxi:</b>\n\n"
                           "Tolov qilasizmi yoki Tekinmi??"
                           "\nKerak bo`lsa, Summani kiriting?"))


@main_router.message(Hodim.price)
async def register_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(Hodim.another)
    await message.answer(_("<b>‼️ Qo`shimcha ma`lumotlar? </b>\n\n"))


@main_router.message(Hodim.another)
async def register_goal(message: Message, state: FSMContext):
    await state.update_data(goal=message.text)
    # await state.set_state(Hodim.yegnd)
    data = await state.get_data()
    text = _("""
    🏢 Idora: {idora}
📚 Texnologiya: {technology}
🇺🇿 Telegram: @{username}
📞 Aloqa: {phone_number}
🌐 Hudud: {location}
✍️ Mas'ul: {masul}
 🕰 Murojaat qilish vaqti: {time}
🕰 Ish vaqti: {time_worked}
💰 Maosh: {price}
‼️ Qo`shimcha: {another}
""").format(idora=data.get('idora'), technology=data.get('technology'), username=message.from_user.username,
               phone_number=data.get('phone_number'), location=data.get('location'), masul=data.get('masul'),
               time=data.get('time'), time_worked=data.get('time_worked'), price=data.get('price'),
               another=data.get('another'))
    await message.answer(text)
    # await message.answer(_("Barcha ma'lumotlar to'g'rmi?"))
    await message.answer(_('Saqlandi'))
    await state.clear()


# @main_router.message(Hodim.yegnd)
# async def register_handlers(message: Message, state: FSMContext):
#     await state.update_data(yegnd=message.text)
#     rkb = ReplyKeyboardBuilder()
#     rkb.row(KeyboardButton(text=_("HA")), KeyboardButton(text=_("YO'Q")))
#     if message.text == _("HA"):
#         await message.answer(_('Saqlandi'))
#     else:
#         await message.answer(_("Qa'bul qilinmadi"))


@main_router.message()
async def register_message(message: Message, state: FSMContext):
    await message.answer(_("/start so`zini bosing. E'lon berish qaytadan boshlanadi"))
