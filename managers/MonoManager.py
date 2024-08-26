import datetime
import time
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

    def get_current_month_spotify_charge(self) -> dict:
        """
        Return example:
        {'amount': -325.99, 'date': '2024-06-20'}
        """

        response = requests.get(
            f"https://api.monobank.ua/personal/statement/{config.MONO_ACCOUNT}/{self.__get_month_ago_timestamp()}",
            headers=self.headers,
        )
        data = response.json()

        result = {}
        for record in data:
            if record.get("description") == "Spotify":
                result["amount"] = abs(record.get("amount") / 100)
                result["date"] = datetime.datetime.fromtimestamp(
                    record.get("time")
                ).strftime("%Y-%m-%d")
                break

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
            return "Моно не десть дістати виписку за 30 днів+"

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

        return "Зарахування на банку внесені"
