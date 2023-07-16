from helpers import get_utc_now_string


def get_sitemap_index_url(conn) -> list[tuple]:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id
            , url
        FROM hms_beagle.urls 
        WHERE url_type = 'sitemap'
        LIMIT 1
        """
    )
    queryset = cursor.fetchall()
    return queryset


def get_mens_synchilla_urls(conn) -> list[tuple]:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT hbu.id
            , hbu.url
            , hbp.id
        FROM hms_beagle.urls AS hbu
        INNER JOIN hms_beagle.products AS hbp
            ON hbu.product_id = hbp.id
        WHERE hbu.url_type = 'product'
            AND hbu.url_active = true
            AND hbp.group = 'synchilla' 
            AND hbp.gender = 'M'
        """
    )
    queryset = cursor.fetchall()
    return queryset


def update_url_activity(conn, url: str, is_active: bool) -> None:
    cursor = conn.cursor()
    print(f"Updating {url} to url_active {is_active}")
    cursor.execute(
        """
        UPDATE hms_beagle.urls
        SET url_active = %s
        WHERE url = %s
        """,
        [is_active, url],
    )
    conn.commit()
    return


def insert_product_url(conn, url: str, product_id: int) -> None:
    cursor = conn.cursor()
    print(f"Inserting {url} for product_id {product_id}")
    cursor.execute(
        """
        INSERT INTO hms_beagle.urls(
            url
            , url_type
            , url_active
            , product_id
        )
        VALUES (%s,%s,%s,%s,)
        """,
        [url, "product", True, product_id],
    )
    conn.commit()
    return


def insert_scraped_data(conn, scraped_data: list[dict]) -> None:
    cursor = conn.cursor()
    print("Inserting stock data")
    for data in scraped_data:
        data["insert_timestamp"] = get_utc_now_string()
        cursor.execute(
            """
            INSERT INTO hms_beagle.product_stock_data(
                color
                , color_code
                , sizes_in_stock
                , medium_in_stock
                , scraped_from_url
                , scrape_run_time
                , insert_timestamp
                , product_id
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            [
                data["color"],
                data["color_code"],
                data["sizes_in_stock"],
                data["medium_in_stock"],
                data["scraped_from_url"],
                data["scrape_run_time"],
                data["insert_timestamp"],
                data["product_id"],
            ],
        )
        conn.commit()
    return
