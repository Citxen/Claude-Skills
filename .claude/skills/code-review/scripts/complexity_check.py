import sys, ast

def check_file(path):
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=path)
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            lines = node.end_lineno - node.lineno + 1
            if lines > 30:
                issues.append(f"{node.name}: {lines} lines (consider splitting)")
    return issues

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
