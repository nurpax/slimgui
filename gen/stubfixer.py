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
