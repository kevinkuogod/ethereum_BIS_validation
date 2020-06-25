from django.shortcuts import render,HttpResponse
import time
import math
import json

def _acao_response(response,csrf_token):
  response['Access-Control-Allow-Orgin']= '*'
  response['Access-Control-Allow-Method']='POST'
  response['Access-Control-Allow-Headers']='x-requseted-with,content-type,Orgin,X-Requested-With,Content-Type,Accept,Connection,User,Agent,Cookie,X-CSRF-TOKEN,withCredentials'
  response['X-CSRF-TOKEN']=csrf_token
  return response

def avg_end_time(request):
  check_json={}
  if(request.method=='POST'):
    received_json_data=json.loads(request.body) 
    csrf_name = received_json_data['csrf_name']
    start_time_sync_data_file = open("balance_end_time.txt", mode='r')
    count_file_line = 0
    count_iot_end_time = 0
    for file_line in start_time_sync_data_file.readlines():
      if((count_file_line%2)==0):
        Iot_start_time_tmp = math.ceil(float(file_line))
        count_iot_end_time = count_iot_end_time+Iot_start_time_tmp
      count_file_line+=1
    check_json['result'] = str(int(count_iot_end_time/(count_file_line/2)))
    response = HttpResponse(check_json,content_type="application/json")
    #print('count_iot_end_time/(count_file_line/2):'+str(int(count_iot_end_time/(count_file_line/2))))
    return _acao_response(response,csrf_name)
  return _acao_response(HttpResponse('json not exit'),'XXXX')

def avg_recivice_time(request):
  check_json={}
  if(request.method=='POST'):
    received_json_data=json.loads(request.body) 
    csrf_name = received_json_data['csrf_name']
    start_time_sync_data_file = open("balance_recevie_data_time.txt", mode='r')
    count_file_line = 0
    count_iot_recivice_time = 0
    recivice_camera_data_time = 0
    recivice_ldr_data_time = 0
    gap_with_camera_ldr = 0
    for file_line in start_time_sync_data_file.readlines():
      file_line_tmp = file_line.split(',')
      recivice_ldr_data_time = file_line_tmp[0] #ldr
      recivice_camera_data_time = file_line_tmp[1] #camera
      gap_with_camera_ldr = abs(math.ceil(float(recivice_ldr_data_time))-math.ceil(float(recivice_camera_data_time)))
      count_iot_recivice_time = count_iot_recivice_time + gap_with_camera_ldr
      count_file_line+=1
    check_json['result'] =str(int(count_iot_recivice_time/(count_file_line)))
    response = HttpResponse(check_json,content_type="application/json")
    #print('count_iot_recivice_time/(count_file_line/2):'+str(int(count_iot_recivice_time/(count_file_line))))
    return _acao_response(response,csrf_name)
  return _acao_response(HttpResponse('json not exit'),'XXXX')

def avg_start_time(request):
  check_json={}
  if(request.method=='POST'):
    received_json_data=json.loads(request.body) 
    csrf_name = received_json_data['csrf_name']
    start_time_sync_data_file = open("balance_start_time.txt", mode='r')
    count_file_line = 0
    count_iot_start_time = 0
    for file_line in start_time_sync_data_file.readlines():
      if((count_file_line%2)==0):
        Iot_start_time_tmp = math.ceil(float(file_line))
        count_iot_start_time = count_iot_start_time+Iot_start_time_tmp
      count_file_line+=1
    check_json['result'] =str(int(count_iot_start_time/(count_file_line/2)))
    response = HttpResponse(check_json,content_type="application/json")
    #print('count_iot_start_time/(count_file_line/2):'+str(int(count_iot_start_time/(count_file_line/2))))
    return _acao_response(response,csrf_name)
  return _acao_response(HttpResponse('json not exit'),'XXXX')