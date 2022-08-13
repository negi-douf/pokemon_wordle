import pytest
from pokemon_wordle import Color, ColorLabels


class TestColorLabels:

    @pytest.mark.parametrize('response,expected', [
        ('フシギダネ', [Color.GREEN, Color.GREEN, Color.GREEN, Color.GREEN, Color.GREEN]),
        ('フ・ギ・ネ', [Color.GREEN, Color.WHITE, Color.GREEN, Color.WHITE, Color.GREEN]),
        ('ネフシギダ', [Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.YELLOW]),
        ('ネフシギギ', [Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.WHITE]),
        ('フフフネギ', [Color.GREEN, Color.WHITE, Color.WHITE, Color.YELLOW, Color.YELLOW]),
    ])
    def test_colorlabel_when_same_char_not_in_pokemon_name(self, response: str, expected: list[Color]):
        color_labels = ColorLabels(answer='フシギダネ', response=response)
        actual = color_labels.labels
        assert actual == expected

    @pytest.mark.parametrize('response,expected', [
        ('ゴーリキー', [Color.GREEN, Color.GREEN, Color.GREEN, Color.GREEN, Color.GREEN]),
        ('ゴ・リ・ー', [Color.GREEN, Color.WHITE, Color.GREEN, Color.WHITE, Color.GREEN]),
        ('ーゴーリキ', [Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.YELLOW]),
        ('ーゴーリリ', [Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.WHITE]),
        ('ゴゴゴゴゴ', [Color.GREEN, Color.WHITE, Color.WHITE, Color.WHITE, Color.WHITE]),
        ('ゴーゴーリ', [Color.GREEN, Color.GREEN, Color.WHITE, Color.YELLOW, Color.YELLOW]),
    ])
    def test_label_when_same_char_in_pokemon_name(self, response: str, expected: list[Color]):
        color_labels = ColorLabels(answer='ゴーリキー', response=response)
        actual = color_labels.labels
        assert actual == expected
