from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

review_table = {
    'Name' : [],
    'Date Published' : [],
    "review" : [],
    "overall rating" : [],
    "Verified customer" : [],
    "type of travel": [],
    "wifi connectivity" : [],
    "Route": [],
    "Date of Travel" : [],
    "Seat Type" : [],
    "Seat Comfort": [],
    "Cabin Staff Service": [],
    "Food & Beverages": [],
    "Inflight Entertainment": [],
    "Ground Service": [],
    "Value For Money": []
}

def update_data(reviews):
    for review in reviews:
        reviewr_name = review.find("span", itemprop="name").text.strip() if review.find("span", itemprop="name") else "No Name"
        #review_table["Name"].append(reviewr_name)
        date_published = review.find("time", itemprop="datePublished").text.strip() if review.find("time", itemprop="datePublished") else ""
        
        review_head = review.find('h2',class_="text_header").text.strip() if review.find('h2',class_="text_header") else "No Header"
        
        ratings = review.find('span', itemprop="ratingValue").text.strip() if review.find('span', itemprop="ratingValue").text.strip() else "Nan"
        
        content_div = review.find('div', itemprop='reviewBody')
        verifiedOrNot = 'Verified' if content_div and content_div.find('em', text='Trip Verified') else 'Not Verified'
        
        rating_table = review.find('table', class_="review-ratings")
        if rating_table:
                rows = rating_table.find_all('tr')
                for row in  rows:
                        cells = row.find_all("td")
                        for cell in cells:
                                if "Type Of Traveller" in cell.text:
                                        typeOtravel = row.find('td', class_='review-value').text.strip()
                                        break
                                elif "Route" in cell.text:
                                        route_travelled = row.find('td',class_='review-value').text.strip()
                                        break
                                elif "Date Flown" in cell.text:
                                        Date_flown = row.find('td',class_='review-value').text.strip()
                                        break
                                elif "Seat Type" in  cell.text:
                                        Seat_type = row.find('td',class_='review-value').text.strip()
                                        break
                                elif "Seat Comfort" in cell.text:
                                        stars = row.find_all('span',class_="star fill")
                                        seat_comfort_stars = len(stars) if stars else None
                                        break
                                elif "Food & Beverages" in cell.text:
                                        stars = row.find_all('span', class_="star fill")
                                        food_beverages_stars = len(stars) if stars else None
                                        break
                                elif "Inflight Entertainment" in cell.text:
                                        stars = row.find_all('span', class_="star fill")
                                        inflight_entertainment_stars = len(stars) if stars else None
                                        break
                                elif "Ground Service" in cell.text:
                                        stars = row.find_all('span', class_="star fill")
                                        ground_service_stars = len(stars) if stars else None
                                        break
                                elif "Wifi & Connectivity" in cell.text:
                                        stars = row.find_all('span', class_="star fill")
                                        wifi_connectivity_stars = len(stars) if stars else None
                                        break
                                elif "Cabin Staff Service" in cell.text:
                                        stars = row.find_all('span', class_="star fill")
                                        Cabin_Staff_Service_stars = len(stars) if stars else None
                                        break
                                elif "Value For Money" in cell.text:
                                        stars = row.find_all('span', class_="star fill")
                                        value_for_money_stars = len(stars) if stars else None
                                        break
                                else:
                                    wifi_connectivity_stars =  None
                                    inflight_entertainment_stars = None
                                    food_beverages_stars = None
                                    Cabin_Staff_Service_stars = None
                                    ground_service_stars = None
                                    break
                                        
                                        
        else:
                print("i was unable to scrape this webpage")
        
        review_table["Name"].append(reviewr_name)
        review_table["Value For Money"].append(value_for_money_stars)
        review_table["wifi connectivity"].append(wifi_connectivity_stars)
        review_table["Cabin Staff Service"].append(Cabin_Staff_Service_stars)
        review_table["Ground Service"].append(ground_service_stars)
        review_table["Inflight Entertainment"].append(inflight_entertainment_stars)
        review_table["Food & Beverages"].append(food_beverages_stars)
        review_table["Seat Comfort"].append(Cabin_Staff_Service_stars)
        review_table["Seat Type" ].append(Seat_type)
        review_table["Date of Travel"].append(Date_flown)
        review_table["Route"].append("Route")
        review_table["type of travel"].append(typeOtravel)
        review_table["Verified customer"].append(verifiedOrNot)
        review_table["Date Published"].append(date_published)
        review_table["review"].append(review_head)
        review_table["overall rating"].append(ratings)


webpage = "https://www.airlinequality.com/airline-reviews/british-airways"

for i in range(1,3):
    d_webpage = f"https://www.airlinequality.com/airline-reviews/british-airways/page/{i}/"
    
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"} 
    response = requests.get(url=d_webpage, headers=headers) 
    print(i)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        
        reviews_section = soup.find('section', class_='layout-section layout-2 closer-top')
        reviews = reviews_section.find_all("article", itemprop="review")
        update_data(reviews)
    print(d_webpage)



data = pd.DataFrame(review_table)
print(data.head())
data.to_excel("British_Airlines_review.xlsx")
