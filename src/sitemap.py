from bs4 import BeautifulSoup
import requests
import re

from helpers import connect_to_db
from queries import get_sitemap_index_url, get_mens_synchilla_urls, insert_product_url


def add_new_mens_synchilla_fleece_urls_from_sitemap(conn) -> None:
    sitemap_index_queryset = get_sitemap_index_url(conn)
    sitemap_index = requests.get(sitemap_index_queryset[0][1])
    soup = BeautifulSoup(sitemap_index.content, "xml")
    sitemap_urls = soup.find_all("loc")
    for url in sitemap_urls:
        if "product" in url.text:
            product_sitemap_url = url.text
            break
    if product_sitemap_url:
        product_sitemap = requests.get(product_sitemap_url)
        soup = BeautifulSoup(product_sitemap.content, "xml")
        synchilla_fleece_urls = soup.find_all("loc", string=re.compile("synchilla-snap-t-fleece-pullover"))
        new_mens_synchilla_fleece_urls = []
        mens_synchilla_queryset = get_mens_synchilla_urls(conn)
        mens_synchilla_urls_db = [result[1] for result in mens_synchilla_queryset] # list[tuple] -> list[str]
        for url in synchilla_fleece_urls:
            if (re.search("^https://www.patagonia.com/product/mens", url.text) 
               and url.text not in mens_synchilla_urls_db):
                new_mens_synchilla_fleece_urls.append(url.text)
        if new_mens_synchilla_fleece_urls:
            # TODO: brittle, works since we're just looking at two variations of the snap-t fleece
            # TODO: optimize this solution, only acceptable since we expect small lists
            for new_url in new_mens_synchilla_fleece_urls:
                if "lightweight" in new_url:
                    for existing_record in mens_synchilla_queryset:
                        if "lightweight" in existing_record[1]:
                            insert_product_url(conn, new_url,existing_record[2])
                            break
                else:
                    for existing_record in mens_synchilla_queryset:
                        if "lightweight" not in existing_record[1]:
                            insert_product_url(conn, new_url,existing_record[2])
                            break
        else:
            print("No new Men's Synchilla Snap-T urls found in sitemap")
    else:
        raise ValueError("Product sitemap url not found in sitemap index")
    return

if __name__ == "__main__":
    conn = connect_to_db()
    add_new_mens_synchilla_fleece_urls_from_sitemap(conn)
    conn.close()