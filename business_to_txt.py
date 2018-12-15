import pandas as pd
import re
import datetime as dt
from pprint import pprint
from extract_review_metadata import *
import pickle

# GLOBAL PARAMETERS
BUSINESS_CSV_FILE = 'D:\\home\\mhanl\\data_mining\\project\\yelp_dataset\\csv\\cities\\business_las_vegas.csv'
REVIEW_CSV_FILE = 'D:\\home\\mhanl\\data_mining\\project\\yelp_dataset\\csv\\review.csv'

# LIST OF CHARACTERS/WORDS THAT WILL BE STRIPPED FROM RESULTING TEXT
STRIPPED_REGEX = ['\s*,\s*',
                  ' a ', ' and ', ' or ', ' the ', '\s{2+}', '\s*~\s*', '\s*"\s*',
                  ' in ', ' I ', ' we ', ' at ', ' my ', ' on ', ' of ', ' so* ',
                  ' us ', ' is ', ' was ', '\s*/\s*', ' had ', ' their ', ' were ',
                  ' to ', ' beat ', ' that ', ' it ', ' like ', ' goes ', ' not ', ' that ',
                  ' that\'s', ' be ', ' they ', ' an ', ' you ', ' it\'s ', ' i\'m ', ' have ',
                  ' has ', ' do ', ' for ', ' are ', ' can ', ' been ', ' as ', ' go ', ' one ',
                  ' out ', ' her ', ' his ', '\s*\:\s*', '\s*\(\s*', '\s*\)\s*', ' me ', ' makes* ', ' with ',
                  '\s*\&\s*', '\s*\-\s*', ' i\'ve ', ' get ', ' and\/or ', ' up ', ' by ', ' either ',
                  ' how ', ' this ', ' after ', ' here ', ' our ', ' got ', ' these ', ' from ',
                  ' will ', ' about ', ' what ', ' too ', '\s*;\s*', ' went ', ' who ', ' who\'s ', ' we\'ve ',
                  ' I\'ll ', ' where\'s ', ' him ', ' hers ', ' there ', ' than ', '\.', '\,', '\n']

# STRIPPED_REGEX = []


def get_restaurants(raw_business_df):
    """
    Extracts restaurants from business dataframe. Stirps all businesses without categories
    and looks for categories that match 'Restaurants'
    :param raw_business_df: pandas dataframe with all relevant business data
    :return: pandas dataframe with all restaurants
    """
    # strip the entries that don't have anything in the categories subset.
    business_data_clean_categories = raw_business_df.dropna(subset=['categories'])

    # grab all the frames with "Restaurants" category
    restaurant_data_frame = business_data_clean_categories[
        business_data_clean_categories['categories'].str.contains('Restaurants')]
    return restaurant_data_frame


def get_business_id(business_df, business_name):
    """
    Given a business name (string), return the id of the business
    :param business_df: pandas dataframe from yelp
    :param business_name: string for name of the business
    :return: business_id string
    """
    # try to match the name given
    found_business = business_df[business_df['name'] == business_name]
    if found_business.empty:
        print("ERROR, could not find business \""+business_name+"\"")
        exit(-1)
    return found_business['business_id'].iloc[0]


def concat_reviews(reviews):
    """
    Combines all reviews in list into one large string
    :param reviews: list of reviews
    :return: string containing all the reviews
    """
    large_review = ''
    for review in reviews:
        large_review +=  review + '\n<EOR>\n'

    return large_review


def get_all_business_ids(business_df):
    """
    Gets a list of all the business ids
    :param business_df: pandas dataframe from yelp
    :return: list with business_id strings
    """
    return business_df['business_id'].tolist()


def get_reviews(business_id, review_df):
    """
    Gets all the reviews for a given business_id
    :param business_id: string with unique business id
    :param review_df: dataframe containing all reviews
    :return: list containing all the reviews for specified business id
    """
    reviews_df = review_df[review_df['business_id'] == business_id]
    if reviews_df.empty:
        reviews = []
        dates = []
    else:
        reviews = reviews_df['text'].tolist()
        dates = reviews_df['date'].tolist()
    return reviews, dates


def to_dt(dates):
    """
    Converts dates from yelp dataset to datetime object
    :param dates: list of dates
    :return: list of dt dates
    """
    dt_dates = []
    for date in dates:
        dt_dates.append(dt.datetime.strptime(date, '%Y-%m-%d'))
    return dt_dates


def write_reviews_to_file(review, file_num, star):
    """
    Writes to a file
    :param review: string to be written to the file
    :param file_num: number for the filename
    :return: None
    """
    f = open('reviews_3mo/'+str(file_num)+'.txt', 'w')
    try:
        f.write(review)
        f.write('\n\n'+'<stars>'+str(star)+'</stars>')
    except UnicodeEncodeError:
        print("Had an encoding error. Skipping for now.")
    f.close()


def strip_characters(in_text):
    for char in STRIPPED_REGEX:
        # run it though twice to get extra clean.
        in_text = re.sub(char, ' ', in_text, flags=re.IGNORECASE)
        in_text = re.sub(char, ' ', in_text, flags=re.IGNORECASE)
    return in_text


if __name__ == "__main__":

    # load in the file
    print("reading business files . . .")
    business_data = pd.read_csv(BUSINESS_CSV_FILE)

    # grab all the frames with "Restaurants" category
    print("sorting business files . . .")
    restaurant_df = get_restaurants(business_data)

    # free up the business data dataframe. Only need to safe restaurants
    del business_data

    # load the reviews into memory. this takes a while
    print("reading reviews . . .")
    review_data = pd.read_csv(REVIEW_CSV_FILE)

    # Get all the business IDs
    print("getting business ids . . .")
    business_ids = get_all_business_ids(restaurant_df)

    weeks = 12
    time_from_open = {}
    i = 0

    # Initialize file number
    bulk_reviews_number = 0
    for business in business_ids:
        # grab a list of all the reviews
        reviews, date = get_reviews(business, review_data)
        if not reviews:
            continue

        date = to_dt(date)

        if min(date) > dt.datetime(2016, 1, 1):
            # Only looking at businesses that are at least 3 years old
            continue

        # Sort reviews based on date
        reviews = [x for _, x in sorted(zip(date, reviews))]
        date = sorted(date)

        # Get stars for restaurant
        star, _, _ = get_success_stats(business, restaurant_df)

        tmp_reviews = []
        j = 0
        # Append reviews for first 12 weeks of business being open
        while j < len(date) and (date[j] - date[0]).days//7 < weeks:
            tmp_reviews.append(reviews[j])
            j += 1

        # combine the reviews into one string
        lump_review = concat_reviews(tmp_reviews)

        # Strip unnecessary words and characters
        lump_review = strip_characters(lump_review)

        # write the reviews to a file
        write_reviews_to_file(lump_review, business, star)

        i += 1
        # update on progress
        print(str(i/len(business_ids)*100)+'%')

    print("done")
