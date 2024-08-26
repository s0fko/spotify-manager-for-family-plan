import os

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

DEBTORS_MESSAGE_UA = "Боржники:\n"
DEBTORS_DEBT_MESSAGE_UA = "{name} твій баланс {balance}, заплати {pay}\n"
NO_DEBTORS_MESSAGE_UA = "Нема :)"

# [Monobank configs]
MONO_TOKEN = "monobank_token"
MONO_ACCOUNT = "0"
MONOBANKA_ID = "monobanka_id"

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
