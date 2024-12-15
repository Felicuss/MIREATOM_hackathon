from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from sympy import latex

from .forms import CustomUserCreationForm, CustomUserProfileForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Formula
from .main import formula_hash, all_normalize_formula, latex_to_sympy, compare_formulas
import json

def article_detail(request, article_id):
    formula = get_object_or_404(Formula, pk=article_id)
    similar_formulas = formula.similar_formulas.all()
    return render(request, 'article_detail.html', {'formula': formula, 'simillar_formula': similar_formulas})

def homepage(request):
    query = request.GET.get('query', '')  # Получаем параметр поиска из URL
    if query:
        formulas = Formula.objects.filter(title__icontains=query).order_by('-created_at')  # Поиск по названию статьи
    else:
        formulas = Formula.objects.all().order_by('-created_at')  # Если запрос пустой, выводим все формулы
    return render(request, 'home.html', {'formulas': formulas, 'query': query})



def search_suggestions(request):
    query = request.GET.get('query', '').strip()
    if query:
        suggestions = Formula.objects.filter(title__icontains=query).values_list('title', flat=True)[:5]
        return JsonResponse({'suggestions': list(suggestions)}, safe=False)
    return JsonResponse({'suggestions': []}, safe=False)


@login_required
def save_formula(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            description = data.get('description')
            latex_code = data.get('latex_code')

            if not latex_code:
                return JsonResponse({'status': 'error', 'message': 'Формула не может быть пустой.'})

            # Нормализуем LaTeX формулу
            normalize_latex = all_normalize_formula(latex_code)

            # Сохраняем формулу в базу данных
            formula = Formula.objects.create(
                title=title,
                description=description,
                latex_code=latex_code,
                normalized_formula=latex(normalize_latex),  # Сохраняем нормализованную формулу
                user=request.user
            )

            # Теперь ищем схожие формулы
            similar_formulas = []
            for existing_formula in Formula.objects.exclude(id=formula.id):
                is_similar, similarity = compare_formulas(latex(normalize_latex), existing_formula.normalized_formula)
                if is_similar:
                    existing_formula.similar_formulas.add(Formula.objects.last().id)
                    similar_formulas.append(existing_formula.id)

            # Добавляем найденные схожие формулы в поле similar_formulas
            formula.similar_formulas.add(*similar_formulas)
            # Сохраняем изменения
            formula.save()

            return JsonResponse({'status': 'success', 'message': f"Формула '{formula.title}' успешно сохранена!"})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Некорректный формат данных.'})

    return JsonResponse({'status': 'error', 'message': 'Недопустимый метод.'})
import logging
logger = logging.getLogger(__name__)

@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        logger.info(f"request.FILES: {request.FILES}")
        form = CustomUserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            saved_user = form.save()
            logger.info(f"Файл сохранен: {saved_user.profile_picture}")
            messages.success(request, "Фото профиля обновлено!")
            return redirect('profile')
        else:
            logger.error(f"Ошибка формы: {form.errors}")
            messages.error(request, f"Ошибка формы: {form.errors}")
    else:
        form = CustomUserProfileForm(instance=user)

    return render(request, 'profile.html', {'form': form})





def formula_editor(request):
    return render(request,'editor.html')

def custom_logout_view(request):
    """Позволяет выйти через GET-запрос"""
    logout(request)
    return redirect('/')  # Перенаправление на главную страницу

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматическая авторизация
            messages.success(request, f'Добро пожаловать, {user.email}! Регистрация прошла успешно.')
            return redirect('profile')  # Перенаправление на профиль после успешной регистрации
        else:
            # Если форма содержит ошибки
            messages.error(request, 'Регистрация не удалась. Проверьте данные и попробуйте снова.')
    else:
        form = CustomUserCreationForm()

    # Отображаем страницу регистрации с формой
    return render(request, 'register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')  # Перенаправляем авторизованного пользователя
        return super().get(request, *args, **kwargs)