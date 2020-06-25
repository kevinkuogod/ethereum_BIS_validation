from django.urls import path
from . import validation_video

urlpatterns=[
    path('validation_video/main',validation_video.main)
]
