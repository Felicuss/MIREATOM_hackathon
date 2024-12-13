from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from .forms import CustomUserCreationForm, CustomUserProfileForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Formula
from .main import formula_hash, all_normalize_formula
import json

def article_detail(request, article_id):
    formula = get_object_or_404(Formula, pk=article_id)
    return render(request, 'article_detail.html', {'formula': formula})

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

            # Нормализуем и получаем хэш от LaTeX формулы
            normalize_latex = all_normalize_formula(latex_code)
            latex_hash = formula_hash(normalize_latex)

            # Проверяем, существует ли уже такая формула по хэш-коду
            existing_formula = Formula.objects.filter(latex_hash=latex_hash).first()
            if existing_formula:
                # Возвращаем информацию о существующей формуле
                return JsonResponse({'status': 'duplicate', 'message': 'Такая формула уже существует.', 'formula': {
                    'title': existing_formula.title,
                    'latex_code': existing_formula.latex_code,
                }})

            # Сохраняем новую формулу
            formula = Formula.objects.create(
                title=title,
                description=description,
                latex_code=latex_code,
                latex_hash=latex_hash,
                user=request.user
            )
            return JsonResponse({'status': 'success', 'message': f"Формула '{formula.title}' успешно сохранена!"})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Некорректный формат данных.'})

    return JsonResponse({'status': 'error', 'message': 'Недопустимый метод.'})


@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        form = CustomUserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Фото профиля обновлено!")
            return redirect('profile')
    else:
        form = CustomUserProfileForm(instance=user)

    return render(request, 'profile.html', {'form': form})


def formula_editor(request):
    return render(request,'editor.html')

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