from app.utils.data_loader import load_and_preprocess

## Singleton
class DataManager:
    _data = None

    @classmethod
    def get_data(cls):
        if cls._data is None:
            cls._data = load_and_preprocess()
        return cls._data

# Dependency function
def get_data():
    return DataManager.get_data()
