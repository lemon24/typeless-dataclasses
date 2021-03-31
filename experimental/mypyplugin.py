from mypy.nodes import AssignmentStmt
from mypy.nodes import CallExpr
from mypy.nodes import NameExpr
from mypy.nodes import PlaceholderNode
from mypy.nodes import RefExpr
from mypy.nodes import Var
from mypy.plugin import Plugin
from mypy.types import AnyType
from mypy.types import TypeOfAny


def typeless_context(ctx):
    if ctx.reason.fullname != 'typeless_dataclasses.typeless':
        return

    cls = ctx.cls

    changed = 0

    for stmt in ctx.cls.defs.body:
        # BEGIN from the dataclasses plugin

        if not isinstance(stmt, AssignmentStmt):
            continue

        lhs = stmt.lvalues[0]
        if not isinstance(lhs, NameExpr):
            continue

        # ###
        print('---', lhs.name, stmt.unanalyzed_type, type(stmt.unanalyzed_type))

        if stmt.unanalyzed_type is not None:
            continue

        stmt.type = AnyType(TypeOfAny.explicit)
        stmt.unanalyzed_type = AnyType(TypeOfAny.explicit)
        changed += 1

        sym = cls.info.names.get(lhs.name)
        if sym is None:
            continue

        node = sym.node
        if isinstance(node, PlaceholderNode):
            return None
        assert isinstance(node, Var)

        # if lhs.name == 'two':
        # import IPython; IPython.embed()

        print(node.name, 'got any')

        expr = stmt.rvalue
        if not (
            isinstance(expr, CallExpr)
            and isinstance(expr.callee, RefExpr)
            and expr.callee.fullname == 'dataclasses.field'
        ):
            node.is_classvar = True
            print(' ', 'also classvar')

        from mypy.server.trigger import make_wildcard_trigger

        ctx.api.add_plugin_dependency(make_wildcard_trigger(sym.fullname))
        ctx.api.add_plugin_dependency(make_wildcard_trigger(cls.fullname))
        ctx.api.add_plugin_dependency(make_wildcard_trigger(ctx.reason.fullname))
        ctx.api.add_plugin_dependency(make_wildcard_trigger(cls.info.mro[1].fullname))
        ctx.api.add_plugin_dependency(sym.fullname)
        ctx.api.add_plugin_dependency(cls.fullname)
        ctx.api.add_plugin_dependency(ctx.reason.fullname)
        ctx.api.add_plugin_dependency(cls.info.mro[1].fullname)

        """
        mypytest.py:14: error: Too many arguments for "Data"
        mypytest.py:16: note: Revealed type is 'def (self: builtins.object)'
        mypytest.py:17: note: Revealed type is 'Any'
        mypytest.py:18: note: Revealed type is 'Any'
        mypytest.py:19: note: Revealed type is 'Any'

        attribs look fine, but the signature doesn't; we neeed to run this *before* the dataclasses plugin somehow

        """

    if changed:
        ctx.api.defer()


class CustomPlugin(Plugin):
    def get_class_decorator_hook(self, fullname: str):
        if 'typeless' in fullname:
            return typeless_context


def plugin(version: str):
    return CustomPlugin
