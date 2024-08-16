import gspread
import telebot
from gspread import Client
from oauth2client.service_account import ServiceAccountCredentials

import config


def get_debtors_message(client: Client) -> str:
    worksheet = client.open(config.TABLE_NAME).sheet1

    table = worksheet.batch_get(["C1:F2"])[0]

    message = config.DEBTORS_MESSAGE_UA
    debtors_exists = False
    for i in range(len(table[0])):
        balance = float(table[1][i].replace(",", "."))
        if float(balance) < 55:
            debtors_exists = True
            # TODO: round zaplati to up int
            # TODO: add USD value instead of 55
            message += config.DEBTORS_DEBT_MESSAGE_UA.format(
                name=table[0][i], balance=balance, pay=55 - balance
            )

    if not debtors_exists:
        message += config.NO_DEBTORS_MESSAGE_UA
    else:
        message += "\n" + config.MONOBANKA_LINK

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
