import typer
from typing_extensions import Annotated


def ccwc(
    file_path: str,
    show_bytes: Annotated[
        bool,
        typer.Option(
            "--bytes",
            "-c",
            help="Count how many bytes the file or stream of file contains",
        ),
    ] = False,
    show_lines: Annotated[
        bool, typer.Option("--lines", "-l", help="Count how many lines the text in the file contains")
    ] = False,
):
    bytes_count = 0
    lines_count = 0
    with open(file_path, "rb") as f:
        for line in f:
            if show_bytes:
                bytes_count += len(line)
            if show_lines:
                lines_count += 1

    if show_bytes:
        print(f"{bytes_count} {file_path}")
        return bytes_count
    if show_lines:
        print(f"{lines_count} {file_path}")
        return lines_count
    return bytes_count
