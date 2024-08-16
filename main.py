import gspread
import telebot
from gspread import Client
from oauth2client.service_account import ServiceAccountCredentials

import config


def get_debtors_message(client: Client) -> str:
    worksheet = client.open("spotify").sheet1

    table = worksheet.batch_get(["C1:F2"])[0]

    message = "Боржники:\n"
    debtors_exists = False
    for i in range(len(table[0])):
        balance = float(table[1][i].replace(",", "."))
        if float(balance) < 55:
            debtors_exists = True
            # TODO: round zaplati to up int
            message += f"{table[0][i]} твій баланс {balance}, заплати {55 - balance}\n"

    if not debtors_exists:
        message += "Нема :)"
    else:
        message += "\nhttps://send.monobank.ua/jar/8DkVAacNhm"

    return message


if __name__ == "__main__":
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        config.SERVICE_ACCOUNT_CREDENTIALS,
        config.SCOPE,
    )
    client = gspread.authorize(credentials)

    bot = telebot.TeleBot(config.BOT_TOKEN)

    @bot.message_handler(commands=["debtors"])
    def send_debtors(message):
        bot.reply_to(message, get_debtors_message(client))

    bot.infinity_polling()
