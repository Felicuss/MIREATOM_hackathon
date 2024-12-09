from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import profile, register_view, CustomLoginView, formula_editor, save_formula, homepage, article_detail

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register_view, name='register'),
    path('formula/', formula_editor, name='editor'),
    path('save-formula/', save_formula, name='save_formula'),
    path('', homepage, name='homepage'),
    path('article/<int:article_id>/', article_detail, name='article_detail'),
]
