import os

# [General]
LOCALE = "uk_UA.UTF-8"

# [GCP]
SERVICE_ACCOUNT_CREDENTIALS = "credentials.json"

# [Google Sheets]
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

TABLE_NAME = "table_name"
SHEET_NAME = "sheet_name"
ADMIN_USER_COLUMN = "B"

USERS_TO_SKIP_FROM_LUCKY_CHOOSE = []

USER_NAMES_MAPPING = {
    "John Doe1": "@telegram_nickname1",
    "John Doe2": "@telegram_nickname2",
    "John Doe3": "@telegram_nickname3",
    "John Doe4": "@telegram_nickname4",
    "John Doe5": "@telegram_nickname5",
    "John Doe6": "@telegram_nickname6",
}

USER_COLUMNS_MAPPING = {
    "@telegram_nickname1": "B",
    "@telegram_nickname2": "C",
    "@telegram_nickname3": "D",
    "@telegram_nickname4": "E",
    "@telegram_nickname5": "F",
    "@telegram_nickname6": "G",
}

# [Telegram configs]
BOT_TOKEN = "bot_token"
ADMIN_USER_ID = 0

HELP_MESSAGE_UA = (
    """
/help - всі команди
/debtors - список боржників

Команди для власника:
/set_updates - записати оновлення з банки
/set_charge - записати оплату за Спотіфай
    """,  # noqa: E122
)

ONLY_FOR_ADMIN_MESSAGE_UA = "Команда тільки для власника"
TOO_MANY_REQUESTS_MESSAGE_UA = "Моно важко, спробуй ще раз згодом"
UPDATE_WAS_30_DAYS_AGO_MESSAGE_UA = "Моно не десть дістати виписку за 30 днів+"
PAY_UPDATE_SUCCESSFUL_MESSAGE_UA = "Зарахування на банку внесені"

DEBTORS_MESSAGE_UA = "Боржники:\n"
DEBTORS_DEBT_MESSAGE_UA = "{name} твій баланс {balance}, заплати {pay}\n"
NO_DEBTORS_MESSAGE_UA = "Нема :)"

SUCCESSFUL_WITHDRAWAL_MESSAGE_UA = "Спотіфайне відрахування внесено"
NO_NEED_TO_WITHDRAWAL_MESSAGE_UA = "Відрахування ще не потрібно"

# [Monobank configs]
MONO_TOKEN = "monobank_token"
MONO_ACCOUNT = "0"
MONOBANKA_ID = "monobanka_id"

JAR_LINK = "https://send.monobank.ua/jar/jar_id"

DESCRIPTION_PAID_UA = "Від: "
DESCRIPTION_WITHDRAWAL_UA = "На чорну картку"
DESCRIPTION_INCOME_UA = "Додавання до банки"

# [Files with stored values]
DATA_FILES_FOLDER = "data_files"
LAST_PAY_UPDATE_FILE_PATH = os.path.join(DATA_FILES_FOLDER, "last_pay_update.txt")
CURRENT_ROW_TO_WRITE_FILE_PATH = os.path.join(
    DATA_FILES_FOLDER, "current_row_to_write.txt"
)
LAST_CHARGE_UPDATE_FILE_PATH = os.path.join(DATA_FILES_FOLDER, "last_charge_update.txt")
