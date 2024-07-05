from pydantic import BaseModel, Field
from typing import List, Union, Optional

class InterestProfile(BaseModel):
    interests: List[str]
    weights: List[float]

class UserData(BaseModel):
    gender: Optional[Union[str, List[str]]] = Field(default=None, description="Can be 'all', 'Male', 'Female', include 'other', or not.")
    occupation: Optional[Union[str, List[str]]] = Field(default=None, description="Can be any specific occupation or list of them.")
    occupation_category: Optional[Union[str, List[str]]] = Field(default=None, description="Can be a category mapping for occupations.")
    city: Optional[Union[str, List[str]]] = Field(default=None, description="Can be a specific city, list of cities or 'all'.")
    region: Optional[Union[str, List[str]]] = Field(default=None, description="Can be a group mapping for regions.")
    income: Optional[List[int]] = Field(default=None, description="Can be 'quantile based' or 'all'.")
    income_group: Optional[Union[str, List[int]]] = Field(default=None, description="Can be a group mapping for income levels.")
    age: Optional[List[int]] = Field(default=None, description="Can be a range or a category label for ages.")
    age_group: Optional[Union[str, List[str]]] = Field(default=None, description="Can be a group mapping for age categories.")
    interest: Optional[InterestProfile] = Field(default=None, description="Needs an interest profile for multiple interests.")
    n_users: Optional[int] = Field(default=None, description="Number of recommended target users.")
    confidence_level: Optional[str] = Field(default=None, description="Number of recommended target users.")

class UserRequest(BaseModel):
    user_data: UserData
