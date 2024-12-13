from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import profile, register_view, CustomLoginView, formula_editor, save_formula, homepage, article_detail, search_suggestions
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('profile/', profile, name='profile'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register_view, name='register'),
    path('formula/', formula_editor, name='editor'),
    path('save-formula/', save_formula, name='save_formula'),
    path('', homepage, name='homepage'),
    path('article/<int:article_id>/', article_detail, name='article_detail'),
    path('search-suggestions/', search_suggestions, name='search_suggestions'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
