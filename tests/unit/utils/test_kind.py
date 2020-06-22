from apraw.utils import prepend_kind



class TestSnake:

    def test_prepend_kind(self):
        kind = "kind"
        id = "bigcomplicatedid"

        assert prepend_kind(id, kind) == kind + "_" + id
