import pandas as pd

from app import config
from .preprocessing import helpers


def load_and_preprocess():
    """
    Load data from CSV files, preprocess, and return the final DataFrame.
    """
    # Load data
    demographic_df = pd.read_csv(config.DEMOGRAPHIC_DATA_PATH)
    interaction_df = pd.read_csv(config.INTERACTION_DATA_PATH)

    user_interaction_df = helpers.process_user_data(demographic_df, interaction_df)

    user_interaction_df = helpers.categorize_age(user_interaction_df, config.age_column)
    
    user_interaction_df = helpers.city_mapping(user_interaction_df)

    user_interaction_df = helpers.occupation_mapping(user_interaction_df)

    user_interaction_df = helpers.categorize_income_quintiles(user_interaction_df)
    return user_interaction_df