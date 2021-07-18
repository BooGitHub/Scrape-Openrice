import requests
from bs4 import BeautifulSoup

x = {
    #"Host": "www.openrice.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

url = "https://www.openrice.com/en/hongkong/restaurants/district/chai-wan"
response = requests.get(
    url,
    headers=x
)

soup = BeautifulSoup(response.text, "html.parser")
soup.find_all("ul")
ul = soup.find_all("ul", class_="sr1-listing-content-cells pois-restaurant-list js-poi-list-content-cell-container")[0]
lis = ul.select("li.sr1-listing-content-cell")

all_comments = []

# loop all restaurant
for li in lis:
    shop_id = li.select("[data-poi-id]")[0]['data-poi-id']
    shop_name = li.select(".title-name")[0].text.strip()
    address = li.select(".address span")[0].text.strip()
    price = li.select(".icon-info-food-price")[0].text.strip()
    like = li.select(".smile-face .score")[0].text.strip()
    link = li.select_one(".title-name>a")["href"]
    print(link)

    response_reviews = requests.get(
        "https://www.openrice.com/" + link + "/reviews",
        headers=x
    )

    views = BeautifulSoup(response_reviews.text, "html.parser")
    comments_container = views.select_one(".js-sr2-review-main.sr2-review-main")
    comments = comments_container.select(".sr2-review-list-container")
    print(len(comments))
    # Loop comments in one shop

    for comment in comments:
        content = comment.select_one(".content-full .review-container")
        photos = content.select("a.photo")
        for photo in photos:
            photo.decompose()
        all_comments.append([shop_id, content.text.replace("\n", "").strip().replace("\n", "")])

        #print(comments_of_oneshop)



import pandas as pd
pd.DataFrame(all_comments).to_csv("Testing1")