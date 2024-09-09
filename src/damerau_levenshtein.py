def levenshtein_calculate_distance(s1: str, s2: str) -> float:
    s1 = s1.lower()
    s2 = s2.lower()

    matrix = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]

    for i in range(len(s1) + 1):
        matrix[i][0] = i
    for j in range(len(s2) + 1):
        matrix[0][j] = j

    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            substitution_cost = 0 if s1[i - 1] == s2[j - 1] else 1
            matrix[i][j] = min(matrix[i - 1][j] + 1,
                               matrix[i][j - 1] + 1,
                               matrix[i - 1][j - 1] + substitution_cost)

    max_length = max(len(s1), len(s2))
    normalized = 1 - matrix[-1][-1] / max_length
    return normalized
