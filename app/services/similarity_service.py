import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from app import config

import pandas as pd

def filter_users_by_interest(df: pd.DataFrame, interest: str, confidence_level: str):
    """
    Filter users based on interest and confidence level using predefined interest columns.

    Parameters:
    - df (pd.DataFrame): DataFrame containing user data and interest scores.
    - interest (str): The column name for the specific interest to filter by (must be one of the predefined interests).
    - confidence_level (str): The confidence level ('very high', 'high', 'good', 'mid', 'low').

    Returns:
    - pd.DataFrame: Filtered DataFrame based on the given confidence level.
    """
    # Predefined interest columns
    interest_columns = config.interests_columns

    if interest not in interest_columns:
        raise ValueError(f"Interest must be one of {interest_columns}")

    sorting_col = f"{interest}_interaction"
    
    if confidence_level == "Very High":
        # Very high confidence: only selected interest positive, all others <= 0
        conditions = (df[interest] > 0) & (df[[col for col in interest_columns if col != interest]].le(0).all(axis=1))
        return df[conditions].sort_values(by=sorting_col, ascending=False)
    
    elif confidence_level == "High":
        # High confidence: selected interest is the maximum and greater than zero
        max_interest = df[interest_columns].idxmax(axis=1)
        conditions = (df[interest] > 0) & (max_interest == interest)
        return df[conditions].sort_values(by=sorting_col, ascending=False)
    
    elif confidence_level == "Good":
        # Good confidence: selected interest greater than zero
        return df[df[interest] > 0].sort_values(by=sorting_col, ascending=False)
    
    elif confidence_level == "Mid":
        # Mid confidence: selected interest greater than or equal to zero
        return df[df[interest] >= 0].sort_values(by=sorting_col, ascending=False)
    
    elif confidence_level == "Low":
        # Low confidence: all users
        return df.sort_values(by=sorting_col, ascending=False)

    else:
        raise ValueError("Invalid confidence level. Choose from 'Very high', 'High', 'Good', 'Mid', 'Low'.")
    

def sort_users_by_cosine_similarity(df:pd.DataFrame, interest_profile: pd.Series) -> pd.DataFrame:
    
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