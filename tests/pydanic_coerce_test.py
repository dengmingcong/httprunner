from pydantic import BaseModel


class Foo(BaseModel):
    some_list: list


def test_pydantic_coerce_tuple_to_list():
    foo = Foo(some_list=(1, 2))
    assert foo.some_list == [1, 2]
