from django.shortcuts import render,HttpResponse
import time
import pymongo
import hmac
import hashlib
import sys
import json

client = pymongo.MongoClient("192.168.1.133",27017)
db = client.iotsensordata

def _acao_response(response,csrf_token):
  response['Access-Control-Allow-Orgin']= '*'
  response['Access-Control-Allow-Method']='POST'
  response['Access-Control-Allow-Headers']='x-requseted-with,content-type,Orgin,X-Requested-With,Content-Type,Accept,Connection,User,Agent,Cookie,X-CSRF-TOKEN,withCredentials'
  response['X-CSRF-TOKEN']=csrf_token
  return response

def _generate_signature(data):
  return hmac.new('kevin'.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest()

def create_background_data(request):
  if(request.method=='POST'):
    received_json_data=json.loads(request.body)
    print(received_json_data)
    leager_site=received_json_data['leager_site']
    error_pos=received_json_data['error_pos']
    switch_site_login_id=received_json_data['switch_site_login_id']
    switch_site_logout_id=received_json_data['switch_site_logout_id']
    csrf_name=received_json_data['csrf_name']

    update_time = time.strftime("%Y-%m-%d %H-%M-%S")

    checksum_data = ""
    checksum_data = checksum_data+'leager_site'+leager_site
    checksum_data = checksum_data+'error_pos'+str(error_pos)
    checksum_data = checksum_data+'switch_site_login_id'+str(switch_site_login_id)
    checksum_data = checksum_data+'switch_site_logout_id'+str(switch_site_logout_id)
    checksum_data = checksum_data+'create_time'+str(update_time)
    checksum_data = checksum_data+'update_time'+str(update_time)
    checksum_data = _generate_signature(checksum_data)

    background_trace_back_job = db.background_trace_back_job
    background_trace_back_job_id = background_trace_back_job.insert_one({ 'leager_site':leager_site,\
                                                                          'error_pos':error_pos,\
                                                                          'switch_site_login_id':switch_site_login_id,\
                                                                          'switch_site_logout_id':switch_site_logout_id,\
                                                                          'create_time':update_time,\
                                                                          'update_time':update_time,
                                                                          'checksum':checksum_data
    })
    check_json={}
    check_json['error']='ok'
    check_json = json.dumps(check_json)
    #print(check_json)
    response = HttpResponse(check_json,content_type="application/json")
    return _acao_response(response,csrf_name)
  return _acao_response(HttpResponse('json not exit'),'XXXX')
