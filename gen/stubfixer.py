import argparse
import re

def main():
    parser = argparse.ArgumentParser(description="Apply various patches to stubgen'd pyi files")
    parser.add_argument('input', type=str)
    parser.add_argument('-o', dest='output', type=str, help="If not specified, output to stdout.  Otherwise, write to this file.  Output can be the same as input.")
    args = parser.parse_args()

    out_lines = []
    with open(args.input, "rt", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.rstrip()
            # See https://github.com/wjakob/nanobind/issues/1155 - generated stubs for nb::ndarray are too strict about dtype
            if re.search(r"def (\w+)\(", line):
                line = re.sub(r'Annotated\[NDArray\[(?:numpy|np)\.float(?:32|64)\]', 'Annotated[NDArray[Any]', line)
                ndarray_1d = "Annotated[NDArray[Any], dict(shape=(None,), order='C', device='cpu', writable=False)]"
                line = line.replace("line_colors: object | None = None", f"line_colors: {ndarray_1d} | None = None")
                line = line.replace("fill_colors: object | None = None", f"fill_colors: {ndarray_1d} | None = None")
                line = line.replace("marker_sizes: object | None = None", f"marker_sizes: {ndarray_1d} | None = None")
                line = line.replace("marker_line_colors: object | None = None", f"marker_line_colors: {ndarray_1d} | None = None")
                line = line.replace("marker_fill_colors: object | None = None", f"marker_fill_colors: {ndarray_1d} | None = None")
                line = line.replace("def line_colors(self) -> object:", f"def line_colors(self) -> {ndarray_1d} | None:")
                line = line.replace("def fill_colors(self) -> object:", f"def fill_colors(self) -> {ndarray_1d} | None:")
                line = line.replace("def marker_sizes(self) -> object:", f"def marker_sizes(self) -> {ndarray_1d} | None:")
                line = line.replace("def marker_line_colors(self) -> object:", f"def marker_line_colors(self) -> {ndarray_1d} | None:")
                line = line.replace("def marker_fill_colors(self) -> object:", f"def marker_fill_colors(self) -> {ndarray_1d} | None:")
                line = line.replace("def line_colors(self, arg: object, /) -> None: ...", f"def line_colors(self, arg: {ndarray_1d} | None, /) -> None: ...")
                line = line.replace("def fill_colors(self, arg: object, /) -> None: ...", f"def fill_colors(self, arg: {ndarray_1d} | None, /) -> None: ...")
                line = line.replace("def marker_sizes(self, arg: object, /) -> None: ...", f"def marker_sizes(self, arg: {ndarray_1d} | None, /) -> None: ...")
                line = line.replace("def marker_line_colors(self, arg: object, /) -> None: ...", f"def marker_line_colors(self, arg: {ndarray_1d} | None, /) -> None: ...")
                line = line.replace("def marker_fill_colors(self, arg: object, /) -> None: ...", f"def marker_fill_colors(self, arg: {ndarray_1d} | None, /) -> None: ...")
            elif re.search(r"^from typing import", line) and 'Any' not in  line:
                line = line + ', Any'
            out_lines.append(line)

    if args.output is not None:
        with open(args.output, "wt", encoding="utf-8") as f:
            f.write('\n'.join(out_lines))
            f.write('\n')
    else:
        print('\n'.join(out_lines))

if __name__ == '__main__':
    main()
