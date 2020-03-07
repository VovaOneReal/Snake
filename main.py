import os
import time
import random
import keyboard

# ИГРОВЫЕ ПЕРЕМЕННЫЕ
# Игра запущена? True - да и входим в цикл, False - нет и пропускам или выходим из цикла.
gameInProgress = True

# TO-DO ЛИСТ
# 1. Змея должна быть корректного размера [CHECK]
# 2. После поедания яблока, змея должна увеличиваться [CHECK]
# 3. Если змея сталкивается с препятствием, то игра заканчивается [CHECK]
#
# ПО ЖЕЛАНИЮ
# 1. Счётчик съеденных яблок
# 2. Таймер
# Если будет добавлен, то можно сделать укорачивание змейки, когда время будет подходить к концу.
# 3. Несколько уровней с разным ландшафтом

# КОДЫ ДЛЯ ОТРИСОВКИ
# 0 - ничего - .
# 1 - голова - O
# 1< - тело - o
# -1 - яблоко - U
# -2 - стена - H


# Функция первого уровня. Она наполняет локацию препятствиями.
def levelOne(plot):
    plot[0][0] = -2
    plot[0][1] = -2
    plot[0][2] = -2
    plot[0][3] = -2
    plot[0][4] = -2
    plot[0][5] = -2
    plot[0][6] = -2
    plot[0][7] = -2
    plot[0][8] = -2

    plot[1][0] = -2
    plot[2][0] = -2
    plot[3][0] = -2
    plot[4][0] = -2
    plot[5][0] = -2
    plot[6][0] = -2
    plot[7][0] = -2
    plot[8][0] = -2

    plot[1][8] = -2
    plot[2][8] = -2
    plot[3][8] = -2
    plot[4][8] = -2
    plot[5][8] = -2
    plot[6][8] = -2
    plot[7][8] = -2
    plot[8][8] = -2

    plot[8][1] = -2
    plot[8][2] = -2
    plot[8][3] = -2
    plot[8][4] = -2
    plot[8][5] = -2
    plot[8][6] = -2
    plot[8][7] = -2

    return plot


# Функция нахождения самого большого числа (т.к. встроенная функция max() не подходит)
def maxValueInPlot(plot, plotX, plotY):
    maxNumber = 0
    j = 0
    while j < plotY:
        k = 0
        while k < plotX:
            # Сравнивая числа в массиве, находим самое большое и записываем в maxNumber
            if plot[j][k] > maxNumber:
                maxNumber = plot[j][k]
            else:
                pass
            k += 1
        j += 1
    return maxNumber


# Функция проверки условий победы/поражения
def gameConditions(plot, nextSnakeHeadX, nextSnakeHeadY, length):
    global gameInProgress
    # Если игрок сталкивается с самим собой или со стеной, то игра окончена
    if plot[nextSnakeHeadY][nextSnakeHeadX] == -2:
        print("Игра окончена")
        gameInProgress = False
    elif plot[nextSnakeHeadY][nextSnakeHeadX] > 0:
        print("Игра окончена")
        gameInProgress = False
    # Если длина игрока достигает 45, то он выигрывает
    elif length == 45:
        print("Вы победили!")
        gameInProgress == False
    # Если игрок съедает яболоко, то его длина увеличивается
    elif plot[nextSnakeHeadY][nextSnakeHeadX] == -1:
        length += 1

    return length


# Функция корректного создания яблок
# В аргументы принимаем содержимое карты, а также её размеры
def appleCreator(plot, plotX, plotY):
    # Для яблока отдельно случайно генерируем координаты по осяи X и Y
    appleX = random.randint(0, plotX - 1)
    appleY = random.randint(0, plotY - 1)
    # Если полученные координаты не конфликтуют с другими объектами, то на это место ставим яблоко
    if plot[appleY][appleX] == 0:
        plot[appleY][appleX] = -1
    # Иначе, вновь пытаемся создать яблоко
    else:
        appleCreator(plot, plotX, plotY)
    return plot


# Функция отслеживания наличия яблок
def apple(plot, plotX, plotY):
    # Добавляем переменную "Имеется ли яблоко на поле?" и изначально предполагаем, что нет.
    ifAppleOnMap = False
    # Если нет, то начинаем просматривать всю карту на наличие яблока
    while not ifAppleOnMap:
        j = 0
        while j < plotY:
            k = 0
            while k < plotX:
                # Если находим яблоко, то "Имеется ли яблоко на поле?" теперь становится истиной.
                if plot[j][k] == -1:
                    ifAppleOnMap = True
                # Иначе мы игнорируем итог и ищем дальше... Мы ничего не меняем при этом.
                else:
                    pass
                    # print("яблоко не обнаружено")
                k += 1
            j += 1
        # Если в итоге мы так и не нашил яблока, то...
        if not ifAppleOnMap:
            # Вызываем функцию генерации яблок и записываем их координаты на карту
            plot = appleCreator(plot, plotX, plotY)
            # Чтобы выйти из цикла в таком случае, меняем значение переменной на "да"
            ifAppleOnMap = True
        # Иначе ничего не делаем
        else:
            pass
            # print("ну наверное тут ошибка")

    return plot


