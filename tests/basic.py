class CustomType:
    pass


def test_func_without_arg_typed(a, b):
    ...


def test_func_with_one_arg_typed(a: int):
    ...


def test_func_with_many_arg_typed(a: int, b: str, c: CustomType):
    ...
