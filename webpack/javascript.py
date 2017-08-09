from slimit import ast


class JSBase:

    def __init__(self, node):
        self.node = node

    def __str__(self):
        if isinstance(self.node, ast.Boolean):
            return str(self.node.value).lower()
        if isinstance(self.node, ast.Number):
            return str(self.node.value)
        return self.node.to_ecma()


class JSValue(JSBase):

    def __init__(self, node):
        if isinstance(node, ast.Node):
            self.node = node
        elif isinstance(node, bool):
            self.node = ast.Boolean(node)
        elif isinstance(node, (int, float)):
            self.node = ast.Number(node)
        else:
            raise AttributeError('Not a real value, babycakes')

    def __eq__(self, other):
        if isinstance(other, ast.Node):
            return self.node.value == other.value
        else:
            return self.node.value == other


class JSString(JSBase):

    def __init__(self, node):
        if isinstance(node, ast.String):
            self.node = node
        elif isinstance(node, str):
            self.node = ast.String("'{}'".format(node))

    def __eq__(self, other):
        if isinstance(other, str):
            return self.node.value[1:-1] == other
        elif isinstance(other, ast.String):
            return self.node.value[1:-1] == other.value[1:-1]
        return False


class JSArray(JSBase):

    def __init__(self, node):
        if isinstance(node, ast.Array):
            self.node = node
        elif isinstance(node, list):
            self.node = ast.Array([
                PY_MAPPING[v.__class__](v).node for v in node
            ])
        else:
            raise AttributeError('node must be an Array')

    def __getitem__(self, key):
        pass

    def __setitem__(self, key, value):
        pass


class JSObject(JSBase):

    def __init__(self, node):

        if isinstance(node, ast.Object):
            self.node = node
        elif isinstance(node, dict):
            self.node = ast.Object(properties=[
                ast.Assign(
                    op=':',
                    left=PY_MAPPING[k.__class__](k).node, 
                    right=PY_MAPPING[v.__class__](v).node
                ) for (k, v) in node.items()
            ])
        else:
            raise AttributeError('node must be an Object')

    def __getitem__(self, key):
        for child in self.node.children():
            if wrapped_ast(child.left) == key:
                cls = AST_MAPPING[child.right.__class__]
                return cls(child.right)
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        for child in self.node.children():
            if wrapped_ast(child.left) == key:
                break
        else:
            child = ast.Assign(
                op=':',
                left=PY_MAPPING[key.__class__](key).node, 
                right=None
            )
            self.node.properties.append(child)

        child.right = PY_MAPPING[value.__class__](value).node

    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    def keys(self):
        for child in self.node.children():
            if isinstance(child.left, ast.String):
                yield child.left.value[1:-1]
            else:
                yield child.left.value


AST_MAPPING = {
    ast.Object: JSObject,
    ast.Array: JSArray,
    ast.Number: JSValue,
    ast.String: JSString,
    ast.Boolean: JSValue
}

PY_MAPPING = {
    bool: JSValue,
    float: JSValue,
    int: JSValue,
    str: JSString,
    dict: JSObject,
    list: JSArray
}
JS_MAPPING = dict((v, k) for k, v in PY_MAPPING.items())


def wrapped_ast(node):
    return AST_MAPPING.get(node.__class__, JSValue)(node)
