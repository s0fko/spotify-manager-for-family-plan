from datetime import datetime
from math import ceil
from typing import List

import gspread
from oauth2client.service_account import ServiceAccountCredentials

import config


class SheetManager:
    credentials = ""
    client = ""
    worksheet = ""

    def __init__(self, credentials: str, scope: list) -> None:
        """Initialize the SheetManager with Google Sheets API credentials and scope.

        Keyword arguments:
        credentials -- path to the JSON keyfile for Google service account
        scope -- list of strings representing the authorization scopes
        """
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            credentials,
            scope,
        )
        self.client = gspread.authorize(self.credentials)
        self.worksheet = self.client.open(config.TABLE_NAME).worksheet(
            config.SHEET_NAME
        )

    def __update_payment_value(self, column: str, row: str, amount: float) -> None:
        """Update the payment value in the specified cell by adding the given amount.

        Keyword arguments:
        column -- column letter of the cell to be updated
        row -- row number of the cell to be updated
        amount -- amount to be added to the existing value in the cell or 0 if it is empty
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

    def get_debtors_message(self, usd_rate_sell: float) -> str:
        """Generate a message listing the debtors based on their balances and current USD rate.

        Keyword arguments:
        usd_rate_sell -- the current selling rate of USD to calculate the payment in UAH

        Returns:
        A formatted message with the list of debtors and link to jar or a message stating no debtors
        """
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
            message += "\n" + config.JAR_LINK

        return message

    def set_month_charge_row(self, row: str, user_charges: List[dict]) -> None:
        """Set the monthly charge row in the spreadsheet and update user charges.

        Keyword arguments:
        row -- the row number where the month charges will be updated
        user_charges -- list of dictionaries containing user names and their corresponding charges
        """
        # format cells to grey
        self.worksheet.format(
            f"A{row}:H{row}",
            {
                "backgroundColor": {"red": 0.95, "green": 0.95, "blue": 0.95},
            },
        )

        # set month name to the first column
        self.worksheet.update_acell(
            f"A{row}",
            datetime.now().strftime("%b %Y"),
        )

        # set charge as new row in the table
        for charge in user_charges:
            column = config.USER_COLUMNS_MAPPING[charge["user"]]
            self.__update_payment_value(column, row, charge.get("amount"))

        # set control sum of Spotify charge
        self.worksheet.update_acell(
            f"H{row}",
            f"=SUM(B{row}:G{row})",
        )

    def get_users_list(self) -> list:
        """Retrieve the list of users from the spreadsheet.

        Returns:
        A list of user names from the specified range in the spreadsheet
        """
        return self.worksheet.batch_get(["B1:G1"])[0][0]
