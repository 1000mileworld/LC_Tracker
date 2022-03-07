from django.urls import path
from .views import ProblemList, ProblemDetail, ProblemCreate, ProblemUpdate, DeleteView, register_view, login_view, problem_list_view, redo_view
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('', ProblemList.as_view(), name='problems'),
    path('', problem_list_view, name='problems'),

    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register_view , name='register'),

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'), name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'), name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset_form.html', email_template_name='password_reset/password_reset_email.html', subject_template_name ='password_reset/password_reset_subject.txt'), name='password_reset'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'), name='password_reset_complete'),

    path('problem/<int:pk>/', ProblemDetail.as_view(), name='problem-detail'),
    path('problem-create/', ProblemCreate.as_view(), name='problem-create'),
    path('problem-update/<int:pk>/', ProblemUpdate.as_view(), name='problem-update'),
    path('problem-delete/<int:pk>/', DeleteView.as_view(), name='problem-delete'),

    path('confirm-redo/<int:pk>', redo_view, name='redo'),
]