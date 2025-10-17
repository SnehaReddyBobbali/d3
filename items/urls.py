from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('post/', views.post_item, name='post_item'),
    path('item/<int:pk>/edit/', views.edit_item, name='edit_item'),
    path('item/<int:pk>/delete/', views.delete_item, name='delete_item'),
    path('my-items/', views.my_items, name='my_items'),
    path('item/<int:pk>/claim/', views.claim_item, name='claim_item'),
    path('my-claims/', views.my_claims, name='my_claims'),
    path('item/<int:pk>/manage-claims/', views.manage_claims, name='manage_claims'),
    path('claim/<int:claim_pk>/update/<str:status>/', views.update_claim_status, name='update_claim_status'),
]
