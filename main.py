import telebot

import config
from managers import MonoManager, SheetManager


def admin_only(func):
    def wrapper(message):
        if message.from_user.id == config.ADMIN_USER_ID:
            return func(message)
        else:
            bot.reply_to(message, "Команда тільки для Соні")

    return wrapper


if __name__ == "__main__":
    sheet_manager = SheetManager.SheetManager(
        credentials=config.SERVICE_ACCOUNT_CREDENTIALS,
        scope=config.SCOPE,
    )
    mono_manager = MonoManager.MonoManager(
        sheet_manager=sheet_manager,
    )

    bot = telebot.TeleBot(config.BOT_TOKEN)

    @bot.message_handler(commands=["debtors"])
    def send_debtors(message):
        bot.reply_to(message, sheet_manager.get_debtors_message())

    @bot.message_handler(commands=["set_updates"])
    @admin_only
    def set_updates(message):
        bot.reply_to(message, mono_manager.set_user_pay_updates())

    @bot.message_handler(commands=["set_charge"])
    @admin_only
    def set_charge(message):
        bot.reply_to(message, mono_manager.set_user_charge())

    bot.infinity_polling()
