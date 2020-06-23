import uuid

from apraw.utils import prepend_kind

class TestSnake:

    def test_prepend_kind(self):
        kind = "kind"
        uuid1 = str(uuid.uuid1())

        prepended_id = kind + "_" + uuid1

        assert prepend_kind(uuid1, kind) == prepended_id
        assert prepend_kind(prepended_id, kind) == prepended_id
