import telebot

import config
from managers import MonoManager, SheetManager

if __name__ == "__main__":
    sheet_manager = SheetManager.SheetManager(
        credentials=config.SERVICE_ACCOUNT_CREDENTIALS,
        scope=config.SCOPE,
    )

    bot = telebot.TeleBot(config.BOT_TOKEN)

    @bot.message_handler(commands=["debtors"])
    def send_debtors(message):
        bot.reply_to(message, sheet_manager.get_debtors_message())

    bot.infinity_polling()
