import ast
import operator as op
import math

# supported operators
_operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

# allowed names from math
_allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith('_')}

# add built-in constants like 'pi', 'e'
_allowed_names.update({'pi': math.pi, 'e': math.e})


def eval_expr(expr: str):
    """Safely evaluate a mathematical expression using AST."""
    node = ast.parse(expr, mode='eval').body
    return _eval(node)


def _eval(node):
    if isinstance(node, ast.Num):  # <number>
        return node.n
    elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
        op_type = type(node.op)
        if op_type in _operators:
            return _operators[op_type](_eval(node.left), _eval(node.right))
    elif isinstance(node, ast.UnaryOp):  # <operator> <operand>
        op_type = type(node.op)
        if op_type in _operators:
            return _operators[op_type](_eval(node.operand))
    elif isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in _allowed_names:
            args = [_eval(arg) for arg in node.args]
            return _allowed_names[node.func.id](*args)
    elif isinstance(node, ast.Name):
        if node.id in _allowed_names:
            return _allowed_names[node.id]
    raise ValueError('Invalid expression')
