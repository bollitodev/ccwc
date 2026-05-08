import typer
import sys
from typing_extensions import Annotated


def ccwc(
        file_path: Annotated[str|None, typer.Argument()] = None,
    bytes_c: Annotated[
        bool,
        typer.Option(
            "--bytes",
            "-c",
            help="Count how many bytes the file or stream of file contains",
        ),
    ] = False,
    lines_c: Annotated[
        bool,
        typer.Option(
            "--lines", "-l", help="Count how many lines the text in the file contains"
        ),
    ] = False,
    word_c: Annotated[
        bool,
        typer.Option("--words", "-w", help="Count how many words contains the file"),
    ] = False,
    chars_c: Annotated[
        bool,
        typer.Option("--chars", "-m", help="Count the amount of characters in the file")
        ] = False
):
    response = ""
    bytes_count = 0
    lines_count = 0
    words_count = 0
    chars_count = 0

    if not any([bytes_c, lines_c, word_c, chars_c]):
        bytes_c = lines_c = word_c = True

    if not file_path:
        for line in sys.stdin:
            if chars_c:
                decoded_str = line.decode("utf-8")
                chars_count += len(decoded_str)
            if word_c:
                decoded_str = line.decode("utf-8")
                words_count += len(decoded_str.split())
            if bytes_c:
                bytes_count += len(line)
            if lines_c:
                lines_count += 1
    else:
        with open(file_path, "rb") as f:
            for line in f:
                if chars_c:
                    decoded_str = line.decode("utf-8")
                    chars_count += len(decoded_str)
                if word_c:
                    decoded_str = line.decode("utf-8")
                    words_count += len(decoded_str.split())
                if bytes_c:
                    bytes_count += len(line)
                if lines_c:
                    lines_count += 1


    if lines_c:
        response = f" {lines_count}"
    if word_c:
        response = f"{response} {words_count}"
    if bytes_c:
        response = f"{response} {bytes_count}"
    if chars_c:
        response = f"{response} {chars_count}"

    print(f"{response} {file_path if file_path else ''}")