# Функция отслеживания действий змеи
def snake(plot, plotX, plotY, x, y, direction, length):
    # Обработка нажатий клавишь для направления змеи + проверка прошлого движения змеи для недопуска самопересечения.
    # Если нажата клавиша W (Вперёд)
    if keyboard.is_pressed(17):
        # И если при этом змея не двигалась вниз...
        if direction != 3:
            # Меняем направление на "вверх"
            direction = 1
        # Иначе ничего не делаем
        else:
            pass
    # Если нажата клавиша D (Вправо)
    elif keyboard.is_pressed(32):
        # И если до этого змея не двигалась влево...
        if direction != 4:
            direction = 2
        else:
            pass
    # Если нажата клавиша S (Вниз)
    elif keyboard.is_pressed(31):
        # Если до этого змея не двигалась вверх...
        if direction != 1:
            direction = 3
        else:
            pass
    # Если нажата клавиша A (Влево)
    elif keyboard.is_pressed(30):
        # Змея не двигалась вправо...
        if direction != 2:
            direction = 4
        else:
            pass

    # Изменение размера змейки
    snakeElements = 0
    j = 0
    while j < plotY:
        k = 0
        while k < plotX:
            # Смотрим, сколько ячеек заняты змеёй.
            if plot[j][k] >= 1:
                # Добавляем по единице в переменную, если находим такую ячейку
                snakeElements += 1
            else:
                pass
            k += 1
        j += 1
    # После этого смотрим, больше ли ячеек со змеёй, чем её заявленная длина?
    if snakeElements > length:
        # В таком случае ищем самый последний элемент змеи (хвост)
        lastSnakeElement = maxValueInPlot(plot, plotX, plotY)
        # Потом снова начинаем перебирать массив с картой в поиске хвоста
        j = 0
        while j < plotY:
            k = 0
            while k < plotX:
                # И если такой находится, то делаем его пустой клеткой
                if plot[j][k] == lastSnakeElement:
                    plot[j][k] = 0
                else:
                    pass
                k += 1
            j += 1

    # Меняем значения уже существующих элементов змейки, чтобы те из головы (1), стали телом (>1).
    # Перебираем массив с картой в поиске нужных элементов
    j = 0
    while j < plotY:
        k = 0
        while k < plotX:
            # Если в ячейке находится "голова", то добавляем единицу, чтобы та стала телом.
            if plot[j][k] >= 1:
                plot[j][k] += 1
            # Иначе мы игнорируем итог и ищем дальше... Мы ничего не меняем при этом.
            else:
                pass
            k += 1
        j += 1

    # Изменение координат головы
    # Если выбрано направление (из предыдущего алгоритма)...
    # Вверх
    if direction == 1:
        y -= 1
    # Вправо
    elif direction == 2:
        x += 1
    # Влево
    elif direction == 3:
        y += 1
    # Ввниз
    elif direction == 4:
        x -= 1
    elif direction == 0:
        pass

    # Функция проверки победы/поражения - проверяем перед тем, как координата головы изменится
    length = gameConditions(plot, x, y, length)

    # Изменяем координату и "перемещаем" голову змеи
    plot[y][x] = 1

    return plot, x, y, direction, length


# Функция отрисовки. Принимает массив карты для отображения
def draw(plot, plotX, plotY):
    # Как выводить информацию (символы, числа)? True - символы, False - числа
    symbolsOutput = True
    # Если False, то выводим числами
    if not symbolsOutput:
        j = 0
        while j < plotY:
            k = 0
            while k < plotX:
                print(plot[j][k], end="")
                k += 1
            print('')
            j += 1
    # Если True, то выводим символами
    elif symbolsOutput:
        j = 0
        while j < plotY:
            k = 0
            while k < plotX:
                # 0 - ничего - .
                if plot[j][k] == 0:
                    print(".", end="")
                    k += 1
                # -1 - яблоко - U
                elif plot[j][k] == -1:
                    print("U", end="")
                    k += 1
                # -2 - стена - H
                elif plot[j][k] == -2:
                    print("H", end="")
                    k += 1
                # 1 - Голова - O
                elif plot[j][k] == 1:
                    print("O", end="")
                    k += 1
                # >1 - Тело - o
                elif plot[j][k] > 1:
                    print("o", end="")
                    k += 1
                # Если что-то другое, то выводим крест.
                else:
                    print("X", end="")
                    k += 1
            print('')
            j += 1


# Функция с циклом игры.
def game():
    # Задаём размер карты
    plotX = 9
    plotY = 9
    # Создаём массив с пустой картой. В дальнейшем вид такой plot[y][x]
    plot = [[0] * plotX for i in range(plotY)]
    plot = levelOne(plot)
    # ПЕРЕМЕННЫЕ ЗМЕИ
    # Создаём переменные координат головы змеи
    snakeHeadX = 4
    snakeHeadY = 4
    # Добавляем голову змеи
    plot[snakeHeadY][snakeHeadX] = 1
    # Переменная направления движения змеи. Наименование по часовой 0 - стоять на месте, 1 - вперёд... 4 - влево.
    snakeDir = 1
    # Длина змеи
    snakeLength = 2

    # Сам цикл игры
    while gameInProgress:
        # Стираем всё нарисованное
        os.system('cls')
        # Обработка наличия яблок
        plot = apple(plot, plotX, plotY)
        # Обработка действий змеи
        plot, snakeHeadX, snakeHeadY, snakeDir, snakeLength = snake(plot, plotX, plotY, snakeHeadX, snakeHeadY, snakeDir, snakeLength)
        # Рисуем карту
        draw(plot, plotX, plotY)
        # Задержка в выводе
        time.sleep(0.65)


# НАЧАЛО ПРОГРАММЫ
print(".....ooo...........................ooooO....")
print("....o...O...O.oo.....oo.O...O.oO...o........")
print(".....oo.....oo..o...o..oo...oo.....oooO.....")
print("...o...o....o...o...o..oo...o.o....o........")
print("....ooo.....o...O....oo.o...o..o...ooooO....")
print("-----[ By VovaOne | v1.0 | 07.03.2020 ]-----")
os.system('pause')
os.system('cls')

game()
os.system('pause')
