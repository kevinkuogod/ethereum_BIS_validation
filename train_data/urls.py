from django.urls import path
from . import avg_calculator,start_time_train

urlpatterns=[
    path('avg_calculator/avg_end_time',avg_calculator.avg_end_time),
    path('avg_calculator/avg_recivice_time',avg_calculator.avg_recivice_time),
    path('avg_calculator/avg_start_time',avg_calculator.avg_start_time),
    path('start_time_train/start_time_train',start_time_train.start_time_train)
]
