import re
import numpy as np
import argparse


def read_file(filename):
    """Читаем файл и удаляем элементы отличные от кода
    """
    with open(filename, 'r', encoding='utf-8') as f:
        a = f.read()
        b = "".join(a)
        c = re.sub('#.*', '', b)  # Убираем однострочные комментарии

        z = re.sub(r'"""[\w\W]*?"""', r'', c, flags=re.M)  # Убираем многострочные комментарии
    return z


def list_to_process(filename):
    """Функция для обработки входного файла, получим список файлов для сравнения
    """
    with open(filename, 'r') as f:
        text_lines = f.readlines()
    file_list = [line.split() for line in text_lines]
    return file_list


def levenshtein(code1, code2):
    """Функция расчета расстояния Левенштейна для двух строк с кодом
    """
    size_x = len(code1) + 1
    size_y = len(code2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if code1[x - 1] == code2[y - 1]:
                matrix[x, y] = min(matrix[x - 1, y] + 1, matrix[x - 1, y - 1], matrix[x, y - 1] + 1)
            else:
                matrix[x, y] = min(matrix[x - 1, y] + 1, matrix[x - 1, y - 1] + 1, matrix[x, y - 1] + 1)
    return (matrix[size_x - 1, size_y - 1])


if __name__ == '__main__':
    # Входные параметры
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, nargs='?')
    parser.add_argument('output_file', type=str, nargs='?')
    args = parser.parse_args()
    # Очистим выходной файл
    file_out = open(args.output_file, "w")
    file_out.close()
    # Получаем список файлов
    file_list = list_to_process(args.input_file)
    counter=0
    min1=float("Inf")
    for file1, file2 in file_list:
        print(file1, file2)
        # Читаем файлы
        text_code1 = read_file(file1)
        text_code2 = read_file(file2)

        filtered_1 = text_code1.split('\n')
        try:
            while True:
                filtered_1.remove("")
        except ValueError:
            pass

        filtered_2 = text_code2.split('\n')
        try:
            while True:
                filtered_2.remove("")
        except ValueError:
            pass

        simvols1 = 0  # Количество символов с пробелами
        simvols2 = 0
        text_1 = "".join(filtered_1)
        spaces_1 = text_1.count(" ")  # Количество пробелов

        for k in filtered_1:
            simvols1 += len(k)
        simvols1_itogo = simvols1 - spaces_1
        text_2 = "".join(filtered_2)
        spaces_2 = text_2.count(" ")  # Количество пробелов

        for w in filtered_2:
            simvols2 += len(w)
        simvols2_itogo = simvols1 - spaces_2

        for i in range(len(filtered_1)):
            for j in range(len(filtered_2)):
                a = levenshtein(filtered_1[i], filtered_2[j])
                if a < min1:
                    min1 = a
            counter += min1
            min1 = float("Inf")
        if simvols1_itogo != 0 and simvols2_itogo != 0:
            score = round(1. - counter / simvols1_itogo, 3)
        else:
            score = 0
        print(score)

        # Запишем в файл результаты
        with open(args.output_file, 'a') as f:
            f.write(f"{score:1.2f}")
            f.write("\n")