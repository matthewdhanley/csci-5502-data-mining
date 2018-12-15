from business_to_txt import *
import pandas as pd
import datetime as dt
import csv
import numpy as np

# GLOBAL PARAMETERS
BUSINESS_CSV_FILE = 'D:\\home\\mhanl\\data_mining\\project\\yelp_dataset\\csv\\cities\\business_las_vegas.csv'
REVIEW_CSV_FILE = 'D:\\home\\mhanl\\data_mining\\project\\yelp_dataset\\csv\\review.csv'


def get_dates(business_id, review_df):
    """
    Gets all the dates of the reviews for a given business_id
    :param business_id: string with unique business id
    :param review_df: dataframe containing all reviews
    :return: list containing all the dates for specified business id
    """
    reviews_df = review_df[review_df['business_id'] == business_id]
    if reviews_df.empty:
        dates = []
        stars = []
        reviews = []
    else:
        dates = reviews_df['date'].tolist()
        stars = reviews_df['stars'].tolist()
        reviews = reviews_df['text'].tolist()

    return dates, stars, reviews


def get_dates_3mo(business_id, review_df):
    """
    Gets all the dates of the reviews for a given business_id
    :param business_id: string with unique business id
    :param review_df: dataframe containing all reviews
    :return: list containing all the dates for specified business id
    """
    reviews_df = review_df[review_df['business_id'] == business_id]
    if reviews_df.empty:
        dates = []
        stars = []
        reviews = []
    else:
        dates = reviews_df['date'].tolist()
        stars = reviews_df['stars'].tolist()
        reviews = reviews_df['text'].tolist()

    dates = to_dt(dates)
    min_date = min(dates)
    return_dates = []
    return_stars = []
    return_reviews = []
    for i in range(0, len(dates)):
        if (dates[i] - min_date).days//7 > 4:
            continue
        return_dates.append(dates[i])
        return_stars.append(stars[i])
        return_reviews.append(reviews[i])

    return return_dates, return_stars, return_reviews


def calc_review_variance(reviews):
    """
    Calculates variance of review length
    :param reviews: array of reviews
    :return: variance of review length
    """
    review_len = [len(x) for x in reviews]
    return np.var(np.array(review_len))


def get_success_stats(business, restaurant_df):
    """
    Gets success statistics of business
    :param business: business id of specific business
    :param restaurant_df: dataframe of business information
    :return: stars of business, number of reviews, if it is open
    """
    business_info = restaurant_df.loc[restaurant_df['business_id'] == business]
    star = float(business_info['stars'])
    num_reviews = int(business_info['review_count'])
    is_open = int(business_info['is_open'])
    return star, num_reviews, is_open


def evaluate_success(stars, reviews, is_open, age):
    """
    Evaluates success based on our criteria
    :param stars: number of stars
    :param reviews: number of reviews
    :param is_open: bool for if the restaurant is open
    :param age: age in years of the restaurant
    :return: bool of success
    """
    if not is_open and age < 4.5:
        return False
    if reviews < 20:
        return False
    if stars < 3.5:
        return False
    return True


def calc_average_review_length(reviews):
    """
    calculates average review length
    :param reviews: list of reviews
    :return: average length
    """
    length = 0
    for review in reviews:
        length += len(review)
    return length/len(reviews)


if __name__ == "__main__":

    # load in the file
    print('reading in business data . . .')
    business_data = pd.read_csv(BUSINESS_CSV_FILE)

    # grab all the frames with "Restaurants" category
    print('getting restaurants . . .')
    restaurant_df = get_restaurants(business_data)

    # free up the business data dataframe. Only need to safe restaurants
    del business_data

    print('reading in reviews . . .')
    # load the reviews into memory. this takes a while
    review_data = pd.read_csv(REVIEW_CSV_FILE)

    # Get all the business IDs
    print("getting business ids...")
    business_ids = get_all_business_ids(restaurant_df)
    min_date = dt.datetime(2019, 1, 1)
    # Initialize file number

    print("opening file")
    f = open('business_success_long.csv', mode='w')
    success_writer = csv.writer(f, delimiter=',')

    cols = ['business_id', 'first_review', 'review_count', 'age', 'stars', 'is_open', 'successful',
            'num_in_4_weeks', 'num_in_8_weeks', 'first_4_week_review', 'first_8_week_review',
            'average_review_length', 'review_length_variance']

    out_df = pd.DataFrame(columns=cols)
    counter = 0
    for business in business_ids:
        # grab a list of all the reviews
        dates, stars_reviews, reviews = get_dates_3mo(business, review_data)

        if not dates:
            continue

        avg_review_length = calc_average_review_length(reviews)
        review_length_variance = calc_review_variance(reviews)
        # print(avg_review_length)

        min_date_tmp = min(dates)
        age = dt.datetime.now() - min_date_tmp
        four_week_counter = 0
        four_week_stars = 0
        eight_week_counter = 0
        eight_week_stars = 0
        for date, star in zip(dates, stars_reviews):
            if (date - min_date_tmp).days//7 <= 4:
                four_week_counter += 1
                four_week_stars += star
            if (date - min_date_tmp).days // 7 <= 8:
                eight_week_counter += 1
                eight_week_stars += star

        stars, num_reviews, is_open = get_success_stats(business, restaurant_df)
        success = evaluate_success(stars, num_reviews, is_open, age.days/365.25)

        data = [{'business_id': business,
                 'first_review': min_date_tmp.strftime("%Y-%m-%d"),
                 'review_count': num_reviews,
                 'age': age.days/365.25,
                 'stars': stars,
                 'is_open': str(is_open),
                 'success': success,
                 'num_in_4_weeks': four_week_counter,
                 'num_in_8_weeks': eight_week_counter,
                 'first_4_week_review': four_week_stars/four_week_counter,
                 'first_8_week_review': eight_week_stars/eight_week_counter,
                 'average_review_length': avg_review_length,
                 'review_length_variance': review_length_variance}]

        tmp_df = pd.DataFrame(data, columns=cols)
        out_df = out_df.append(tmp_df)
        counter += 1
        print(counter/len(business_ids)*100)
    with open('features_df_3mo.pi', 'wb') as handle:
        print("writing to pickle")
        pickle.dump(out_df, handle)
    out_df.to_csv('plz_dont_break.csv')

    f.close()
    print("done")
