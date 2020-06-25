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

def update_trace_asset_in_leagersite(determine_error, recode_cur_switch_site_pos, asset_id, error_message, determine_main, asset_id_array):
  search_data_condition={"asset_RFID":asset_id}
  recode_cur_switch_site_pos =  int(recode_cur_switch_site_pos)
  trace_asset_in_leagersite = db.trace_asset_in_leagersite
  search_data_list=trace_asset_in_leagersite.find(search_data_condition)[0]

  update_error = search_data_list['error']
  update_error[recode_cur_switch_site_pos].append(determine_error)
  update_time = time.strftime("%Y-%m-%d %H-%M-%S")

  
  checksum_data = ""
  checksum_data = checksum_data+'asset_RFID'+search_data_list['asset_RFID']
  checksum_data = checksum_data+'leager_site_id_array'+str(search_data_list['leager_site_id_array'])
  checksum_data = checksum_data+'switch_site_id_array'+str(search_data_list['switch_site_id_array'])
  checksum_data = checksum_data+'error'+str(update_error)
  error_item = search_data_list['error_item']
  error_time = search_data_list['error_time']
  if(error_message != "null"):
    if(determine_main == 1):
      error_item[recode_cur_switch_site_pos] = asset_id_array
    else:
      error_item[recode_cur_switch_site_pos] = [asset_id_array[len(asset_id_array)-1]]
  error_time[recode_cur_switch_site_pos].append(update_time)
  checksum_data = checksum_data+'error_item'+str(error_item)
  checksum_data = checksum_data+'error_time'+str(error_time)
  checksum_data = checksum_data+'create_time'+str(search_data_list['create_time'])
  checksum_data = checksum_data+'update_time'+str(update_time)
  checksum_data = _generate_signature(checksum_data)

  search_update_condition={"_id":search_data_list['_id']}
  update_parameter={"$set":{'asset_RFID':search_data_list['asset_RFID'],\
                            'leager_site_id_array':search_data_list['leager_site_id_array'],\
                            'switch_site_id_array':search_data_list['switch_site_id_array'],\
                            'error':update_error,\
                            'error_item':error_item,\
                            'error_time':error_time,\
                            'create_time':search_data_list['create_time'],\
                            'update_time':update_time,\
                            'checksum':checksum_data
  }}
  realtime_data_id = trace_asset_in_leagersite.update(search_update_condition, update_parameter)




def main(request):
  if(request.method=='POST'):
    received_json_data=json.loads(request.body)
    #error or ok
    determine_error=received_json_data['determine_error']
    #asset_id
    recode_cur_switch_site_pos_array=received_json_data['recode_cur_switch_site_pos_array'].split('--')
    asset_id_array=received_json_data['asset_id_array'].split('--')
    error_message=received_json_data['error_message']
    csrf_name=received_json_data['csrf_name']
  
    if(len(asset_id_array) == 1):
      update_trace_asset_in_leagersite(determine_error, recode_cur_switch_site_pos_array[0], asset_id_array[0], error_message, 1, asset_id_array)
    elif(len(asset_id_array) > 1):
      update_trace_asset_in_leagersite(determine_error, recode_cur_switch_site_pos_array[0], asset_id_array[0], error_message, 1, asset_id_array)
      update_trace_asset_in_leagersite(determine_error, recode_cur_switch_site_pos_array[len(recode_cur_switch_site_pos_array)-1], asset_id_array[len(asset_id_array)-1], error_message, 0, asset_id_array)


    check_json={}
    check_json['error']='ok'
    check_json = json.dumps(check_json)
    #print(check_json)
    response = HttpResponse(check_json,content_type="application/json")
    return _acao_response(response,csrf_name)
  return _acao_response(HttpResponse('json not exit'),'XXXX')
