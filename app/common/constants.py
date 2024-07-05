from enum import Enum

class ConfidenceLevel(Enum):
    VERYHIGH = 'Very High'
    HIGH = 'High'
    GOOD = 'Good'
    MID = 'Mid'
    LOW = 'Low'

class Method(Enum):
    COSINE_SIMILARITY = 'cosine_similarity'
    INTERESTED = 'interested'