from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
from ast import literal_eval

from queries import get_mens_synchilla_urls, insert_scraped_data
from helpers import get_utc_now_string, check_url, connect_to_db


def scrape_mens_synchilla_stock_data(conn) -> None:
    mens_synchilla_queryset = get_mens_synchilla_urls(conn)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    for result in mens_synchilla_queryset:
        url_to_scrape = result[1]
        product_id = result[2]
        scrape_run_time = get_utc_now_string()
        scraped_data = []
        try:
            driver.get(url_to_scrape)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product-swatch"))
            )
            swatches = driver.find_elements(By.CSS_SELECTOR, ".product-swatch")
            for swatch in swatches:
                data = {}
                data["color"] = swatch.get_attribute("data-caption")
                data["color_code"] = swatch.get_attribute("data-color")
                data["sizes_in_stock"] = literal_eval(
                    swatch.get_attribute("data-size-stock")
                )
                if "M" in data["sizes_in_stock"]:
                    data["medium_in_stock"] = True
                else:
                    data["medium_in_stock"] = False
                data["scraped_from_url"] = url_to_scrape
                data["scrape_run_time"] = scrape_run_time
                data["product_id"] = product_id
                scraped_data.append(data)
            insert_scraped_data(conn, scraped_data)
        except TimeoutException:
            print(f"Timed out on {url_to_scrape}, checking if available...")
            check_url(url_to_scrape)
        time.sleep(5)  # let our bots not get ratelimited
    driver.close()
    return


if __name__ == "__main__":
    conn = connect_to_db()
    scrape_mens_synchilla_stock_data(conn)
    conn.close()
