import gspread
from oauth2client.service_account import ServiceAccountCredentials

import config


class SheetManager:
    credentials = ""
    client = ""
    worksheet = ""

    def __init__(self, credentials, scope) -> None:
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            credentials,
            scope,
        )
        self.client = gspread.authorize(self.credentials)
        self.worksheet = self.client.open(config.TABLE_NAME).worksheet(
            config.SHEET_NAME
        )

    def get_debtors_message(self) -> str:
        table = self.worksheet.batch_get(["D1:G2"])[0]

        message = config.DEBTORS_MESSAGE_UA
        debtors_exists = False
        for i in range(len(table[0])):
            balance = float(table[1][i].replace(",", "."))
            if float(balance) < 55:
                debtors_exists = True
                # TODO: round zaplati to up int
                # TODO: add USD value instead of 55
                message += config.DEBTORS_DEBT_MESSAGE_UA.format(
                    name=table[0][i], balance=balance, pay=(55 - balance)
                )

        if not debtors_exists:
            message += config.NO_DEBTORS_MESSAGE_UA
        else:
            message += "\n" + config.MONOBANKA_LINK

        return message

    def update_users_cell(self, column: str, row: str, amount: float) -> None:
        """
        Used by MonoManager.set_user_pay_updates method
        """
        current_val = self.worksheet.acell(f"{column}{row}").value
        current_val = (
            0
            if current_val is None
            else float(current_val.replace(",", ".").replace("\xa0", ""))
        )
        future_val = current_val + amount

        self.worksheet.update_acell(
            f"{column}{row}",
            future_val,
        )
