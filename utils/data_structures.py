from copy import deepcopy

import tabulate

class Grid:
    def __init__(self, width, height, default=''):
        self.width = width
        self.height = height
        self.data = [[default for y in range(width)] for x in range(height)]

    def set(self, x, y, value):
        self.data[y][x] = value

    def get(self, x, y):
        return self.data[y][x]

    def __str__(self):
        return self.render()

    def out_of_bound(self, x, y):
        if x < 0 or y < 0:
            return True
        if x >= self.width or y >= self.height:
            return True
        return False

    def count(self, item):
        result = 0
        for y in range(self.height):
            result += self.data[y].count(item)
        return result

    def render(self, fmt="rounded_grid", headers=True):
        data = deepcopy(self.data)
        if headers:
            for y in range(self.height):
                data[y].insert(0, str(y).rjust(2, "0"))

            header = [str(x).rjust(2, "0") for x in range(self.width)]
            header.insert(0, "")
            data.insert(0, header)

        if fmt == "ultra_compact":
            tablefmt = "minpadding"
            tabulate._table_formats[tablefmt] = tabulate.TableFormat(
                lineabove=tabulate.Line("", "", "", ""),
                linebelowheader=tabulate.Line("", "", "", ""),
                linebetweenrows=None,
                linebelow=tabulate.Line("", "", "", ""),
                headerrow=tabulate.DataRow("", "", ""),
                datarow=tabulate.DataRow("", "", ""),
                padding=0,
                with_header_hide=["lineabove", "linebelow"],
            )
            tabulate.multiline_formats[tablefmt] = tablefmt
            tabulate.tabulate_formats = list(sorted(tabulate._table_formats.keys()))

            return tabulate.tabulate(data, tablefmt=tablefmt)

        return tabulate.tabulate(data, tablefmt=fmt)
