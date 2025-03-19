
from functools import lru_cache
import json
import re
from typing import Any, Dict, Optional, Set

def camel_to_snake(name):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

@lru_cache
def get_definitions() -> Dict[str, Any]:
    with open('gen/cimgui/definitions.json', 'rt', encoding='utf-8') as f:
        return json.load(f)

@lru_cache
def get_imgui_funcnames() -> Set[str]:
    defs = get_definitions()
    syms = set()
    for name, decl in defs.items():
        if name.startswith('ig'):
            syms |= { decl[0]['funcname'] }
    return syms

#access the Style structure (colors, sizes). Always use PushStyleColor(), PushStyleVar() to modify style mid-frame!

def _is_special_case_string(tokens: list[str]) -> Optional[list[str]]:
    exceptions = [
        ['Window', ' ', 'Menu', ' ', 'Button'],
    ]
    for e in exceptions:
        if ''.join(tokens[:len(e)]) == ''.join(e):
            return e
    return None

def docstring_fixer(docstring):
    '''Replace imgui function names in a docstring with markdown code blocks in Python naming convention that should match slimgui.'''
    tokens = re.findall(r'\w+|[^\w\s]|\s+', docstring)
    imgui_funcnames = get_imgui_funcnames()
    out = []
    tok_idx = 0
    while tok_idx < len(tokens):

        # Skip some predefined strings that look like code that should be fixed.
        if (s := _is_special_case_string(tokens[tok_idx:])) is not None:
            out += s
            tok_idx += len(s)
            continue

        toks = tokens[tok_idx:tok_idx+3]
        ignore_rename = ['Value']
        match toks:
            case [sym, '(', ')']:
                if (sym not in ignore_rename) and (sym in imgui_funcnames):
                    out.append(f'`{camel_to_snake(sym)}()`')
                else:
                    out += toks
                tok_idx += len(toks)
            case rest:
                sym = rest[0]
                if (sym not in ignore_rename) and (sym in imgui_funcnames):
                    out.append(f'`{camel_to_snake(sym)}`')
                else:
                    out.append(sym)
                tok_idx += 1
    return ''.join(out)

#if __name__ == '__main__':
#    print(docstring_fixer('Set the color of the IsItemHovered() and SetTooltip'))
