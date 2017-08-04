from django.conf import settings

from django.test import TestCase
from slimit.parser import Parser
from slimit import ast

from slimit.visitors.nodevisitor import ASTVisitor

from django.contrib.staticfiles.finders import find


class ConfigMunger(ASTVisitor):

    def visit(self, tree):
        if not isinstance(tree, ast.Program):
            return

        for node in tree.children():
            if self.is_module_export(node):
                self.munge_exports(node.expr.right)

    def is_module_export(self, node):
        if not isinstance(node, ast.ExprStatement):
            return False

        if not(node.expr.op) == '=':
            return False

        if not isinstance(node.expr.left, ast.DotAccessor):
            return False

        if node.expr.left.identifier.value != 'exports':
            return False

        if not isinstance(node.expr.left.node, ast.Identifier):
            return False

        if node.expr.left.node.value != 'module':
            return False

        return True

    def munge_exports(self, node):

        for child in node:

            if isinstance(child, ast.Assign) and child.op == ':' and child.left.value == 'entry':
                self.munge_entry(child.right)

            if isinstance(child, ast.Assign) and child.op == ':' and child.left.value == 'output':
                self.munge_output(child.right)

    def munge_entry(self, node):

        if isinstance(node, ast.Object):
            # This is a dict....
            for child in node:
                self.munge_entry(child.right)

        elif isinstance(node, ast.String):
            path = node.value[1:-1]
            match = find(path)

            if match:
                node.value = "'{}'".format(match)

    def munge_output(self, node):
        
        if not isinstance(node, ast.Object):
            return

        if getattr(settings, 'STATIC_ROOT'):
            for child in node:
                if isinstance(child.right, ast.String) and child.op == ':' and child.left.value == 'path':
                    # Set the path...
                    child.right.value = "'{}'".format(settings.STATIC_ROOT)
                    break
            else:
                path_node = ast.Assign(
                    op=':',
                    left=ast.Identifier('path'),
                    right=ast.String("'{}'".format(settings.STATIC_ROOT))
                )
                node.properties.append(path_node)

        if getattr(settings, 'STATIC_URL'):
            for child in node:
                if isinstance(child.right, ast.String) and child.op == ':' and child.left.value == 'publicPath':
                    # Set the path...
                    child.right.value = "'{}'".format(settings.STATIC_URL)
                    break
            else:
                public_path_node = ast.Assign(
                    op=':',
                    left=ast.Identifier('publicPath'),
                    right=ast.String("'{}'".format(settings.STATIC_URL))
                )
                node.properties.append(public_path_node)


def get_munged_config(config):
    parser = Parser()
    program = parser.parse(config)

    visitor = ConfigMunger()
    visitor.visit(program)

    return program.to_ecma()