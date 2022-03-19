import pytest

from translation import Lang, detect_language


@pytest.mark.parametrize(
    "content,expected",
    [
        pytest.param("Ostrava je statutární, krajské a univerzitní město.", Lang.CS),
        pytest.param(
            "О́страва, Остра́ва — статутный город на востоке Чешской", Lang.RU
        ),
        pytest.param("ОО́страва — місто на північному сході Чехії, третє за", Lang.UK),
        pytest.param("Ostrava — місто на північному сході Чехії, третє за", Lang.UK),
    ],
)
def test_detect_language(content: str, expected: Lang) -> None:
    assert detect_language(content) == expected
