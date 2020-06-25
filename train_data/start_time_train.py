from django.shortcuts import render,HttpResponse
import time
import json

def _acao_response(response,csrf_token):
  response['Access-Control-Allow-Orgin']= '*'
  response['Access-Control-Allow-Method']='POST'
  response['Access-Control-Allow-Headers']='x-requseted-with,content-type,Orgin,X-Requested-With,Content-Type,Accept,Connection,User,Agent,Cookie,X-CSRF-TOKEN,withCredentials'
  response['X-CSRF-TOKEN']=csrf_token
  return response

def start_time_train(request):
  check_json={}
  if(request.method=='POST'):
    received_json_data=json.loads(request.body) 
    csrf_name = received_json_data['csrf_name']
    start_time_sync_data_file = open("start_time_sync_data.txt", mode='r')
    IOT_data_start_time_array=[]
    camera_data_start_time_array=[]
    count_file_line = 0
    count_iot_data_time=0
    calculator_avg_time=0
    for file_line in start_time_sync_data_file.readlines():
      if((count_file_line%2)==0):
        count_iot_data_time+=1
        #算開始的區間
        file_line_tmp = file_line.split(',')
        file_line_tmp_array=[]
        count_Iot_time=0
        first_iot_second=0
        end_iot_second=0
        for Iot_time in file_line_tmp:
          #去掉小數點之後的值
          Iot_start_time_tmp = Iot_time.split('.')
          timeArray = time.localtime(int(Iot_start_time_tmp[0]))
          otherStyleTime = time.strftime("%M:%S", timeArray)
          print(otherStyleTime)
          Iot_second = otherStyleTime.split(':')[1]
          Iot_second_array=[]
          if(count_Iot_time == 0):  
            first_iot_second = int(Iot_second)
          end_iot_second= first_iot_second-int(Iot_second)
          count_Iot_time+=1
      calculator_avg_time = calculator_avg_time+end_iot_second
      count_file_line+=1
    start_time_sync_data_file.close()
    check_json['result'] = calculator_avg_time/count_iot_data_time
    response = HttpResponse(check_json,content_type="application/json")
    #print(calculator_avg_time/count_iot_data_time)
    return _acao_response(response,csrf_name)
  return _acao_response(HttpResponse('json not exit'),'XXXX')