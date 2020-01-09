from textwrap import dedent

from jedi.inference import helpers


def test_call_of_leaf_in_brackets(Script):
    s = dedent("""
    x = 1
    type(x)
    """)
    last_x = Script(s).names(references=True, definitions=False)[-1]
    name = last_x._name.tree_name

    call = helpers.call_of_leaf(name)
    assert call == name
