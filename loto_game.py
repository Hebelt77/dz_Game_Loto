import time
from random import sample, shuffle


class Card:

    def __init__(self):
        self.card_num = None    # Список с цифрами карты
        self.generation_card()  # Вызов метода для генерации случайных цифр в карточке
        # self.card_out = self.card_output()  # Свойство для вывода в консоль

    def generation_card(self):
        self.card_num = sample((list(i for i in range(1, 91))), 15)

    def check_num(self, num):  # Проверка на наличие номера в карте
        return not self.card_num.count(num) == 0  # Метод count возвращает сколько раз элемент встречается в списке

    def delete_num_card(self, num):  # Замена числа в карточке на "X"
        index = self.card_num.index(num)
        self.card_num[index] = 'X'

    @property                                   # Декоратор property объявляет метод как свойство
    def chekup_card(self):                      # Проверка на наличие в карточке цифр
        card = set(str(self.card_num))
        card -= {'[', ']', ',', ' ', 'X', "'"}
        return True if not card else False      # Если цифр не осталось True, иначе False

    @property                                   # Декоратор property объявляет метод как свойство
    def card_output(self):
        card = list(map(lambda x: str(x), self.card_num))
        spc = list('    ')
        card_1 = card[:5]; card_1.extend(spc); shuffle(card_1)  # Формируем три среза по 5 цифр,
        card_2 = card[5:10]; card_2.extend(spc);  shuffle(card_2)  # добавляем пробелы и перемешиваем списки
        card_3 = card[10:15];    card_3.extend(spc);   shuffle(card_3)

        output = (f'{32 * "-"}\n'                   # Формируем карточку для вывода в консоль
                  f'|{"  ".join(card_1)}|\n'
                  f'|{"  ".join(card_2)}|\n'
                  f'|{"  ".join(card_3)}|\n'
                  f'{32 * "-"}')
        return output


class PlayerComputer:

    def __init__(self, name):
        self.card = Card()
        self.name = name
        # print(f'Имя игрока {self.name}')

    def running(self, num):
        time.sleep(1)       # Метод sleep делает паузу перед ходом компьютера в 1 секунду
        if self.card.check_num(num):
            self.card.delete_num_card(num)
            print(f"Номер {num} есть в карточке игрока: {self.name}")
            print(self.card.card_output)
            return True
        else:
            print(f'Номера {num} нет в карточке игрока: {self.name}')
            print(self.card.card_output)
            return True


class HumanPlayer:

    def __init__(self, name):
        self.card = Card()
        self.name = name

    def running(self, num):
        print(f'    Карточка игрока {self.name}\n'
              f'{self.card.card_output}')
        answer = input("Зачеркнуть цифру? 'Д/Н': ").upper()
        print()
        while answer not in 'ДН':
            answer = input(f"Вы ввели неверный символ!!\n"
                           f"Введите Д или Н!: ").upper()
        if answer == 'Д' and self.card.check_num(num):
            self.card.delete_num_card(num)
            return True
        elif answer == 'Н' and not self.card.check_num(num):
            return True
        else:
            return False


class Game:
    keg_bag = list(range(1, 91))    # Создаём список бочонков

    def __init__(self):
        self.players = list()                # Инициализируем объект класса для списка экземпляров классов игроков

    def menu(self):
        print(f'Добро пожаловать в игру лото:)\n'
              f'\n'
              f'Для начала выберите пункт меню\n'
              f'1.) Один игрок с компьютером.\n'
              f'2.) Компьютер с компьютером.\n'
              f'3.) Несколько игроков (Два и более)')
        point = input('>>: ')
        while point not in '123':
            point = input(f'Не верный ввод!!!\n'
                          f'Введите номер пункта меню >>: ')
        if point == '1':
            name_player = input(
                "Введите имя игрока >>: ")  # Добавляем список игроков в свойство класса для инстанцирования
            self.players.extend([HumanPlayer(name_player), PlayerComputer('Computer ALFA')])  # и передаём в параметры имя игрока

        if point == '2':
            self.players.extend([PlayerComputer('Computer ALFA'), PlayerComputer('Computer OMEGA')])

        if point == '3':
            numbers = input("Введите количество игроков >>: ")
            while not isinstance(numbers, int) or numbers < 2:
                try:
                    numbers = int(numbers)
                    1/0 if numbers < 2 else print()            # Вызываем ошибку если
                except:                                        # количесто игроков меньше 2
                    numbers = input("Введите числовое значение больше 2!!! >>: ")

            names_players = list()
            for i in range(numbers):                                            # Формируем список с именами игроков
                names_players.append(input(f"Введите имя {i + 1} игрока >>: "))

            for name in names_players:                  # Добавляем в свойство класса список игроков для инстанцирования
                self.players.extend([HumanPlayer(name)])  # и передаём в параметры имя игрока

    def bag(self):                                  # Метод достаёт из мешка номер бочонка
        num = sample(self.keg_bag, k=1)
        self.keg_bag.remove(num[0])                     # Удаляет его
        print(f'Выпал бочонок с номером-> {num[0]}')
        return num[0]                                   # И возвращает

    def game_process(self):                                     # Процесс игры
        Game.menu(self)
        for index, player in enumerate(self.players, start=1):
            print(f'Имя {index} игрока: {player.name}')  # Выводим имена игроков из каждого экземпляра класса в списке

        end = False
        while not end:                  # Крутим цикл пока end ложно
            print(f'{("| |" * 20)}')
            num = Game.bag(self)        # Получаем номер бочонка из мешка:)

            for player in self.players:
                print(f'Ход игрока {player.name}')
                print(len(self.players))

                if player.running(num):                 # Проверяем ответ игрока
                    if player.card.chekup_card or len(self.players) == 1:      # Если в карточке игрока закончились цифры
                        print(f'Игрок {player.name} Победил!!!')              # либо игрок остался один
                        end = True                                            # заканчиваем игру
                        break

                else:
                    print(f'Игрок {player.name} Проиграл!!! :(')
                    self.players.remove(player)                     # Удаляем проигравшего игрока из списка игроков
                    if len(self.players) == 0:              # Если в списке не осталось игроков
                        print("Все игроки проиграли :ь")
                        end = True
                        break


if __name__ == '__main__':
    game = Game()           # Старт игры
    game.game_process()

    # game.menu()

    # h = HumanPlayer('f')
    # while True:
    #     num = int(input(': '))
    #     h.running(num)

    # lst = list('12345')
    # space = list('        ')
    # print(space)
    # lst.extend(space)
    # shuffle(lst)
    # print(' '.join(lst))

    # card = Card()
    # print(card.card_num)
    # while True:
    #     num = int(input(': '))
    #     card.delete_num_card(num)
    #     print(card.card_num)
    #     print(card.chekup_card)

    # m = (set(str(card.card_num)))
    # m = [1, 2]
    # print(game.chekup_card(m))

    # m -= {'[', ',', ']', ' '}
    # if not m:
    #     print(m)


