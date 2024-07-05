import os
import sys

# Get the directory of the current directly
current_directory = os.path.dirname(os.path.abspath(__file__))

# Define full paths to your data files using the current directory
DEMOGRAPHIC_DATA_PATH = os.path.join(current_directory, 'utils', 'preprocessing', 'data', 'demographic_data.csv')
INTERACTION_DATA_PATH = os.path.join(current_directory, 'utils', 'preprocessing', 'data', 'interaction_data.csv')
sys.path.append('UserProfiling')

confidence_level_list = ["Very High", "High", "Good", "Mid", "Low"]

n_return_users_default = 50
random_users_percent_default = 20

# Demogrphic df columns
city_column = "city"
age_column = "age"
occupation_column = "occupation"
income_column = "income"
gender_column = "gender"

# Demogrphic df preprocessed columns
region_column = "region"
occupation_category_column = "occupation_category"
age_group_column = "age_group"
age_group_name_column = "age_group_name"
income_quintile_column = "income_quintile"
income_quintile_name_column = "income_quintile_name"


# Define Weights
inital_interest_weight = 5
yes_interaction_weight = 3
no_interaction_weight = -3
neutral_interaction_weight = -1

# Define interests columns
interests_columns = ['Sports', 'Finance', 'Politics', 'Fashion', 'Technology', 'Travel']
interation_columns = ['Fashion_interaction', 'Finance_interaction', 
                                                'Politics_interaction', 'Sports_interaction', 
                                                'Technology_interaction', 'Travel_interaction']

# Define mapping between cities and regions in Italy
region_mapping = {
    'Northern Italy': {'Milan', 'Turin', 'Genoa', 
                       'Bologna', 'Venice', 'Verona', 'Brescia',
                         'Trieste', 'Padua', 'Modena', 'Parma'},
    'Central Italy': {'Rome', 'Florence'},
    'Southern Italy': {'Naples', 'Bari', 'Taranto', 'Reggio Calabria'},
    'Insular Italy': {'Palermo', 'Catania', 'Messina'}
}

# Define occupation mapping between occupations and categories
occupation_mapping = {
    'Doctor': 'Highly Specialized Professions',
    'Lawyer': 'Highly Specialized Professions',
    'Engineer': 'Highly Specialized Professions',
    'Artist': 'Creative and Educational Professions',
    'Teacher': 'Creative and Educational Professions',
    'Unemployed': 'General Employment Status'
}

# Define the age bins and corresponding labels
age_bins = [17, 24, 34, 44, 54, 69]  
age_numeric_labels = ['18-24', '25-34', '35-44', '45-54', '55-69']
age_descriptive_labels = ['Young Adults', 'Adults', 'Middle-aged Adults', 'Mature Adults', 'Older Adults']

# Define the income bins and labels
income_quintile_labels=['1st Quintile', '2nd Quintile', '3rd Quintile', '4th Quintile', '5th Quintile']
number_of_income_quintile = 5
