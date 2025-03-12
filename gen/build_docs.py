
import argparse
import os
import re
import subprocess
import sys

import ast
import tempfile

def _tokenize_code(line):
    # Define patterns for different elements
    keyword_pat = r'(def|class|return|if|else|elif|for|while|import|from|as|with|try|except|finally|True|False|None)'
    string_pat = r'(\'.*?\'|".*?")'
    special = r'[\[\],:]'
    ws_pat = r'\s'
    symbol_pat = r'\w+'

    # Combine patterns into a single pattern with named groups
    combined = f'(?P<keyword>{keyword_pat})|(?P<string>{string_pat})|(?P<symbol>{symbol_pat})|(?P<special>{special})|(?P<ws>{ws_pat})'

    # Find all matches and create a list of tokens
    tokens = []
    for match in re.finditer(combined, line):
        token_type = match.lastgroup  # Get the type of the token (keyword, string, comment)
        assert token_type is not None
        token_value = match.group(token_type)  # Get the value of the token
        tokens.append((token_type, token_value))

    return tokens

def _highlight_def_line(line: str) -> str:
    tokens = _tokenize_code(line)

    # Initialize the highlighted output
    highlighted_output = []
    last_index = 0

    # Loop over the tokens and apply highlighting
    for idx, token in enumerate(tokens):
        token_type, token_value = token
        start_index = line.index(token_value, last_index)
        end_index = start_index + len(token_value)

        # Add any non-highlighted text before the token
        highlighted_output.append(line[last_index:start_index])

        if token_type == 'ws':
            # don't spanify whitespace
            highlighted_output.append(' ')
        else:
            if token_type == 'symbol':
                prev_toks = tokens[idx-2:idx]
                next_tok = tokens[idx+1:idx+2]
                if len(prev_toks) >= 2 and prev_toks[0][0] == 'keyword' and prev_toks[0][1] == 'def':
                    highlighted_output.append(f"<span class='func_name'>{token_value}</span>")
                elif len(next_tok) > 0 and next_tok[0][0] == 'special' and next_tok[0][1] == ':':
                    highlighted_output.append(f"<span class='arg_name'>{token_value}</span>")
                else:
                    highlighted_output.append(f"<span class='{token_type}'>{token_value}</span>")
            else:
                highlighted_output.append(f"<span class='{token_type}'>{token_value}</span>")

        # Update the last index
        last_index = end_index

    return ''.join(highlighted_output)

# Parse a .pyi file to extract top-level symbols, their args and return
# values.  Documentation renderer will use this information to generate
# API ref information.
def pyi_to_html_lookup(file_path, outf):
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Parse the content of the .pyi file into an AST
    tree = ast.parse(file_content)

    # Now you can traverse the AST to extract type information
    for node in tree.body:
        source_line = file_content.splitlines()[node.lineno - 1]
        if isinstance(node, ast.FunctionDef):

            docstring = ast.get_docstring(node)

            outf.write(f'$$func={node.name}\n')
            source_line = source_line.rstrip(": ...")

            outf.write('<div class="apifunc">\n')
            outf.write(f'  <code>{_highlight_def_line(source_line)}</code>\n')
            if docstring:
                outf.write(f'  <p>{docstring}</p>\n')
            outf.write('</div>\n')

            outf.write('$$end\n')
        elif isinstance(node, ast.ClassDef):
            #print(f"Class: {node.name}")
            pass


def main():
    parser = argparse.ArgumentParser(description="Build documentation.")
    parser.add_argument("input_file", type=str, help="The input markdown file.")
    parser.add_argument("--pyi-file", type=str, help=".pyi file to extract type information from.")
    parser.add_argument("--output", type=str, help="The output HTML file.")
    parser.add_argument("--print-pyi-html", action="store_true", help="Enable HTML for .pyi generated HTML API ref content.")
    args = parser.parse_args()

    print(f"Building docs from {args.input_file}...")

    docs_basedir = os.path.dirname(os.path.abspath(args.input_file))
    if not os.path.isfile(f'{docs_basedir}/template.html'):
        print(f"Error: template.html not found in {docs_basedir}", file=sys.stderr)
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        lua_filter = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docbuild_extras.lua')

        api_html = f'{tmpdir}/api_mockup.html'
        with open(api_html, 'wt', encoding='utf-8') as file:
            pyi_to_html_lookup(args.pyi_file, file)
            if args.print_pyi_html:
                print('Generated HTML API ref content:')
                with open(api_html, 'rt', encoding='utf-8') as file:
                    print(file.read())
                exit()

        subprocess.run(["pandoc",
            args.input_file, "-o", args.output,
            '--template', f'{docs_basedir}/template.html',
            '--standalone', '--toc', '--wrap=none',
            '--lua-filter', lua_filter,
            '--metadata', f'api_html={api_html}',
        ], check=True)

if __name__ == "__main__":
    main()