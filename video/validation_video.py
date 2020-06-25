from django.shortcuts import render,HttpResponse
#!/usr/bin/python3
import cv2
import os
import shutil 
import hashlib
import sys 
import json
import ipfshttpclient
import subprocess

def _acao_response(response,csrf_token):
  response['Access-Control-Allow-Orgin']= '*'
  response['Access-Control-Allow-Method']='POST'
  response['Access-Control-Allow-Headers']='x-requseted-with,content-type,Orgin,X-Requested-With,Content-Type,Accept,Connection,User,Agent,Cookie,X-CSRF-TOKEN,withCredentials'
  response['X-CSRF-TOKEN']=csrf_token
  return response

def main(request):
  if(request.method=='POST'):
    received_json_data=json.loads(request.body)
    test_video_hash = received_json_data['test_video_hash']
    test_frame_hash_array = received_json_data['test_frame_hash_array'].split('-')
    csrf_name = received_json_data['csrf_name']
    if(os.path.isfile("hash_recode_compare.txt")):
      os.remove("hash_recode_compare.txt")  
    hash_recode = open("hash_recode_compare.txt", "w+")
    # ipfs_client = ipfshttpclient.connect('/ip4/192.168.1.133/tcp/5001')
    ipfs_client = ipfshttpclient.connect('/dns/192.168.1.133/tcp/5001/http')
    ipfs_client.get(test_video_hash)
    videos_src_path = '/var/www/html/process_trace_data'
    videos_save_path = '/var/www/html/traceability_project/public/'
    #如果redis呼叫的檔案會出現在執行背景執行指令的地方
    # os.rename('/var/www/html/traceability_project/'+test_video_hash,'/var/www/html/traceability_project/public/'+test_video_hash+'.avi')

    #os.remove(/var/www/html/traceability_project/'+test_video_hash)
    #一般手動測試時
    os.rename('/var/www/html/process_trace_data/'+test_video_hash,'/var/www/html/process_trace_data/'+test_video_hash+'.avi')
    # if(os.path.isdir((videos_save_path + '/' + 'video_ppm'))):
    #   shutil.rmtree(videos_save_path + '/' + 'video_ppm')
    # os.mkdir(videos_save_path + '/' + 'video_ppm')
    # os.chmod(videos_save_path + '/' + 'video_ppm', 777)
    # video_save_full_path = os.path.join(videos_save_path,'video_ppm')+'/'
    video_full_path =  os.path.join(videos_src_path,test_video_hash+'.avi')
    print(video_full_path)
    # video_full_path =  os.path.join(videos_src_path,test_video_hash)
    cap = cv2.VideoCapture(video_full_path)
    frame_count = 0
    success = True
    check_json={}
    check_json['item_error'] = []
    check_json['IPFS_frame_hash'] = []
    check_json['error_message'] = "not video data"
    while(success):
      success, frame = cap.read()
      # print(type(frame))
      # print(success)
      if(success != False):
        hash_frame = hashlib.sha256(frame.tobytes()).hexdigest()
        if(len(test_frame_hash_array) > frame_count):
          check_json['IPFS_frame_hash'].append(hash_frame)
          if(test_frame_hash_array[frame_count] == hash_frame):
            check_json['check'] = 1
            check_json['error_message'] = ""
            check_json['item_error'].append('ok')
          else:
            check_json['check'] = 0
            check_json['item_error'].append('validation error')
            check_json['error_message'] = "validation error"
        elif(frame_count >= len(test_frame_hash_array)):
            check_json['check'] = 0
            check_json['item_error'].append('test_frame_hash_array more than frame_count')
            check_json['error_message'] = "test_frame_hash_array more than frame_count"
        frame_count = frame_count + 1

      # print(sys.getsizeof(frame.tobytes()))
      # hash_recode.write(hash_frame+"\n")

      # params = []
      # params.append(1)
      # params.append(1)
      #這邊Python權限開設資料夾不足
      # ppm_file = video_save_full_path + 'QmZdUpd9aBJoGrnqSMe9fG3UMJM6qZZ5o3Jv8uMU1ujYd4' + "_%d.ppm" % frame_count
      # cv2.imwrite(ppm_file, frame, params)
      # os.chmod(ppm_file, 777)
    hash_recode.close()
    cap.release()
    if(check_json['check'] == 1):
      p=subprocess.Popen("python3 /var/www/html/process_trace_data/video/avi_to_mp4_with_converter.py "+video_full_path+" "+videos_save_path+" "+test_video_hash, shell=True)  
      p.wait()
    check_json['test_frame_hash_count'] = len(test_frame_hash_array)
    check_json['IPFS_frame_count'] = frame_count
    check_json = json.dumps(check_json)
    # print(check_json)
    response = HttpResponse(check_json,content_type="application/json")
    return _acao_response(response,csrf_name)
  return _acao_response(HttpResponse('json not exit'),'XXXX')
