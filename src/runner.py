from scrape_stock_data import scrape_mens_synchilla_stock_data
from examine_stock_data import examine_stock_data_for_new_mens_medium_synchilla_colors
from helpers import connect_to_db

if __name__ == "__main__":
    conn = connect_to_db()
    scrape_mens_synchilla_stock_data(conn)
    examine_stock_data_for_new_mens_medium_synchilla_colors(conn)
    conn.close()
