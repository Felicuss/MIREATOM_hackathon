from fuzzywuzzy import fuzz
from sympy.parsing.latex import parse_latex
from sympy import simplify, latex
from itertools import islice
from string import ascii_letters
import logging
logger = logging.getLogger(__name__)


def latex_to_sympy(latex_formula):
    try:
        return parse_latex(latex_formula)
    except Exception as e:
        raise ValueError(f"Ошибка преобразования LaTeX в SymPy: {e}")


def normalize_formula(latex_formula):
    if not latex_formula or not latex_formula.strip():
        raise ValueError("Формула пуста или некорректна.")

    try:
        sympy_expr = latex_to_sympy(latex_formula)
    except Exception as e:
        raise ValueError(f"Ошибка обработки формулы: {e}")

    normalized_expr = simplify(sympy_expr)

    return normalized_expr
def rename_variables(formula: str) -> str:
    letters: str = ascii_letters
    dict_f: dict[int, str | int] = {}
    for i in range(len(formula)):
        if (formula[i] in letters) and \
           (i == 0 or formula[i - 1] not in letters) and \
           (i == len(formula) - 1 or formula[i + 1] not in letters):
            dict_f[i] = formula[i]

    cnt = 0
    for i, key1 in enumerate(dict_f.keys()):
        if str(dict_f[key1]) in letters:
            for key2 in islice(dict_f.keys(), i + 1, None):
                if dict_f[key2] == dict_f[key1] and key2 != key1:
                    dict_f[key2] = cnt
            dict_f[key1] = cnt
            cnt += 1

    formula_list = list(formula)
    for key in dict_f.keys():
        dict_f[key] = letters[dict_f[key]]
        formula_list[key] = dict_f[key]
    formula = ''.join(formula_list)
    return formula


def formula_hash(latex_formula):
    try:
        return hash(latex_formula)
    except Exception as e:
        raise ValueError(f"Ошибка генерации хэша: {e}")



def compare_formulas(latex_formula1, latex_formula2):
    norm_str1 = latex(latex_formula1)
    norm_str2 = latex(latex_formula2)
    similarity = fuzz.ratio(norm_str1, norm_str2)
    return similarity >= 75, similarity


def all_normalize_formula(latex5):
    return normalize_formula(latex(simplify(rename_variables(str(normalize_formula(latex5))))))

