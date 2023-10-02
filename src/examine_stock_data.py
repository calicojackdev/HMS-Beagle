from sendgrid.helpers.mail.exceptions import SendGridException

from queries import (
    get_mens_medium_synchilla_stock_data_by_date,
    get_last_two_mens_synchilla_stock_data_insert_dates,
)
from helpers import connect_to_db
from notify import send_mail


def build_notification_message(new_stock_data: set) -> str:
    notifications = ["New stock data found:"]
    products = list(set([p[4] for p in new_stock_data]))
    for product in products:
        product_url = list(
            set(
                [
                    psd[3]
                    for psd in filter(lambda nsd: nsd[4] == product, new_stock_data)
                ]
            )
        )[0]
        product_colors = ", ".join(
            [psd[1] for psd in filter(lambda nsd: nsd[4] == product, new_stock_data)]
        )
        product_notification = (
            f"<a href='{product_url}'>{product}</a> | {product_colors}"
        )
        notifications.append(product_notification)
    return "<br>".join(notifications)


def get_recent_mens_medium_synchilla_stock_data(conn) -> dict[set]:
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
    recent_mens_medium_synchilla_stock_data = {
        "latest_stock_data": latest_mens_medium_synchilla_stock_data,
        "previous_stock_data": previous_mens_medium_synchilla_stock_data,
    }
    return recent_mens_medium_synchilla_stock_data


def examine_stock_data(recent_stock_data: dict[set]) -> set | None:
    latest_stock_data = recent_stock_data["latest_stock_data"]
    previous_stock_data = recent_stock_data["previous_stock_data"]
    new_stock_data = latest_stock_data.difference(previous_stock_data)
    if (latest_stock_data != previous_stock_data) and new_stock_data:
        notification_message = build_notification_message(new_stock_data)
        try:
            send_mail(notification_message)
        except SendGridException as sge:
            print(sge)
            print(notification_message)
    elif latest_stock_data == previous_stock_data:
        print("No new stock data found")
    return new_stock_data


if __name__ == "__main__":
    conn = connect_to_db()
    recent_mens_medium_synchilla_stock_data = (
        get_recent_mens_medium_synchilla_stock_data(conn)
    )
    examine_stock_data(recent_mens_medium_synchilla_stock_data)
    conn.close()
