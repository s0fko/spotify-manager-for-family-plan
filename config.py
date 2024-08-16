# [GCP]
SERVICE_ACCOUNT_CREDENTIALS = "credentials.json"

# [Google Sheets]
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

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

DESCRIPTION_PAID_UA = "Від: "
DESCRIPTION_WITHDRAWAL_UA = "На чорну картку"
DESCRIPTION_INCOME_UA = "Додавання до банки"

# [Monobank configs]
MONO_TOKEN = "monobank_token"
MONO_ACCOUNT = "0"
MONOBANKA_ID = "monobanka_id"

# [Files with stored values]
LAST_PAY_UPDATE_FILE_NAME = "last_pay_update.txt"
CURRENT_ROW_TO_WRITE_FILE_NAME = "current_row_to_write.txt"
