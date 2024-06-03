import json
from pathlib import Path
from functools import reduce


# n, mean, M2 = 0, 0.0, 0
#
# for path in Path('imdb-user-reviews').glob('**/*'):
#     if path.is_file() and path.suffix == '.json':
#         with open(path, 'r') as f:
#             info = json.load(f)
#         score = float(info['movieIMDbRating'])
#         n += 1
#         delta = score - mean
#         mean += delta / n
#         M2 += delta * (score - mean)
#
# print(mean, (M2 / n) ** (1 / 2))


def mapper(file_path: Path) -> tuple[int, float, float]:
    if file_path.is_file() and file_path.suffix == '.json':
        with open(file_path, 'r') as f:
            film_info = json.load(f)
            film_score = float(film_info['movieIMDbRating'])
        return 1, film_score, film_score ** 2  # n is always 1 for an individual score, sum of scores, sum of squares
    return 0, 0.0, 0.0


def reducer(acc: tuple[int, float, float], val: tuple[int, float, float]) -> tuple[int, float, float]:
    n1, mean1, m2_1 = acc
    n2, film_score, score_squared = val
    if n2 == 0:
        # No new data, return the old accumulator
        return acc
    new_n = n1 + n2
    new_mean = mean1 + (film_score - mean1) / new_n
    new_m2 = m2_1 + (film_score - mean1) * (film_score - new_mean)
    return new_n, new_mean, new_m2


n, mean, M2 = reduce(reducer, map(mapper, Path('imdb-user-reviews').glob('**/*')))
print(mean, (M2 / n) ** (1 / 2))
# 8.03 1.0517128885774862
