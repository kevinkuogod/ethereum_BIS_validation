from django.shortcuts import render,HttpResponse
import hashlib
import hmac
import sys
import time
import json

def _acao_response(response,csrf_token):
  response['Access-Control-Allow-Orgin']= '*'
  response['Access-Control-Allow-Method']='POST'
  response['Access-Control-Allow-Headers']='x-requseted-with,content-type,Orgin,X-Requested-With,Content-Type,Accept,Connection,User,Agent,Cookie,X-CSRF-TOKEN,withCredentials'
  response['X-CSRF-TOKEN']=csrf_token
  return response

def _generate_signature(data):
  return hmac.new('kevin'.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest()

def check_hmac(request):
  if(request.method=='POST'):
    received_json_data=json.loads(request.body)
    data_array=[]
    for json_data in received_json_data:  
      data_array.append(str(received_json_data[json_data]))

    checksum_data = ""
    calculator_num = 0
    check_json={}
    csrf_name=data_array[len(data_array)-2]
    test_compare=data_array[len(data_array)-1]
    print(len(data_array))
    print(data_array)
    print(data_array[3])
    #-1為比較的值
    #-2為比較的值與csrf
    get_total = int((len(data_array)-2)/3)
    for i in range(get_total):
      calculator_num = i*3
      if(data_array[calculator_num+1] == '0'):
        checksum_data = checksum_data+data_array[calculator_num]
      if(data_array[calculator_num+1] == '1'):
        data_array[calculator_num+2] = data_array[calculator_num+2].replace('---',' ')
        checksum_data = checksum_data+data_array[calculator_num]
        checksum_data = checksum_data+data_array[calculator_num+2]
      if(data_array[calculator_num+1] == '2'):
        checksum_data = checksum_data+data_array[calculator_num]
        data_array[calculator_num+2] = data_array[calculator_num+2].replace('+',', [')
        data_array[calculator_num+2] = data_array[calculator_num+2].replace('---',' ')
        data_array_2 = data_array[calculator_num+2].split('--')
        checksum_data = checksum_data+'['
        for j in range(len(data_array_2)):
          #因為近來星號會被拿掉，且被添加附檔名
          # if(data_array[j][(len(data_array[j])-4):len(data_array[j])] == ".avi"):
          #   data_array[j] = "'"+data_array[j][0:(len(data_array[j])-4)]+"'"
          #用Redis會造成的情況
          # if( (data_array[calculator_num] == 'video_IPFS_hash_array') and (data_array[j][0] != "'") and (data_array[j][0] != "*")):
          #   data_array[j] = "'"+data_array[j]+"'"
          if(data_array[calculator_num] == 'video_IPFS_hash_array'):
            #-2是減掉多的加長字元與*號，結尾才需要預先補單引號
            data_array_2[j] = data_array_2[j][0:(len(data_array_2[j])-2)]+"'"
          if(j==0):
            checksum_data = checksum_data+data_array_2[j]
          else:
            checksum_data = checksum_data+', '+data_array_2[j]
        checksum_data = checksum_data+']'
    checksum_data = checksum_data.replace("*","'")
    checksum =_generate_signature(checksum_data)
    if(test_compare == checksum):
      check_json['error']='ok'
    else:
      check_json['error']='error'
    check_json = json.dumps(check_json)
    # print(check_json)
    # print(test_compare)
    print(checksum_data)
    # print(checksum)

    response = HttpResponse(check_json,content_type="application/json")
    return _acao_response(response,csrf_name)
  return _acao_response(HttpResponse('json not exit'),'XXXX')
