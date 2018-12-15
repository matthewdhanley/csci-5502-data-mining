from business_to_txt import *
import pandas as pd

# WRITES REVIEWS TO FILE FOR EACH BUSINESS IN GIVEN DATASET

# GLOBAL PARAMETERS
BUSINESS_CSV_FILE = 'D:\\home\\mhanl\\data_mining\\project\\yelp_dataset\\csv\\cities\\business_las_vegas.csv'
REVIEW_CSV_FILE = 'D:\\home\\mhanl\\data_mining\\project\\yelp_dataset\\csv\\review.csv'


def extract_business_reviews(business_ids, review_df):
    for bid in business_ids:
        reviews_df = review_df[review_df['business_id'] == bid]
        df_to_csv(reviews_df, 'reviews_by_business_id/'+str(bid)+'.csv')


def df_to_csv(df, csv_path):
    df.to_csv(csv_path)


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

    print('extracting business ids . . .')
    # Get all the business IDs
    business_ids = get_all_business_ids(restaurant_df)

    print('extracting all reviews for relevant restaurants . . .')
    extract_business_reviews(business_ids, review_data)

    print('done.')

