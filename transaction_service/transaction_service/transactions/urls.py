from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.TransactionView.as_view()),
    path('detail/<int:pk>', views.TransactionDetailView.as_view()),
]
