import pandas as pd
import logging
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from app import config

logger = logging.getLogger("similarity_service")


def get_lower_confidence_level(current_level):
    """
    Get the next lower confidence level.
    """
    levels = config.confidence_level_list
    current_index = levels.index(current_level)
    if current_index < len(levels) - 1:
        return levels[current_index + 1]
    else:
        return "Low"


def add_random_users(df: pd.DataFrame, num_random_users: int, confidence_level: str, interest: str) -> pd.DataFrame:
    """
    Add random users based on the specified proportions from lower confidence levels or users without interactions.

    Parameters:
    - df (pd.DataFrame): DataFrame containing user data and interest scores.
    - num_random_users (int): Number of random users to add.
    - confidence_level (str): The current confidence level.
    - interest (str): The column name for the specific interest.

    Returns:
    - pd.DataFrame: DataFrame with added random users.
    """
    # Determine number of users to add from each lower confidence level
    num_one_level_lower = int(num_random_users * 0.5)
    num_two_levels_lower = int(num_random_users * 0.3)
    num_no_interaction = num_random_users - num_one_level_lower - num_two_levels_lower
    random_users_df = pd.DataFrame()

    # Determine lower confidence levels
    lower_confidence_1 = get_lower_confidence_level(confidence_level)
    lower_confidence_2 = get_lower_confidence_level(lower_confidence_1)

    # Get DataFrames for each level
    df_lower_1 = filter_users_by_interest(df, interest, lower_confidence_1, num_one_level_lower, add_random=None)
    df_lower_2 = filter_users_by_interest(df, interest, lower_confidence_2, num_two_levels_lower, add_random=None)
    df_no_interaction = df[df[config.interation_columns].sum(axis=1) == 0]

    # Sample users from each level
    if num_one_level_lower > 0:
        random_users_df = pd.concat([random_users_df, df_lower_1.sample(num_one_level_lower, replace=True)])

    if num_two_levels_lower > 0:
        random_users_df = pd.concat([random_users_df, df_lower_2.sample(num_two_levels_lower, replace=True)])

    if num_no_interaction > 0:
        if not df_no_interaction.empty:
            random_users_df = pd.concat([random_users_df, df_no_interaction.sample(num_no_interaction, replace=True)])
        else:
            random_users_df = pd.concat([random_users_df, df_lower_2.sample(num_no_interaction, replace=True)])

    logger.info("Number of added user from one lower confidence level %d", len(df_lower_1))
    logger.info("Number of added user from two lower confidence level %d", len(df_lower_2))
    logger.info("Number of added user who do not have any interaction %d", len(df_no_interaction))

    return random_users_df



def filter_users_by_interest(df: pd.DataFrame, interest: str, confidence_level: str, 
                             num_users: int, add_random: float|None) -> pd.DataFrame:
    """
    Filter users based on interest and confidence level using predefined interest columns.

    Parameters:
    - df (pd.DataFrame): DataFrame containing user data and interest scores.
    - interest (str): The column name for the specific interest to filter by (must be one of the predefined interests).
    - confidence_level (str): The confidence level ('very high', 'high', 'good', 'mid', 'low').
    - num_users (int): Number of users to return.
    - add_random (float, optional): Proportion of random users to add (0 to 1). Defaults to None.

    Returns:
    - pd.DataFrame: Filtered DataFrame based on the given confidence level.
    """
    # Predefined interest columns
    interest_columns = config.interests_columns

    if interest not in interest_columns:
        raise ValueError(f"Interest must be one of {interest_columns}")

    sorting_col = f"{interest}_interaction"

    # Base filtering based on confidence level
    if confidence_level == "Very High":
        conditions = (df[interest] > 0) & (df[[col for col in interest_columns if col != interest]].le(0).all(axis=1))
        filtered_df = df[conditions].sort_values(by=sorting_col, ascending=False)

    elif confidence_level == "High":
        max_interest = df[interest_columns].idxmax(axis=1)
        conditions = (df[interest] > 0) & (max_interest == interest)
        filtered_df = df[conditions].sort_values(by=sorting_col, ascending=False)

    elif confidence_level == "Good":
        filtered_df = df[df[interest] > 0].sort_values(by=sorting_col, ascending=False)

    elif confidence_level == "Mid":
        filtered_df = df[df[interest] >= 0].sort_values(by=sorting_col, ascending=False)

    elif confidence_level == "Low":
        filtered_df = df.sort_values(by=sorting_col, ascending=False)

    else:
        raise ValueError("Invalid confidence level. Choose from 'Very high', 'High', 'Good', 'Mid', 'Low'.")

   # Add random users if specified
    if add_random is not None:
        num_random_users = int(num_users * add_random)
        random_users_df = add_random_users(df, num_random_users, confidence_level, interest)
        logger.info("Number of random users %d", len(random_users_df))
        logger.info("Number of filtered users before adding random users %d", len(filtered_df))
    
        # Trim the filtered_df to leave space for random users
        filtered_df_temp = filtered_df[:(num_users - num_random_users)]
        logger.info("Number of filtered users after reserving space for random users %d", len(filtered_df_temp))
    
        # Combine filtered_df and random_users_df, then drop duplicates
        combined_df = pd.concat([filtered_df_temp, random_users_df]).drop_duplicates().reset_index(drop=True)
        logger.info("Number of users after adding random users and dropping duplicates %d", len(combined_df))
    
        # Calculate shortfall and add more users from the filtered_df if needed
        shortfall = num_users - len(combined_df)
        if shortfall > 0:
            additional_users = filtered_df[len(filtered_df_temp):(len(filtered_df_temp) + shortfall)]
            combined_df = pd.concat([combined_df, additional_users]).drop_duplicates().reset_index(drop=True)
            logger.info("Number of users after filling shortfall %d", len(combined_df))

        filtered_df = combined_df

        logger.info("Number of targeted users after final processing %d", len(filtered_df))

    return filtered_df.head(num_users)


def sort_users_by_cosine_similarity(df: pd.DataFrame, interest_profile: pd.Series) -> pd.DataFrame:
    """
    Sorts users based on the cosine similarity between their interest scores and a given interest profile
    using Scikit-learn's cosine_similarity function. In case of ties in similarity, it sorts based on the weights
    in the interest profile from highest to lowest.

    Parameters:
    - df (pd.DataFrame): DataFrame containing user data and interest scores.
    - interest_profile (pd.Series): A Series where the index corresponds to interest columns and the values sum to 1,
                                    representing the target profile to compare against.

    Returns:
    - pd.DataFrame: DataFrame sorted by similarity to the interest profile, highest similarity first,
                    and by descending weights of interest in the event of ties.
    """

    # Ensure that the sum of the profile values is 1
    if not np.isclose(interest_profile.sum(), 1):
        raise ValueError("The sum of the interest profile values must be 1.")

    # Extract the interest columns
    interest_columns = config.interests_columns

    # Get user interests and the profile in the correct shape
    user_interests = df[interest_columns].values
    profile_array = interest_profile.values.reshape(1, -1)

    # Calculate cosine similarities
    similarities = cosine_similarity(user_interests, profile_array).flatten()

    # Add similarity scores to the DataFrame
    df['similarity'] = similarities

    # Create a list of columns sorted by the weight in the interest profile
    sorted_interests = interest_profile.sort_values(ascending=False).index.tolist()

    # Sort by similarity score (descending), and by interest weights in descending order as tiebreakers
    sorted_df = df.sort_values(by=['similarity'] + sorted_interests, ascending=[False] + [False] * len(sorted_interests))

    return sorted_df