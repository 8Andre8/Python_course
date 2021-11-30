import pytest
from morse import decode


@pytest.mark.parametrize('s, exp', [
    ('... --- ...', 'SOS'),
    ('.- .- .-', 'AAA'),
    ('', '')
])
def test_morse_decode(s, exp):
    assert decode(s) == exp
