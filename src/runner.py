from scrape_stock_data import scrape_mens_synchilla_stock_data
from examine_stock_data import (
    get_recent_mens_medium_synchilla_stock_data,
    examine_stock_data,
)
from helpers import connect_to_db


if __name__ == "__main__":
    conn = connect_to_db()
    scrape_mens_synchilla_stock_data(conn)
    recent_mens_medium_synchilla_stock_data = (
        get_recent_mens_medium_synchilla_stock_data(conn)
    )
    examine_stock_data(recent_mens_medium_synchilla_stock_data)
    conn.close()
