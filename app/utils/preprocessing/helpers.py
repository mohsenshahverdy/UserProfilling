from app import config
import pandas as pd



def process_user_data(demographic_df:pd.DataFrame, interaction_df:pd.DataFrame) -> pd.DataFrame:
    """
    Processes demographic and interaction data to update user interest scores based on
    predefined interests and responses from interaction data.

    Parameters:
    - demographic_df (pd.DataFrame): DataFrame containing user demographics and their primary interests.
    - interaction_df (pd.DataFrame): DataFrame containing user interactions with different survey types and responses.

    Returns:
    - pd.DataFrame: Updated demographic DataFrame with adjusted interest scores.
    """
    # Copy dataframes to avoid modifying original data
    demographic_data = demographic_df.copy()
    interaction_data = interaction_df.copy()

    # Interests columns
    interests = config.interests_columns

    # Initialize interest columns in demographic data with zero
    for interest in interests:
        demographic_data[interest] = 0

    # Process the interaction data
    # Create a pivot table to count responses per user per survey type
    interaction_pivot = interaction_data.pivot_table(
        index='user_id', 
        columns=['survey_type', 'response'], 
        aggfunc='size', 
        fill_value=0
    )

    # Flatten the pivot table column names
    interaction_pivot.columns = ['_'.join(col).strip() for col in interaction_pivot.columns.values]
    interaction_pivot.reset_index(inplace=True)

    # Merge the interaction pivot table with demographic data
    demographic_data = demographic_data.merge(interaction_pivot, on='user_id', how='left')

    # Adjust scores based on survey responses
    for interest in interests:
        demographic_data[f'{interest}_Yes'] = demographic_data.get(f'{interest}_Yes', 0) * config.yes_interaction_weight
        demographic_data[f'{interest}_No'] = demographic_data.get(f'{interest}_No', 0) * config.no_interaction_weight
        demographic_data[f'{interest}_Neutral'] = demographic_data.get(f'{interest}_Neutral', 0) * config.neutral_interaction_weight

        # Sum up the points for each interest and update the interest score
        demographic_data[interest] += (demographic_data[f'{interest}_Yes'] +
                                       demographic_data[f'{interest}_No'] +
                                       demographic_data[f'{interest}_Neutral'])

    # Drop the individual response columns if they are no longer needed
    response_columns = [f'{interest}_{response}' for interest in interests for response in ['Yes', 'No', 'Neutral']]
    demographic_data.drop(columns=response_columns, inplace=True)

    merged_df = add_interaction_counts(demographic_data, interaction_data)

    # Set initial interest scores based on user's listed interests
    merged_df = merged_df.fillna(0)

    for index, row in merged_df.iterrows():
        user_interest = row['interests']
        if user_interest in interests:
            merged_df.at[index, user_interest] += config.inital_interest_weight

    merged_df['Total'] = merged_df[config.interation_columns].sum(axis=1)

    return merged_df

def add_interaction_counts(demographic_df, interaction_df):
    """
    Processes interaction data to compute interaction counts per user per survey type,
    merges these counts into demographic data, and ensures all interaction columns
    are filled with integers.

    Parameters:
    - demographic_df (pd.DataFrame): DataFrame containing user demographics.
    - interaction_df (pd.DataFrame): DataFrame containing user interactions with survey types.

    Returns:
    - pd.DataFrame: The updated demographic DataFrame with added interaction counts.
    """
    # Group interaction data by 'user_id' and 'survey_type' and count occurrences
    interaction_counts = interaction_df.groupby(['user_id', 'survey_type']).size().unstack(fill_value=0)

    # Reset index to turn the index into a column, making 'user_id' a regular column
    interaction_counts.reset_index(inplace=True)

    # Rename columns to indicate they represent interaction counts
    interaction_counts.columns = [f"{col}_interaction" if col != 'user_id' else col for col in interaction_counts.columns]

    # Merge the calculated interaction counts with the demographic data
    merged_data = demographic_df.merge(interaction_counts, on='user_id', how='left')

    # Fill missing interaction values with zero and convert them to integers
    for col in merged_data.columns:
        if 'interaction' in col:  # Apply only to interaction columns
            merged_data[col] = merged_data[col].fillna(0).astype(int)

    return merged_data


def categorize_age(df: pd.DataFrame, age_column: str) -> pd.DataFrame:
    """
    Categorizes the age in a DataFrame into specified bins and adds these as new columns.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the age data.
    - age_column (str): The name of the column in the DataFrame that contains age data.

    Adds:
    - 'age_group': Categorical labels for age ranges.
    - 'age_group_name': Descriptive names for age categories.
    """
    
    # Create age categories
    df[config.age_group_column] = pd.cut(df[age_column], bins=config.age_bins, labels=config.age_numeric_labels, right=True)
    df[config.age_group_name_column] = pd.cut(df[age_column], bins=config.age_bins, labels=config.age_descriptive_labels, right=True)

    return df


# Function to determine region
def get_region(city: str) -> str:
    for region, cities in config.region_mapping.items():
        if city in cities:
            return region
    return 'Unknown'  # For the city is not found in the mapping

# Funtion for mapping cities to regions
def city_mapping(df: pd.DataFrame) -> pd.DataFrame:
    df[config.region_column] = df[config.city_column].apply(get_region)
    return df

# Funtion for mapping occupation 
def occupation_mapping(df: pd.DataFrame) -> pd.DataFrame:
    df[config.occupation_category_column] = df[config.occupation_column].map(config.occupation_mapping)
    return df


def categorize_income_quintiles(df: pd.DataFrame) -> pd.DataFrame:
    """
    Categorizes the income data in a DataFrame into quintiles and adds the categorization as a new column.

    Parameters:
    - df (pd.DataFrame): DataFrame containing the income data.

    Returns:
    - pd.DataFrame: The DataFrame with an additional column for income quintiles.
    """

    quintile_labels = config.income_quintile_labels
    df[config.income_quintile_name_column] = pd.qcut(df[config.income_column],
                                                      q=config.number_of_income_quintile, labels=quintile_labels)
    return df