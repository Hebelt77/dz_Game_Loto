import pytest
from random import sample
from loto_game import Card, PlayerComputer, HumanPlayer, Game


class TestCard:
    def setup(self):
        self.card = Card()

    def test_generation_card(self):
        assert (isinstance(i, int) for i in self.card.card_num)  # В списке находятся числа
        assert len(self.card.card_num) == 15  # В списке 15 чисел
        assert len(self.card.card_num) == len(set(self.card.card_num))  # Все числа уникальные

    def test_check_num(self):
        num = sample(self.card.card_num, k=1)
        assert (self.card.check_num(num[0]))  # Цифра есть в карточке
        assert not (self.card.check_num(100))  # Цифры нет в карточке

    def test_delete_num_card(self):
        num = sample(self.card.card_num, k=1)
        self.card.delete_num_card(num[0])
        assert 'X' in self.card.card_num  # Цифра меняется на X

    def test_chekup_card(self):
        assert not self.card.chekup_card              # Проверка на заполненный список
        self.card.card_num.clear()
        assert self.card.chekup_card        # Проверка на пустой список

    def test_card_output(self):
        assert isinstance(self.card.card_output, str)  # На выводе строка


class TestPlayerComputer:

    def setup(self):
        self.computer = PlayerComputer('test')

    def test_init(self):
        assert self.computer.name == 'test'  # Инициализация свойства класса
        assert isinstance(self.computer.card, Card)  # Объект принадлежит к классу Card

    def test_running(self):
        num = sample(self.computer.card.card_num, k=1)
        assert self.computer.running(num[0])
        assert not self.computer.running(100)


class TestHumanPlayer:
    def setup(self):
        self.human = HumanPlayer('test')

    def test_init(self):
        assert isinstance(self.human.card, Card)  # Объект принадлежит к классу Card
        assert self.human.name == 'test'          # Инициализация свойства класса

    def test_running(self):
        num = sample(self.human.card.card_num, k=1)
        assert self.human.running(num[0], answer='Д')
        assert self.human.running(100, answer='Н')
        assert self.human.running(num[0], answer='Н')
        assert not self.human.running(100, answer='Д')


class TestGame:

    def setup(self):        # Инстанцируем объект класса перед каждым тестом
        self.game = Game()

    def teardown(self):     # Очищаем список игроков после тестов
        self.game.players.clear()

    def test_init(self):
        assert isinstance(self.game.players, list)
        assert len(self.game._Game__keg_bag) == 90  # Проверка инкапсулированного атрибута класса

    def test_bag(self):
        assert isinstance(self.game.bag(), int)
        assert self.game._Game__keg_bag.count(self.game.bag()) == 0     # Возвращаемое число удаляется из мешка

    def test_game_mode1(self):
        self.game.game_mode('1', 'test')
        assert len(self.game.players) == 2

    def test_game_mode2(self):
        self.game.game_mode('2', None)
        assert len(self.game.players) == 2

    def test_game_mode3(self):
        self.game.game_mode('3', ['test_1', 'test_2', 'test_3', 'test_4'])
        assert len(self.game.players) == 4

