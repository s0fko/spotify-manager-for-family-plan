import datetime
import random
import time
from math import floor
from typing import List, Tuple

import requests
from dateutil.relativedelta import relativedelta

import config

from . import SheetManager


class MonoManager:
    headers = {"X-Token": config.MONO_TOKEN}
    sheet_manager: SheetManager

    def __init__(self, sheet_manager: SheetManager):
        self.sheet_manager = sheet_manager

    @classmethod
    def __get_month_ago_timestamp(cls) -> str:
        one_month_ago = datetime.datetime.now() - relativedelta(days=30)
        return str(int(time.mktime(one_month_ago.timetuple())))

    @classmethod
    def get_usd_rate_sell(cls) -> float:
        """
        Returns 0< if request satisfied.
        Returns 0 if too many requests
        """

        response = requests.get("https://api.monobank.ua/bank/currency").json()

        if "errCode" in response:
            return 0.0

        for record in response:
            if (
                record.get("currencyCodeA") == 840
                and record.get("currencyCodeB") == 980
            ):
                return record.get("rateSell")

    @classmethod
    def __get_monobanka_statement(cls, from_time: str) -> Tuple[List[dict]]:
        """
        Valid description types:
            - 'Від: ' - paid
            - 'Додавання до банки' - income
        """

        response = requests.get(
            f"https://api.monobank.ua/personal/statement/{config.MONOBANKA_ID}/{from_time}",
            headers=MonoManager.headers,
        )
        data = response.json()
        paid, income = [], []

        for record in data:
            if record.get("description").startswith(config.DESCRIPTION_PAID_UA):
                paid.append(
                    {
                        "time": record.get("time"),
                        "from": record.get("description").replace(
                            config.DESCRIPTION_PAID_UA, ""
                        ),
                        "amount": float(record.get("amount") / 100),
                    }
                )
            elif record.get("description").startswith(config.DESCRIPTION_INCOME_UA):
                income.append(
                    {
                        "time": record.get("time"),
                        "amount": float(record.get("amount") / 100),
                    }
                )

        return paid, income

    @classmethod
    def __get_current_month_spotify_charge(cls) -> dict:
        """
        Return example:
        {'amount': -325.99, 'date': '2024-06-20'}
        """

        response = requests.get(
            f"https://api.monobank.ua/personal/statement/{config.MONO_ACCOUNT}/{MonoManager.__get_month_ago_timestamp()}",  # noqa: E501
            headers=MonoManager.headers,
        )
        data = response.json()

        result = {}
        for record in data:
            if record.get("description") == "Spotify":
                result["amount"] = abs(record.get("amount") / 100)
                result["date"] = record.get("time")
                break

        return result

    @classmethod
    def __get_user_charge_amounts(cls, users: list, amount: float) -> List[dict]:
        """
        Based on the last Spotify withdrawal record.
        Return example:
        [
            {'user': 'Софія', 'amount': -54.34},
            {'user': 'Саша', 'amount': -54.33}
        ]
        """

        base_user_amount = floor(amount / len(users) * 100) / 100
        remainder = round(amount - (base_user_amount * len(users)), 2)

        lucky = users.index(random.choice(users))

        result = []
        for i in range(len(users)):
            result.append(
                {
                    "user": users[i],
                    "amount": -round(base_user_amount + remainder, 2)
                    if i == lucky
                    else -base_user_amount,
                }
            )

        return result

    def set_user_pay_updates(self) -> str:
        """
        Set into Google Sheet user pays and incomes from the last period
        """

        # get time interval
        f = open(config.LAST_PAY_UPDATE_FILE_PATH, "r")
        from_time = int(f.readlines()[0])
        time_now = str(int(time.mktime(datetime.datetime.now().timetuple())))

        # check if operation can be proceeded
        thirty_days_ago = datetime.datetime.now() - datetime.timedelta(days=30)
        if datetime.datetime.fromtimestamp(from_time) < thirty_days_ago:
            return config.UPDATE_WAS_30_DAYS_AGO_MESSAGE_UA

        # get list of statemets
        paid, income = MonoManager.__get_monobanka_statement(from_time)

        # get row number to write
        f = open(config.CURRENT_ROW_TO_WRITE_FILE_PATH, "r")
        row = int(f.readlines()[0])

        # update cells
        for record in paid:
            nickname = config.USER_NAMES_MAPPING.get(record.get("from"))
            column = config.USER_COLUMNS_MAPPING.get(nickname)
            self.sheet_manager.update_users_cell(column, row, record.get("amount"))

        for record in income:
            column = config.ADMIN_USER_COLUMN
            self.sheet_manager.update_users_cell(column, row, record.get("amount"))

        # update last_pay_update
        f = open(config.LAST_PAY_UPDATE_FILE_PATH, "w")
        f.write(time_now)

        return config.PAY_UPDATE_SUCCESSFUL_MESSAGE_UA

    def set_user_charge(self) -> str:
        """
        Set into Google Sheet user charge for the current month
        """

        spotify_charge = MonoManager.__get_current_month_spotify_charge()

        # check if its time for the charge
        f = open(config.LAST_CHARGE_UPDATE_FILE_PATH, "r")
        last_charge_update = int(f.readlines()[0])
        newest_charge_update = int(spotify_charge["date"])
        if newest_charge_update <= last_charge_update:
            return config.NO_NEED_TO_WITHDRAWAL_MESSAGE_UA

        # get user charge amounts
        user_list = self.sheet_manager.get_users_list()
        if config.USERS_TO_SKIP_FROM_LUCKY_CHOOSE:
            for user in config.USERS_TO_SKIP_FROM_LUCKY_CHOOSE:
                user_list = [u for u in user_list if u != user]

        user_charges = MonoManager.__get_user_charge_amounts(
            user_list, spotify_charge["amount"]
        )

        # get row number to write
        f = open(config.CURRENT_ROW_TO_WRITE_FILE_PATH, "r")
        row = int(f.readlines()[0])

        self.sheet_manager.format_cells_to_grey(row + 1)

        # set month name to the first column
        self.sheet_manager.set_date_to_cell(row + 1)

        # set charge as new row in the table
        for charge in user_charges:
            column = config.USER_COLUMNS_MAPPING[charge["user"]]
            self.sheet_manager.update_users_cell(column, row + 1, charge.get("amount"))

        # set control sum of Spotify charge
        self.sheet_manager.set_sum_formula_to_row(row + 1)

        # update current_row_to_write
        f = open(config.CURRENT_ROW_TO_WRITE_FILE_PATH, "w")
        f.write(str(row + 2))

        # update last_charge_update
        f = open(config.LAST_CHARGE_UPDATE_FILE_PATH, "w")
        f.write(str(newest_charge_update))

        return config.SUCCESSFUL_WITHDRAWAL_MESSAGE_UA
