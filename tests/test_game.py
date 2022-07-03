import pytest
from pokemon_wordle import Color, Game, Pokemon


class TestGame:

    @pytest.mark.parametrize('responce,expected', [
        ('フシギダネ', [Color.GREEN, Color.GREEN, Color.GREEN, Color.GREEN, Color.GREEN]),
        ('フ・ギ・ネ', [Color.GREEN, Color.NONE, Color.GREEN, Color.NONE, Color.GREEN]),
        ('ネフシギダ', [Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.YELLOW]),
        ('ネフシギギ', [Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.NONE]),
        ('フフフネギ', [Color.GREEN, Color.NONE, Color.NONE, Color.YELLOW, Color.YELLOW]),
    ])
    def test_label_when_same_char_not_in_pokemon_name(self, responce: str, expected: list[Color]):
        choiced_pokemon = Pokemon(name='フシギダネ', type_01='くさ', type_02='どく')
        game = Game(answer_pokemon=choiced_pokemon)
        actual = game.label(responce)
        assert actual == expected

    @pytest.mark.parametrize('responce,expected', [
        ('ゴーリキー', [Color.GREEN, Color.GREEN, Color.GREEN, Color.GREEN, Color.GREEN]),
        ('ゴ・リ・ー', [Color.GREEN, Color.NONE, Color.GREEN, Color.NONE, Color.GREEN]),
        ('ーゴーリキ', [Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.YELLOW]),
        ('ーゴーリリ', [Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.NONE]),
        ('ゴゴゴゴゴ', [Color.GREEN, Color.NONE, Color.NONE, Color.NONE, Color.NONE]),
        ('ゴーゴーリ', [Color.GREEN, Color.GREEN, Color.NONE, Color.YELLOW, Color.YELLOW]),
    ])
    def test_label_when_same_char_in_pokemon_name(self, responce: str, expected: list[Color]):
        choiced_pokemon = Pokemon(name='ゴーリキー', type_01='かくとう')
        game = Game(answer_pokemon=choiced_pokemon)
        actual = game.label(responce)
        assert actual == expected
