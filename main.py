import pygame
import random

pygame.init()
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
f1 = pygame.font.Font(None, 36)

positions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
# РАЗМЕР 1 КЛЕКТИ В ПИКСЕЛЯХ
cell_size = 10
# ЗАДАЕМ РАЗМЕР ОКНА В ПИКСЕЛЯХ
root = pygame.display.set_mode((1500, 1000))

# НАЧАЛЬНАЯ ГЕНЕРАЦИЯ КЛЕТОК, ЕСЛИ numb_0 = 10; numb_1 = 1,
# ТО НАЧАЛЬНОЕ ОТНОШЕНИЕ ВСЕХ МЕРТВЫХ К ЖИВЫМ КЛЕТКАМ БУДЕТ = 10/1
numb_0 = 5
numb_1 = 1
chance_array = []
for i in range(numb_0):
    chance_array.append(0)
for i in range(numb_1):
    chance_array.append(1)
# СОЗДАЕМ МАССИВ ДЛЯ КЛЕТОК, КОТОРЫЙ БУДЕТ ОТРИСОВЫВАТЬСЯ
field_life = []
for i in range(0, root.get_height() // cell_size + 2):
    field_life.append([])
    for j in range(0, root.get_width() // cell_size + 2):
        field_life[i].append(random.choice(chance_array))

# СОЗДАЕМ ВТОРОСТЕПЕННЫЙ МАССИВ ДЛЯ ОБНОВЛЕНИЯ КЛЕТОК
intermediate_field_life = []
for i in range(0, root.get_height() // cell_size + 2):
    intermediate_field_life.append([])
    for j in range(0, root.get_width() // cell_size + 2):
        #field_life[i].append(random.choice(0))
        intermediate_field_life[i].append(0)

# ФУНКЦИЯ ДЛЯ РЕШЕНИЯ РОЖДЕНИЯ/СМЕРТИ КЛЕТКИ
def life_or_death(x, y):
    counter_life_around = 0
    for pos in positions:
        if field_life[y + pos[0]][x + pos[1]] == 1:
            counter_life_around += 1
    if field_life[y][x] == 1:
        if counter_life_around not in [2, 3]:
            intermediate_field_life[y][x] = 0
        else:
            intermediate_field_life[y][x] = 1
    elif field_life[y][x] == 0:
        if counter_life_around in [3]:
            intermediate_field_life[y][x] = 1
        else:
            intermediate_field_life[y][x] = 0

# ОСНОВНОЙ ЦИКЛ ПРОГРАММЫ
while True:
    root.fill(white)
    # ОТРИСОВЫВАЕМ РАЗЛИНОВКУ
    # ПО ГОРИЗОНТАЛИ
    for i in range(0, root.get_height() // cell_size):
        pygame.draw.line(root, black, (0, i * cell_size), (root.get_width(), i * cell_size))
    # ПО ВЕРИТКАЛИ
    for j in range(0, root.get_width() // cell_size):
        pygame.draw.line(root, black, (j * cell_size, 0), (j * cell_size, root.get_height()))
    # ОТРИСОВКА КЛЕТОК (ЧЕРНАЯ-ЖИВАЯ/ БЕЛАЯ- МЕРВТАЯ)
    for y in range(1, len(field_life) - 1):
        for x in range(1, len(field_life[y]) - 1):
            if field_life[y][x] == 1:
                pygame.draw.rect(root, black, [(x - 1) * cell_size, (y - 1) * cell_size, cell_size, cell_size])
    # ПОДСЧИТЫВАЕМ КОЛИЧЕСТВО ЖИВЫХ КЛЕТОК ДЛЯ ВЫВОДА
    sum_life = 0
    for y in field_life:
        sum_life += sum(y)
    # ОТРИСОВКА КОЛИЧЕСТВА
    sum_life_text = f1.render(str(sum_life), True, red)
    root.blit(sum_life_text, (10, 10))

    # ОБНОВЛЯЕМ ЖИЗНИ КЛЕТОК
    for y in range(1, len(field_life) - 1):
        for x in range(1, len(field_life[y]) - 1):
            life_or_death(x, y)
    # ПРИСВАИВАЕМ ОСНОВНОМУ МАССИВУ НОВЫЕ ЗНАЧЕНИЯ (НЕ ПОНИМАЮ ПОЧЕМУ COPY() РАБОТАЕТ НЕКОРРЕКТНО)
    for y in range(len(field_life)):
        for x in range(len(field_life[y])):
            field_life[y][x] = intermediate_field_life[y][x]
    # ОБНУЛЯЕМ;) ВТОРОСТЕПЕННЫЙ МАССИВ
    for i in range(len(intermediate_field_life)):
        for j in range(len(intermediate_field_life[i])):
            intermediate_field_life[i][j] = 0

    # ЧЕКИНГ ЗАКРЫТИЯ ОКНА
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.update()