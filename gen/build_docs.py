
import argparse
import inspect
import json
import os
import re
import subprocess
import sys
import importlib
import types

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
    line = line.replace('slimgui.slimgui_ext.imgui.', 'imgui.')
    line = line.replace('slimgui.slimgui_ext.implot.', 'implot.')
    line = line.replace('slimgui_ext.imgui.', 'imgui.')
    line = line.replace('slimgui_ext.implot.', 'implot.')
    line = line.replace('slimgui.imgui.', 'imgui.')
    line = line.replace('slimgui.implot.', 'implot.')
    tokens = _tokenize_code(line)

    # Initialize the highlighted output
    output = []
    last_index = 0

    # Loop over the tokens and apply highlighting
    for idx, token in enumerate(tokens):
        token_type, token_value = token
        start_index = line.index(token_value, last_index)
        end_index = start_index + len(token_value)

        # Add any non-highlighted text before the token
        output.append(line[last_index:start_index])

        if token_type == 'ws':
            # don't spanify whitespace
            output.append(' ')
        else:
            if token_type == 'symbol':
                prev_toks = tokens[idx-2:idx]
                next_tok = tokens[idx+1:idx+2]
                if len(prev_toks) >= 2 and prev_toks[0][0] == 'keyword' and prev_toks[0][1] == 'def':
                    output.append(f"<span class='func_name'>{token_value}</span>")
                elif len(next_tok) > 0 and next_tok[0][0] == 'special' and next_tok[0][1] == ':':
                    output.append(f"<span class='arg_name'>{token_value}</span>")
                else:
                    output.append(f"<span class='{token_type}'>{token_value}</span>")
            else:
                output.append(f"<span class='{token_type}'>{token_value}</span>")

        last_index = end_index
    return ''.join(output)

def _expand_code_blocks_to_html(s: str) -> str:
    '''Convert:
    - inline `code` to <code>
    - triple-backtick blocks to <pre>
    - double newlines to <br>
    '''
    
    # Handle fenced code blocks
    def block_repl(match):
        code = match.group(1)
        return f'<pre>{code.strip()}</pre>'
    s = re.sub(r'```(?:\w*\n)?(.*?)```', block_repl, s, flags=re.DOTALL)
    # Handle inline code (single-line only)
    s = re.sub(r'`([^`\n]+)`', lambda m: f'<code>{m.group(1)}</code>', s)
    # Convert double newlines to <br>
    s = re.sub(r'\n{2,}', '<br>', s)
    return s

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
            entry = {
                'def_line_html': f'<div class="api">\n  <code>{_highlight_def_line(source_line)}</code>\n</div>\n',
            }
            if docstring is not None and docstring != '':
                entry['docstring'] = docstring
            outf.write(f'{json.dumps(entry)}\n')
            outf.write('$$end\n')
        elif isinstance(node, ast.ClassDef):
            if not any(ty in source_line for ty in ['(enum.IntEnum)', '(enum.IntFlag)']):
                continue
            outf.write(f'$$class={node.name}\n')
            outf.write('<div class="api-class">\n')
            outf.write(f'  <div><span class="class_name">{node.name}</span> (enum)</div>\n')
            outf.write('  <table>\n')

            expr_for_assign = {}
            prev_assign = None
            for class_node in node.body:
                if isinstance(class_node, ast.Expr):
                    expr_for_assign[prev_assign] = class_node
                    prev_assign = None
                elif isinstance(class_node, ast.Assign):
                    prev_assign = class_node

            for class_node in node.body:
                if isinstance(class_node, ast.Assign):
                    for target in class_node.targets:
                        if any(x in target.id for x in ['__repr__', '__str__']):
                            continue

                        doc_string = ''
                        if (expr := expr_for_assign.get(class_node)) is not None:
                            doc_string = expr.value.value
                            if doc_string is None:
                                doc_string = ''
                            doc_string = _expand_code_blocks_to_html(doc_string.strip())

                        if isinstance(target, ast.Name):
                            outf.write(f'  <tr><td class="field">{target.id}</td><td class="fielddoc">{doc_string}</td></tr>\n')

            outf.write('  </table>\n')
            outf.write('</div>\n')
            outf.write('$$end\n')

def module_to_html_lookup(module, outf):
    m =  importlib.import_module(module)
    for name in dir(m):
        obj = getattr(m, name)

        # Handle only functions and classes defined in Python.  This is because
        # it seems to be easier to get docs and arg names from the pyi file.
        if isinstance(obj, types.FunctionType):
            func = obj
            outf.write(f'$$func={name}\n')
            sig = inspect.signature(func)
            sig = inspect.signature(func)
            func_def = f'def {func.__name__}{sig}'
            entry = {
                'def_line_html': f'<div class="api">\n  <code>{_highlight_def_line(func_def)}</code>\n</div>\n',
            }
            docstring = inspect.getdoc(func)
            if docstring is not None and docstring != '':
                entry['docstring'] = docstring
            outf.write(f'{json.dumps(entry)}\n')
            outf.write('$$end\n')

def main():
    parser = argparse.ArgumentParser(description="Build documentation.")
    parser.add_argument("input_file", type=str, help="The input markdown file.")
    parser.add_argument("--pyi-file", type=str, help=".pyi file to extract type information from.")
    parser.add_argument("--module", type=str, help="module path to import for doc strings (use this or --pyi-file, not both).")
    parser.add_argument("--output", type=str, help="The output HTML file.")
    parser.add_argument("--imgui-version", type=str, help="The version of imgui")
    parser.add_argument("--print-apiref-html", action="store_true", help="Enable HTML for .pyi generated HTML API ref content.")
    args = parser.parse_args()

    print(f"Building docs from {args.input_file}...")

    docs_basedir = os.path.dirname(os.path.abspath(args.input_file))
    if not os.path.isfile(f'{docs_basedir}/template.html'):
        print(f"Error: template.html not found in {docs_basedir}", file=sys.stderr)
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        lua_filter = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docbuild_extras.lua')

        api_html = f'{tmpdir}/api.html'
        with open(api_html, 'wt', encoding='utf-8') as file:
            if args.pyi_file is not None:
                pyi_to_html_lookup(args.pyi_file, file)
            if args.module is not None:
                module_to_html_lookup(args.module, file)

        if args.print_apiref_html:
            print('Generated HTML API ref content:')
            with open(api_html, 'rt', encoding='utf-8') as file:
                print(file.read())
            exit()

        # Add '--toc' if you want table of contents
        subprocess.run(["pandoc",
            args.input_file, "-o", args.output,
            '--template', f'{docs_basedir}/template.html',
            '--standalone', '--wrap=none',
            '-f', 'markdown-smart',
            '--lua-filter', lua_filter,
            '--metadata', f'api_html={api_html}',
            '--metadata', f'imgui_version={args.imgui_version}',
        ], check=True)

if __name__ == "__main__":
    main()