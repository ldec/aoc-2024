from rich import print as _print


def print(*args, **kwargs):
    """
    Workaround for https://youtrack.jetbrains.com/issue/PY-57706/Indentation-is-incorrect-when-Emulate-terminal-in-output-console-is-used
    """
    return _print(*args, **kwargs, end="\r\n")
