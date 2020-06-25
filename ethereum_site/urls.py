from django.urls import path
from . import process_ethereum_data

urlpatterns=[
    path('process_ethereum_data/main',process_ethereum_data.main)
]
