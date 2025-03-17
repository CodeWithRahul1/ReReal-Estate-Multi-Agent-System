from django.urls import path
from .views import PropertyListCreateView, PropertyRetrieveUpdateDeleteView, buyer_agent, predict_price, chatbot_query

urlpatterns = [
    path('properties/', PropertyListCreateView.as_view(), name='property-list-create'),
    path('properties/<int:pk>/', PropertyRetrieveUpdateDeleteView.as_view(), name='property-detail'),
    path('buyer-agent/', buyer_agent, name='buyer-agent'),
    path('predict-price/', predict_price, name='predict-price'),
     path('chatbot/', chatbot_query, name='chatbot'),
]
