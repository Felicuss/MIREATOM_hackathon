import sympy as sp
from sympy.parsing.latex import parse_latex

# База данных формул в LaTeX
database = [
    r"-(a + b)",  # Формула 1
    r"-a - b",     # ормула 2 (эквивалентна Формуле 1)
    r"a * b + c",  # Формула 3
    r"c + a * b",  # Формула 4 (эквивалентна Формуле 3)
    r"x + y",      # Формула 5
    r"y + x",      # Формула 6 (эквивалентна Формуле 5)
    r"x + x * y",  # Формула 7
    r"a + b * b",  # Формула 8
    r"a + b + 1",  # Формула 9 (похожая на x + y)
]

# Функция для парсинга LaTeX в выражение SymPy
def parse_latex_formula(latex_string):
    return parse_latex(latex_string)

# Функция для нормализации выражений
def normalize_expression(expr):
    # Упрощаем выражение до нормализованной формы
    # Убираем все буквы и приводим к виду без переменных для "похожих" формул
    expr = sp.simplify(expr)
    return expr

# Функция для нахождения похожих формул
def compare_formulas(input_latex, database):
    # Разбираем введенную формулу
    input_expr = parse_latex_formula(input_latex)
    normalized_input = normalize_expression(input_expr)

    # Переменная для поиска похожих формул
    similar_formulas = []

    # Проходим по базе данных и ищем похожие формулы
    for formula in database:
        # Разбираем формулы из базы данных
        db_expr = parse_latex_formula(formula)
        normalized_db = normalize_expression(db_expr)

        # Если выражения схожи (нормализованы и упрощены)
        if sp.simplify(normalized_input - normalized_db) == 0:
            similar_formulas.append(formula)  # Добавляем в список похожих

    return similar_formulas

# Пример использования
input_latex = r"x + y + 1"  # Вводим формулу

matching_latex = compare_formulas(input_latex, database)

if matching_latex:
    print(f"Найдены похожие формулы: {', '.join(matching_latex)}")
else:
    print("Похожих формул не найдено")
