import math
from neural_network.expert_vectors import ExpertVector


def create_weight_matrix(vectors, weight):
    n = len(vectors[0])
    weight_matrix = []  # весовая матрица

    for i in range(n):
        weight_matrix.append([])  # создаем новую строку матрицы
        for j in range(n):  # пробегаем по столбцам
            comp = 0
            for k in range(len(vectors)):  # вычисление элемента матрицы
                comp += vectors[k][j] * vectors[k][i]
            comp *= weight  # умножаем на вес после цикла т.к. вес везде одинаковый
            weight_matrix[i].append(comp)

    return weight_matrix


def out_norm_vector(weight_matrix, vector):
    exp_v = ExpertVector()
    norm_vect = []
    for i in range(len(vector)):  # пропускаем вектор через матрицу фильтра
        comp = 0
        for j in range(len(vector)):
            comp += weight_matrix[i][j] * vector[j]
        norm_vect.append(comp)

    for i, item in enumerate(norm_vect):  # нормируем
        if item >= 0:
            norm_vect[i] = 1
        else:
            norm_vect[i] = -1

    return norm_vect


def minimum_distance(expert_vectors, vector):
    min_dist = math.inf
    for i in range(len(expert_vectors)):
        dist = 0
        a = 'намана'
        if vector == expert_vectors[i]:
            a = 'ебаный стыд'
        for j in range(len(vector)):  # находим расстояния
            dist += (vector[j] - expert_vectors[i][j]) ** 2
        dist = math.sqrt(dist)

        if dist < min_dist:  # сравниваем с минимальным
            min_dist = dist

    return min_dist


def critical_distance(vectors, weight_matrix):  # находим критическое расстояние
    distances = []
    for vector in vectors:
        distances.append(minimum_distance(vectors, out_norm_vector(weight_matrix, vector)))

    distances.sort(reverse=True)
    return distances[-2]


def predict(test_vector, number=0):
    exp_v = ExpertVector()
    vectors = exp_v.get_expert_vecotrs(f'vectors/{number}.bin')

    weight_matrix = create_weight_matrix(vectors, 1 / len(vectors))  # строим матрицу фильтра
    crit_dist = critical_distance(vectors, weight_matrix)  # определяем критическое расстояние
    min_dist = minimum_distance(vectors, out_norm_vector(weight_matrix, test_vector))
    if min_dist <= crit_dist:
        return True
    else:
        return False