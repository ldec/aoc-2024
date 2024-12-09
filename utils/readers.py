from os.path import isfile
from typing import List, Any, Optional

from utils.data_structures import Grid


class Reader:
    """
    Base class for Reader implementation.
    """

    def read(self, *args, **kwargs):
        """
        Base implem of the read function
        """
        raise NotImplementedError


class FileReader(Reader):
    """
    Base class for file Reader implementation

    Support basic file reading
    """

    file = None

    def __init__(self, file: str) -> None:
        assert isfile(file), f"Cannot import file {file}"
        self.file = file

    def read(self, *args, **kwargs) -> str:
        """
        Base implementation of a file read function
        """
        with open(self.file, "r") as f:
            return f.read()


class GridReader(FileReader):
    """
    Implementation of a grid reader
    """
    def read(self, *args, **kwargs) -> List[List[str]]:
        """
        Implementation of a grid reader
        """
        data = super(GridReader, self).read()
        result = []
        for line in data.splitlines():
            result.append(list(line))

        return result

class GridReaderv2(FileReader):
    """
    Implementation of a grid reader, returning a Grid datastructure
    """
    def read(self, *args, **kwargs) -> Grid:
        """
        Implementation of a grid reader
        """
        data = super(GridReaderv2, self).read().splitlines()

        grid = Grid(len(data), len(list(data[0])))

        for y in range(len(data)):
            line = list(data[y])
            for x in range(len(line)):
                grid.set(x,y, line[x], set_item_map=True)

        return grid

class SpaceDelimitedColumnFileReader(FileReader):
    """
    Implementation of an multiple column data file Reader, delimited by space.

    E.g.

    1 4
    2 5
    3 6
    """

    def read(
        self, *args, type_to_cast: Any = None, **kwargs
    ) -> List:
        """
        Implementation of an N column data file read function

        :param type_to_cast: Optional type casting for each line
        :param sort: Sort the list
        """
        data = super(SpaceDelimitedColumnFileReader, self).read()
        split_data = []
        for line in data.splitlines():
            separated_line = []
            columns = line.split(" ")
            for column in columns:
                if column:
                    separated_line.append(column)

            if type_to_cast is not None:
                separated_line = list(map(type_to_cast, separated_line))
            split_data.append(separated_line)

        return split_data


class OneColumnFileReader(FileReader):
    """
    Implementation of a one column data file Reader

    E.g.

    1
    2
    3
    """

    def read(
        self, *args, type_to_cast: Any = None, sort: bool = False, **kwargs
    ) -> List:
        """
        Implementation of a one column data file read function

        :param type_to_cast: Optional type casting for each line
        :param sort: Sort the list
        """
        data = super(OneColumnFileReader, self).read()
        split_data = [line for line in data.splitlines() if line]
        if type_to_cast is not None:
            split_data = list(map(type_to_cast, split_data))
        if sort:
            split_data = sorted(split_data)
        return split_data
