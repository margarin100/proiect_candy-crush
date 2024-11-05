import random

# Joc: parametri de baza
ROWS, COLS = 11, 11
GOAL_SCORE = 10000
NUM_GAMES = 100

# Punctaj pentru formatiuni
POINTS = {
    'line_3': 5,
    'line_4': 10,
    'line_5': 50,
    'L': 20,
    'T': 30
}


# Initializare matrice cu valori random intre 1 si 4
def init_matrix():
    return [[random.randint(1, 4) for _ in range(COLS)] for _ in range(ROWS)]


# Afisare matrice
def display_matrix(matrix):
    for row in matrix:
        print(' '.join(str(cell) for cell in row))
    print("\n")


# Detectare formatiuni de bomboane
def detect_formations(matrix):
    formations = []
    for i in range(ROWS):
        for j in range(COLS):
            # Linie de 3, 4, 5 elemente
            if j <= COLS - 3 and matrix[i][j] == matrix[i][j + 1] == matrix[i][j + 2]:
                formations.append(('line_3', [(i, j + k) for k in range(3)]))
            if j <= COLS - 4 and matrix[i][j] == matrix[i][j + 1] == matrix[i][j + 2] == matrix[i][j + 3]:
                formations.append(('line_4', [(i, j + k) for k in range(4)]))
            if j <= COLS - 5 and matrix[i][j] == matrix[i][j + 1] == matrix[i][j + 2] == matrix[i][j + 3] == matrix[i][
                j + 4]:
                formations.append(('line_5', [(i, j + k) for k in range(5)]))

            # Coloana de 3, 4, 5 elemente
            if i <= ROWS - 3 and matrix[i][j] == matrix[i + 1][j] == matrix[i + 2][j]:
                formations.append(('line_3', [(i + k, j) for k in range(3)]))
            if i <= ROWS - 4 and matrix[i][j] == matrix[i + 1][j] == matrix[i + 2][j] == matrix[i + 3][j]:
                formations.append(('line_4', [(i + k, j) for k in range(4)]))
            if i <= ROWS - 5 and matrix[i][j] == matrix[i + 1][j] == matrix[i + 2][j] == matrix[i + 3][j] == \
                    matrix[i + 4][j]:
                formations.append(('line_5', [(i + k, j) for k in range(5)]))

            # Formatiune "L"
            if i <= ROWS - 3 and j <= COLS - 3:
                if matrix[i][j] == matrix[i + 1][j] == matrix[i + 2][j] == matrix[i + 2][j + 1] == matrix[i + 2][j + 2]:
                    formations.append(('L', [(i, j), (i + 1, j), (i + 2, j), (i + 2, j + 1), (i + 2, j + 2)]))
                if matrix[i][j] == matrix[i][j + 1] == matrix[i][j + 2] == matrix[i + 1][j] == matrix[i + 2][j]:
                    formations.append(('L', [(i, j), (i, j + 1), (i, j + 2), (i + 1, j), (i + 2, j)]))

            # Formatiune "T"
            if i <= ROWS - 3 and j <= COLS - 3:
                if matrix[i][j + 1] == matrix[i + 1][j] == matrix[i + 1][j + 1] == matrix[i + 1][j + 2] == \
                        matrix[i + 2][j + 1]:
                    formations.append(('T', [(i, j + 1), (i + 1, j), (i + 1, j + 1), (i + 1, j + 2), (i + 2, j + 1)]))

    return formations


# Eliminare bomboane din formatiuni
def remove_candies(matrix, formation):
    for _, positions in formation:
        for (i, j) in positions:
            matrix[i][j] = 0


# Coborarea bomboanelor
def drop_candies(matrix):
    for j in range(COLS):
        column = [matrix[i][j] for i in range(ROWS) if matrix[i][j] != 0]
        column = [0] * (ROWS - len(column)) + column
        for i in range(ROWS):
            matrix[i][j] = column[i]


# Interschimbare bomboane
def swap(matrix, pos1, pos2):
    i1, j1 = pos1
    i2, j2 = pos2
    matrix[i1][j1], matrix[i2][j2] = matrix[i2][j2], matrix[i1][j1]


# Rulare joc principal
def play_game():
    matrix = init_matrix()
    score = 0
    swaps = 0

    # Afisare matrice initiala
    print("Matricea initiala:")
    display_matrix(matrix)

    while True:
        formations = detect_formations(matrix)
        if not formations:
            # Cauta interschimbari posibile intre bomboane adiacente
            found = False
            for i in range(ROWS):
                for j in range(COLS):
                    if j < COLS - 1:  # Interschimbare orizontala
                        swap(matrix, (i, j), (i, j + 1))
                        if detect_formations(matrix):  # Verifica formatiuni
                            swaps += 1
                            found = True
                        swap(matrix, (i, j), (i, j + 1))  # Revert

                    if i < ROWS - 1:  # Interschimbare verticala
                        swap(matrix, (i, j), (i + 1, j))
                        if detect_formations(matrix):  # Verifica formatiuni
                            swaps += 1
                            found = True
                        swap(matrix, (i, j), (i + 1, j))  # Revert

                    if found:
                        break
                if found:
                    break

            if not found:
                break  # Opreste daca nu mai sunt interschimbari valide

        # Calcul punctaj si eliminare bomboane
        for form_type, positions in formations:
            score += POINTS[form_type]
        remove_candies(matrix, formations)

        # Opreste daca scorul a atins pragul
        if score >= GOAL_SCORE:
            break

        drop_candies(matrix)

    return score, swaps


# Simuleaza mai multe jocuri si calculeaza scoruri medii
def simulate_games():
    total_score = 0
    total_swaps = 0
    scores = []
    for i in range(1, NUM_GAMES + 1):
        print(f"\n--- Jocul {i} ---")
        game_score, game_swaps = play_game()
        scores.append(game_score)
        total_score += game_score
        total_swaps += game_swaps
        print(f"Scor total Jocul {i}: {game_score} puncte")
        print(f"Interschimbari Jocul {i}: {game_swaps}\n")

    average_score = total_score / NUM_GAMES
    average_swaps = total_swaps / NUM_GAMES
    return scores, average_score, average_swaps


# Rulare simulare si afisare scoruri
scores, average_score, average_swaps = simulate_games()
print("\nScor mediu dupa 100 jocuri:", average_score)

