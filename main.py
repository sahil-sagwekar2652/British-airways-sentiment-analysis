import re
import requests
from bs4 import BeautifulSoup, SoupStrainer

URL = "https://www.airlinequality.com/airline-reviews/british-airways/page/page_no/?sortby=post_date%3ADesc&pagesize=100"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 OPR/86.0.4363.59",
    "Accept-Language": "en-US,en;q=0.9"
}

filename = input("Save data as (filename.extension): ")
while not filename:
    print("Invalid filename.")
    filename = input("Save data as (filename.extension): ")

with open(filename, 'w') as file:
    file.write("rating,header,customer_country,date,review,Aircraft,Type of Traveller,Seat Type,Route,Date Flown,Seat Comfort,Cabin Staff Service,Food & Beverages,Inflight Entertainment,Ground Service,Wifi & Connectivity,Value For Money,Recommended\n")

    for i in range(1, 37):
        response = requests.get(url=URL.replace('page_no', str(i)), headers=headers)
        articles = SoupStrainer("article", class_=re.compile("list-item"))
        soup = BeautifulSoup(response.text, 'html.parser', parse_only=articles)
        articles = soup.find_all('article')

        for article in articles:
            rating = article.find('div', class_="rating-10").get_text().strip().split("/")[0]
            header = article.find('h2', class_="text_header").string.replace(",", "")

            try:
                cust_details1 = article.find('h3', class_="text_sub_header").get_text().strip().split("(")
                customer_country = cust_details1[1].split(") ")[0]
                date = cust_details1[1].split(") ")[1]
            except (AttributeError, IndexError):
                customer_country, date = '', ''

            try:
                review = article.find('div', class_="text_content").get_text().split(" |")[1].strip().replace(",", "")
            except IndexError:
                review = article.find('div', class_="text_content").get_text().strip().replace(",", "")

            my_dict = {
                "rating": rating,
                "header": header,
                "customer_country": customer_country,
                "date": date,
                "review": '"'+review+'"',
                "Aircraft": '',
                "Type Of Traveller": '',
                "Seat Type": '',
                "Route": '',
                "Date Flown": '',
                "Seat Comfort": '',
                "Cabin Staff Service": '',
                "Food & Beverages": '',
                "Inflight Entertainment": '',
                "Ground Service" : '',
                "Wifi & Connectivity" : '',
                "Value For Money" : '',
                "Recommended": ''
                }

            article = BeautifulSoup(str(article), 'html.parser')

            for i in article.find_all('td', 'review-value'):
                my_dict[i.previousSibling.get_text()] = i.get_text()

            for j in article.find_all('td', 'review-rating-stars'):
                my_dict[j.parent.find('td', 'review-rating-header').get_text()] = str(len(j.parent.find_all('span', class_="fill")))

            try:
                print(",".join(str(value) for value in my_dict.values()), file=file)
            except UnicodeEncodeError:
                pass
