import sys, ast

FUNCTION_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef)

def nested_functions(node):
    # Yield the closest function definitions inside node, without descending into them
    for child in ast.iter_child_nodes(node):
        if isinstance(child, FUNCTION_TYPES):
            yield child
        else:
            yield from nested_functions(child)

def span(node):
    start = min([d.lineno for d in node.decorator_list] + [node.lineno])
    return node.end_lineno - start + 1

def check_file(path):
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=path)
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, FUNCTION_TYPES):
            # Count only the function's own lines, not those of functions defined inside it
            lines = node.end_lineno - node.lineno + 1
            lines -= sum(span(child) for child in nested_functions(node))
            if lines > 30:
                issues.append((node.lineno, f"{node.lineno}: {node.name}: {lines} lines (consider splitting)"))
    return [message for _, message in sorted(issues)]

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: complexity_check.py <file.py>", file=sys.stderr)
        sys.exit(2)
    try:
        issues = check_file(sys.argv[1])
    except (OSError, UnicodeDecodeError, SyntaxError) as e:
        print(f"error: cannot check {sys.argv[1]}: {e}", file=sys.stderr)
        sys.exit(1)
    for issue in issues:
        print(issue)
