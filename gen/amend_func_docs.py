# Note: this script runs in CI and should run on the lowest Python version
# that the library is being built for.

# This script reads the comments from the ImGui header file and adds them to the
# corresponding functions in the pyi file.
import argparse
import re
from typing import Dict, Union

import gen_utils

def parse_func_line_comments(header_path: str) -> Dict[str, Union[str, None]]:
    with open(header_path, "rt", encoding="utf-8") as f:
        lines = f.readlines()

    func_line_comments: Dict[str, Union[str, None]] = {}
    for line in lines:
        line = line.rstrip()
        # IMGUI_API void          SetItemDefaultFocus();      // make last item the default focused item of a window.
        if (m := re.match(r"^\s*IMGUI_API.* (\w+)\(.*;(.*)", line)) is not None:
            comment = None
            func_name = gen_utils.camel_to_snake(m.group(1))
            trail = m.group(2)
            if (pos := trail.find('//')) != -1:
                comment = trail[pos+2:].lstrip(' \t')
            func_line_comments[func_name] = comment
    return func_line_comments


def main():
    parser = argparse.ArgumentParser(description="Extract doc comments from imgui.h")
    parser.add_argument('--imgui-h', type=str, default='src/c/imgui/imgui.h')
    parser.add_argument('--pyi-file', type=str, default='src/slimgui/slimgui_ext.pyi')
    parser.add_argument('-o', dest='output', type=str, help="If not specified, output to stdout.  Otherwise, write to this file.  Output can be the same as input.")
    args = parser.parse_args()

    syms = parse_func_line_comments(args.imgui_h)

    out_lines = []
    with open(args.pyi_file, "rt", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.rstrip()

            if (m := re.match(r"^def (\w+)\(", line)) is not None:
                line = re.sub(r': ...$', ':', line)

                out_lines.append(line)
                func_name = m.group(1)
                if (comment := syms.get(func_name)) is not None:
                    comment = comment.strip()
                    if comment == '"':
                        comment = '' # remove spurious double quotes
                    comment = comment.replace('"', '\\"')
                    if comment != '':
                        out_lines.append(f'    """{comment}"""')
                out_lines.append('    ...\n')
            else:
                out_lines.append(line)

    if args.output is not None:
        with open(args.output, "wt", encoding="utf-8") as f:
            f.write('\n'.join(out_lines))
    else:
        print('\n'.join(out_lines))

if __name__ == "__main__":
    main()
