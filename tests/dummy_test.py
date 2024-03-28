import pytest
from iSparrowRecord import dummy


def test_dummy():
    assert dummy.test(3) == 6
