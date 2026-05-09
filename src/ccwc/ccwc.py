import typer
import sys
from typing_extensions import Annotated
from abc import ABC, abstractmethod


class BaseWc(ABC):
    print_counter_order = ("lines", "words", "bytes", "chars")
    default_counters = ("lines", "words", "bytes")

    results = {}

    def __init__(self, counters: dict[str, int]) -> None:
        if not any(counters.values()):
            for key in self.default_counters:
                counters[key] = True
        self.counters = counters

    @abstractmethod
    def read(self):
        pass

    def apply_counters(self, stream):
        for line in stream:
            if self.counters["bytes"]:
                self.results["bytes"] = self.results.get("bytes", 0) + len(line)
            if self.counters["lines"]:
                self.results["lines"] = self.results.get("lines", 0) + 1
            if any([self.counters["words"], self.counters["chars"]]):
                decoded_str = line.decode("utf-8")
                if self.counters["words"]:
                    self.results["words"] = self.results.get("words", 0) + len(
                        decoded_str.split()
                    )
                if self.counters["chars"]:
                    self.results["chars"] = self.results.get("chars", 0) + len(
                        decoded_str
                    )

    def show_results(self) -> str:
        res = ""
        for c in self.print_counter_order:
            if c in self.results:
                value = self.results[c]
                res = f"{res}{value} "
        return res

    @abstractmethod
    def print_results(self):
        pass


class FileWc(BaseWc):
    def __init__(self, file_path: str, counters: dict[str, int]) -> None:
        super().__init__(counters)
        self.file_path = file_path

    def read(self):
        with open(self.file_path, "rb") as f:
            self.apply_counters(f)

    def print_results(self):
        print(f"{self.show_results()} {self.file_path}")


class SystemInputWc(BaseWc):
    def __init__(self, counters: dict[str, int]) -> None:
        super().__init__(counters)

    def read(self):
        self.apply_counters(sys.stdin)

    def print_results(self):
        print(self.show_results())


def ccwc(
    file_path: Annotated[str | None, typer.Argument()] = None,
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
    words_c: Annotated[
        bool,
        typer.Option("--words", "-w", help="Count how many words contains the file"),
    ] = False,
    chars_c: Annotated[
        bool,
        typer.Option(
            "--chars", "-m", help="Count the amount of characters in the file"
        ),
    ] = False,
):
    counters = {"lines": lines_c, "words": words_c, "bytes": bytes_c, "chars": chars_c}
    if not file_path:
        wc_obj = SystemInputWc(counters)
    else:
        wc_obj = FileWc(file_path, counters)

    wc_obj.read()
    wc_obj.print_results()
