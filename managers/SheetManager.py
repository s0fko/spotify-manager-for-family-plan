from math import ceil

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

    def get_debtors_message(self, usd_rate_sell: float) -> str:
        table = self.worksheet.batch_get(["D1:G2"])[0]

        message = config.DEBTORS_MESSAGE_UA
        month_payment_uah = (usd_rate_sell * 7.99) / 6

        debtors_exists = False
        for i in range(len(table[0])):
            balance = float(table[1][i].replace(",", "."))

            if float(balance) < month_payment_uah:
                debtors_exists = True
                message += config.DEBTORS_DEBT_MESSAGE_UA.format(
                    name=table[0][i],
                    balance=balance,
                    pay=ceil(month_payment_uah - balance),
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

    def get_users_list(self) -> list:
        return self.worksheet.batch_get(["B1:G1"])[0][0]
