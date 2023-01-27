import unittest
from random import sample
from loto_game import Card, PlayerComputer, HumanPlayer, Game


class TestCard(unittest.TestCase):

    def setUp(self):
        self.card = Card()

    def test_generation_card(self):
        self.assertTrue(isinstance(i, int) for i in self.card.card_num)  # В списке находятся числа
        self.assertEqual(len(self.card.card_num), 15)  # В списке 15 чисел
        self.assertEqual(len(self.card.card_num), len(set(self.card.card_num)))  # Все числа уникальные

    def test_check_num(self):
        num = sample(self.card.card_num, k=1)
        self.assertTrue(self.card.check_num(num[0]))  # Цифра есть в карточке
        self.assertFalse(self.card.check_num(100))  # Цифры нет в карточке

    def test_delete_num_card(self):
        num = sample(self.card.card_num, k=1)
        self.card.delete_num_card(num[0])
        self.assertTrue('X' in self.card.card_num)  # Цифра меняется на X

    def test_chekup_card(self):
        self.assertFalse(self.card.chekup_card)  # Проверка на заполненный список
        self.card.card_num.clear()
        self.assertTrue(self.card.chekup_card)  # Проверка на пустой список

    def test_card_output(self):
        self.assertTrue(isinstance(self.card.card_output, str))  # На выводе строка


class TestPlayerComputer(unittest.TestCase):

    def setUp(self):
        self.computer = PlayerComputer('test')

    def test_init(self):
        self.assertEqual(self.computer.name, 'test')  # Инициализация свойства класса
        self.assertTrue(isinstance(self.computer.card, Card))  # Объект принадлежит к классу Card

    def test_running(self):
        num = sample(self.computer.card.card_num, k=1)
        self.assertTrue(self.computer.running(num[0]))  # Цифра есть в карточке
        self.assertFalse(self.computer.running(100))  # Цифры нет в карточке


class TestHumanPlayer(unittest.TestCase):
    def setUp(self):
        self.human = HumanPlayer('test')

    def test_init(self):
        self.assertTrue(isinstance(self.human.card, Card))  # Объект принадлежит к классу Card
        self.assertTrue(self.human.name == 'test')  # Инициализация свойства класса

    def test_running(self):
        num = sample(self.human.card.card_num, k=1)
        self.assertTrue(self.human.running(num[0], answer='Д'))
        self.assertTrue(self.human.running(100, answer='Н'))
        self.assertTrue(self.human.running(num[0], answer='Н'))
        self.assertFalse(self.human.running(100, answer='Д'))


class TestGame(unittest.TestCase):

    def setUp(self):  # Инстанцируем объект класса перед каждым тестом
        self.game = Game()

    def tearDown(self):  # Очищаем список игроков после тестов
        self.game.players.clear()

    def test_init(self):
        self.assertTrue(isinstance(self.game.players, list))
        self.assertEqual(len(self.game._Game__keg_bag), 90)  # Проверка инкапсулированного атрибута класса

    def test_bag(self):
        self.assertTrue(isinstance(self.game.bag(), int))
        self.assertEqual(self.game._Game__keg_bag.count(self.game.bag()),
                         0)  # Возвращаемое число удаляется из мешка

    def test_game_mode1(self):
        self.game.game_mode('1', 'test')
        self.assertEqual(len(self.game.players), 2)

    def test_game_mode2(self):
        self.game.game_mode('2', None)
        self.assertEqual(len(self.game.players), 2)

    def test_game_mode3(self):
        self.game.game_mode('3', ['test_1', 'test_2', 'test_3', 'test_4'])
        self.assertEqual(len(self.game.players), 4)
