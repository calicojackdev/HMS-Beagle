# TODO: write tests, mock db data

from queries import (
    get_mens_medium_synchilla_stock_data_by_date,
    get_last_two_mens_synchilla_stock_data_insert_dates,
)
from helpers import connect_to_db


def examine_stock_data_for_new_mens_medium_synchilla_colors(conn) -> list:
    last_two_mens_synchilla_stock_data_insert_dates = (
        get_last_two_mens_synchilla_stock_data_insert_dates(conn)
    )
    latest_insert_date = last_two_mens_synchilla_stock_data_insert_dates[0][0]
    previous_insert_date = last_two_mens_synchilla_stock_data_insert_dates[1][0]
    latest_mens_medium_synchilla_stock_data = set(
        get_mens_medium_synchilla_stock_data_by_date(conn, latest_insert_date)
    )
    previous_mens_medium_synchilla_stock_data = set(
        get_mens_medium_synchilla_stock_data_by_date(conn, previous_insert_date)
    )
    if (
        latest_mens_medium_synchilla_stock_data
        != previous_mens_medium_synchilla_stock_data
    ) and latest_mens_medium_synchilla_stock_data.difference(
        previous_mens_medium_synchilla_stock_data
    ):
        print("New Medium Men's Synchilla stock data found:")
        for (
            new_mens_medium_synchilla_stock_data
        ) in latest_mens_medium_synchilla_stock_data.difference(
            previous_mens_medium_synchilla_stock_data
        ):
            print(
                f"{new_mens_medium_synchilla_stock_data[1]} | {new_mens_medium_synchilla_stock_data[3]}"
            )

    elif (
        latest_mens_medium_synchilla_stock_data
        == previous_mens_medium_synchilla_stock_data
    ):
        print("No new Men's Medium Synchilla stock data found")


if __name__ == "__main__":
    conn = connect_to_db()
    examine_stock_data_for_new_mens_medium_synchilla_colors(conn)
    conn.close()
