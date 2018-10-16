import requests, re
from bs4 import BeautifulSoup

def find_restaurants_five_star_reviewers(restaurant):
    restaurant = 'genki-ya-brookline-brookline-2' #change this
    fivestar_reviews_left = True
    reviewer_list = []
    base_url = 'https://www.yelp.com/biz/' + restaurant + '?sort_by=rating_desc'
    url = base_url
    page_num = 0

    while fivestar_reviews_left:
        page = requests.get(url)
        reviews = find_reviews_on_page(page)
        for review in reviews:
            if review.find(class_="i-stars i-stars--regular-5 rating-large"):
                reviewer_id = find_reviewer_id(review)
                reviewer_list.append(reviewer_id)
            elif review.find(class_="i-stars i-stars--regular-4 rating-large"):
                fivestar_reviews_left = False
        page_num += 1
        page_url = str(page_num*20)
        url = base_url + "&start=" + page_url
        return reviewer_list

def find_reviews_on_page(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    review_list = soup.find(class_="review-list")
    reviews = review_list.find_all("li")
    return reviews

def find_reviewer_id(review):
    review_info = str((str(review.find_all('div'))).split("\n")[0])
    start = 'reviewer_id:'
    end = '">'
    reviewer_id = review_info[(review_info.index(start)+len(start)):review_info.index(end)]
    return reviewer_id



def find_reviewers_fivestar_reviews(reviewer_id):
    base_url = 'https://www.yelp.com/reviewer_details_reviews_self?reviewerid=' + reviewer_id + '&review_sort=rating&rec_pagestart='
    page_addon = '0'
    page_num = 0
    restaurant_list = []
    fivestar_reviews_left = True
    while fivestar_reviews_left:
        url = base_url + page_addon
        page = requests.get(url)
        reviews = find_reviews_on_page(page)
        for review in reviews:
            restaurant_info = review.find(class_="media-story")
            if restaurant_info:
                if review.find(class_="i-stars i-stars--regular-5 rating-large"):
                    find_review_address_and_categories(restaurant)
                else:
                    fivestar_reviews_left = False
        page_num += 1
        page_addon = str(page_num*10)

def find_review_address_and_categories(restaurant_info):
    address = restaurant_info.find("address").text
    categories = restaurant_info.find_all(class_ = "category-str-list")
    category_list = []
    for category in categories:
        category_list.append(category.text.strip)

reviewer_id = 'DWU7Mr8kb0y-eEdOcv_22Q'
find_reviewers_fivestar_reviews(reviewer_id)






















#hi
