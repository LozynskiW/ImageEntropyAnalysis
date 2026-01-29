from abc import abstractmethod, ABC

from data_unification.enums import KeyValues, MapKeysEnum, PersistentNames, TransientValues


class DataRow(ABC):
    _data_row: dict

    @abstractmethod
    def get_value(self, key: MapKeysEnum):
        raise NotImplementedError


class DataMap(ABC):
    """
    This is a structure that is meant to keep data from db (list[dict] type) in a way
    that guarantees ease of access to data, consistency and immutability of this data.
    Also allows to

    In other words this exists so that when You try to plot 'distance' in function of 'entropy' You can be sure that
    first values from list of distances and list of entropies are both values from one single json document from db
    (this is why data is dict).

    Furthermore, this class allows to index the data via some float parameters @see data_unification.enums.KeyValues
    to enable faster data retrieval by state.
    """
    _data_map_indexes: dict[KeyValues, dict[float, list[DataRow]]]

    # @abstractmethod
    # def get_values_by_key_and_value(self, key_index: KeyValues, value) -> list:
    #     raise NotImplementedError

    # @abstractmethod
    # def get_all_values_for_key(self, key_index: KeyValues) -> list:
    #     raise NotImplementedError

    def get_data_map_indexes(self) -> dict[KeyValues, dict[float, list[DataRow]]]:
        """
        Method used to access data_map index and implement custom logic. Should always return a copy of index.
        """
        return self._data_map_indexes

    @abstractmethod
    def get_values(self, key: MapKeysEnum) -> list:
        """
        Method should return all values for given key. For example data as it is saved to db looks like this:
        [
            {
                "expected_value": 3.24,
                "variance": 10.03
            },
            {
                "expected_value": 4.24,
                "variance": 17.41
            },
        ]
        And so the key is "expected_value" or "variance" and so if given key is "expected_value" it should return:
        [3.24, 4.24]
        Parameters
        ----------
        key - instance of MapKeysEnum that represents key for key-value pair
        """
        raise NotImplementedError

    @abstractmethod
    def get_values_by(self, key: MapKeysEnum, min_val: float, max_val: float) -> list:
        """
        Used to get some values that passes condition - are min_val <= value < max_val
        Parameters
        ----------
        key - values You want to get
        min_val - minimal value used to filter, inclusive
        max_val - maximal value used to filter, exclusive
        """
        raise NotImplementedError

    @abstractmethod
    def get_values_for_where(self, values_key: MapKeysEnum, values_where_key: MapKeysEnum, min_val: float, max_val: float) -> list:
        """
        Used to get some value by using other value as a condition for getting the value out. For example
        You want distance, but only when pitch angle is between 10 and 20 degrees
        Parameters
        ----------
        values_key - values You want to get
        values_where_key - values that will be used to select values from values_key - used for filtering.
        min_val - minimal value used to filter values for values_where_key, inclusive
        max_val - maximal value used to filter values for values_where_key, exclusive
        """
        raise NotImplementedError

    @abstractmethod
    def _get_values_by_key_and_value(self, key_index: KeyValues, value) -> list:
        raise NotImplementedError
