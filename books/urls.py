from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('browse/',views.browse_books,name='browse_books'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-book/',views.add_book,name='add_book'),
    path('issue-book/',views.issue_book,name='issue_book'),
    path('return-book/',views.return_book,name='return_book'),
]