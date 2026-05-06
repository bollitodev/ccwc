import typer
from typing_extensions import Annotated

def ccwc(file_path:str, show_bytes: Annotated[bool, typer.Option("--bytest", "-c",help="Count how many bytes the file or stream of file contains")]= False):
    bytes_count = 0
    with open(file_path, "r") as f:
        content = f.read()

        if show_bytes:
            bytes_count = len(content.encode('utf-8'))

    if show_bytes:
        print(f"{bytes_count} {file_path}")
        return bytes_count 
    return (bytes_count)


