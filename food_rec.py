import requests, time, threading, sys, os, webbrowser
from threading import Thread
from bs4 import BeautifulSoup
from random import shuffle

class Restaurant():

    def __init__(self, name, address, categories, url):
        self.name = name
        self.address = address
        self.categories = categories
        self.url = url

def find_restaurant(url, location, cuisine):
    for page_num in range(10): #looks through the first ten pages of reviews (that are sorted by rating)
        reviewers = find_reviewers(url, page_num)
        for reviewer in reviewers:
            t = Thread(target=find_reviewers_reviews, daemon = True, args=(reviewer, location, cuisine, url))
            t.start()
    return "Sorry, we weren't able to find a restaurant that matches your search criteria. Please try again."

def find_reviewers(restaurant_url, page_num):
    url = restaurant_url + '?sort_by=rating_desc&start=' + str(page_num*20)
    reviews = find_restaurant_reviews(url)
    reviewers = []
    for review in reviews:
        if review.find(class_="i-stars i-stars--regular-5 rating-large"):
            reviewer_id = find_reviewer_id(review)
            reviewers.append(reviewer_id)
        elif four_stars_or_less(review):
            return reviewers
    return reviewers

def find_restaurant_reviews(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    review_list = soup.find(class_="review-list")
    reviews = review_list.find_all("li")
    return reviews

def find_reviewer_id(review):
    review_info = str((str(review.find_all('div'))).split("\n")[0])
    start = 'user_id:'
    end = '">'
    reviewer_id = review_info[(review_info.index(start)+len(start)):review_info.index(end)]
    return reviewer_id

def four_stars_or_less(review):
    return (review.find(class_="i-stars i-stars--regular-4 rating-large") or
            review.find(class_="i-stars i-stars--regular-3 rating-large") or
            review.find(class_="i-stars i-stars--regular-2 rating-large") or
            review.find(class_="i-stars i-stars--regular-1 rating-large"))

def find_reviewers_reviews(reviewer_id, desired_location, desired_cuisine, url):
    base_url = 'https://www.yelp.com/user_details_reviews_self?userid=' + reviewer_id + '&review_sort=rating&rec_pagestart='
    page_num = 0
    fivestar_reviews_left = True
    while fivestar_reviews_left:
        url = base_url + str(page_num)
        reviews = find_user_reviews(url)
        for review in reviews:
            restaurant_info = review.find(class_="media-story")
            if restaurant_info and review.find(class_="i-stars i-stars--regular-5 rating-large"):
                restaurant = make_restaurant_obj(restaurant_info)
                if fits_search_criteria(restaurant, desired_location, desired_cuisine, url):
                    print("We found a restaurant for you!")
                    print("Name: ", restaurant.name)
                    print("Address: ", restaurant.address)
                    print("Url: ", restaurant.url)
                    webbrowser.open(restaurant.url)
                    os._exit(1)
                    return restaurant
            elif four_stars_or_less(review):
                fivestar_reviews_left = False
        page_num += 10
    return None

def find_user_reviews(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    review_list = soup.find(class_= "user-details_reviews")
    reviews = review_list.find_all("li")
    return reviews

def make_restaurant_obj(restaurant_info):
    name = restaurant_info.find(class_ = "biz-name js-analytics-click").text
    url = 'https://www.yelp.com/' + restaurant_info.find(class_ = "biz-name js-analytics-click")['href']
    address = restaurant_info.find("address").text.replace("    ","")
    categories = restaurant_info.find_all(class_ = "category-str-list")
    category_list = []
    for category in categories:
        category = category.text.replace("\n                    ","")
        category = category.replace("\n","")
        category_list.append(category)
    restaurant = Restaurant(name, address, category_list, url)
    return restaurant

def fits_search_criteria(restaurant, desired_location, desired_cuisine, url):
    if desired_location in restaurant.address:
        for category in restaurant.categories:
            if desired_cuisine in category:
                if 'CLOSED' not in restaurant.name and restaurant.url != url:
                    return True
    return False

def main():
    print("Hi! Welcome to Restaurant Recommender. \
    This program is going to give you a restaurant recommendation based on \
    a restaurant you like and what type of food you're looking for. \n")

    restaurant_url = input("\nStep 1: Enter the Yelp url of a restaurant you like: ")
    desired_location = input("\nStep 2: Enter what city or state you want to find restaurants in: ")
    desired_cuisine = input("\nStep 3: Enter the type of food you're looking for: ")

    print("\nOk, the program is now finding you your new favorite restaurant! This might take a few minutes. \n")
    print(find_restaurant(restaurant_url, desired_location, desired_cuisine))

if __name__ == '__main__':
    main()
