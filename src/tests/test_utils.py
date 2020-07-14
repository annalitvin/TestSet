from django.test import SimpleTestCase
from tests import utils


class TestFrange(SimpleTestCase):

    def test_add(self):

        assert utils.add(2, 2) == 4
        assert utils.add(0, 2) == 2
        assert utils.add(1, 2) == 3
        assert utils.add(-1, 2) == 1
        assert utils.add(2, 0) == 2
        assert utils.add(2, 1) == 3
        assert utils.add(2, -1) == 1
