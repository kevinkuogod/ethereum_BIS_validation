from django.urls import path
from . import hmac
from . import process_background_trace_back_job_table
from . import process_trace_asset_in_leagersite_table

urlpatterns=[
    path('check/hmac',hmac.check_hmac),
    path('process_background_trace_back_job_table/create_background_data',process_background_trace_back_job_table.create_background_data),
    path('process_trace_asset_in_leagersite_table/update_trace_asset_in_leagersite',process_trace_asset_in_leagersite_table.main)
]
