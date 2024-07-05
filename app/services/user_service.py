import pandas as pd
from app.api.schemas import UserData
from app import config
from app.utils.helpers import filter_by_intervals, filter_by_feature
from .similarity_service import sort_users_by_cosine_similarity, filter_users_by_interest
import logging 

logger = logging.getLogger("user_service")


def process_user_data(user_data: UserData, data: pd.DataFrame) -> pd.DataFrame:
    """
    Process the user data for profile computation.

    Args:
    user_data (UserData): The user data received from the API.

    Returns:
    dict: A dictionary containing the processed results or status.
    """
    try:
        # Perform processing logic here.
        logger.info( "Processing user data start with %d data points ", len(data))
        ## filters by age
        data = filter_by_intervals(data, user_data.age, config.age_column)
        data = filter_by_feature(data, user_data.age_group, config.age_group_name_column)

        logger.info( "Remaining data points after filtering by age %d", len(data))

        ## filters by city and region
        data = filter_by_feature(data, user_data.city, config.city_column)
        data = filter_by_feature(data, user_data.region, config.region_column)

        logger.info( "Remaining data points after filtering by city and region %d", len(data))

        ## filter by gender
        data = filter_by_feature(data, user_data.gender, config.gender_column)

        logger.info( "Remaining data points after filtering by gender %d", len(data))

        ## filters by income
        data = filter_by_intervals(data, user_data.income, config.income_column)
        data = filter_by_feature(data, user_data.income_group, config.income_quintile_name_column)

        logger.info( "Remaining data points after filtering by income %d", len(data))

        ## filters by occupation
        data = filter_by_feature(data, user_data.occupation, config.occupation_column)
        data = filter_by_feature(data, user_data.occupation_category, config.occupation_category_column)

        logger.info( "Remaining data points after filtering by occupation %d", len(data))

        data = handle_interest_profile(user_data, data)
        if user_data.n_users and isinstance(user_data.n_users, int):
            data = data[:user_data.n_users]
        
        if len(data) == 0:
            return "Please use more easier limitations."
        return data
    except Exception as e:
        logger.info("An error occurred: %s", e)
        return None


def handle_interest_profile(user_data: UserData, data: pd.DataFrame) -> str:
    confidence_level = user_data.confidence_level
    if not confidence_level:
        confidence_level = "Low"

    number_of_users = user_data.n_users 
    if not number_of_users:
        number_of_users = config.n_return_users_default

    random_users_percent = user_data.random_user_percent
    if not random_users_percent:
        random_users_percent = config.random_users_percent_default

    random_users_percent = random_users_percent / 100
    
    if user_data:
        if len(user_data.interest.interests) == 1:
            data = filter_users_by_interest(data, user_data.interest.interests[0], confidence_level, num_users=number_of_users, add_random=random_users_percent)
        elif len(user_data.interest.interests) > 1:
            interest_profile = pd.Series(data=user_data.interest.weights, index=user_data.interest.interests)
            data = sort_users_by_cosine_similarity(data, interest_profile)
        
    return data[:number_of_users]