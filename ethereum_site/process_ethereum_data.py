from django.shortcuts import render,HttpResponse
import sys
import time
import json
import hashlib
# 連線方法一
# from web3 import Web3
# ipc 會需要root權限，網頁部分不實用
# my_provider = Web3.IPCProvider('/opt/privatechain/data0/geth.ipc')
# w3 = Web3(my_provider)

# 連線方法二
import web3
from web3.auto import w3

def _acao_response(response,csrf_token):
  response['Access-Control-Allow-Orgin']= '*'
  response['Access-Control-Allow-Method']='POST'
  response['Access-Control-Allow-Headers']='x-requseted-with,content-type,Orgin,X-Requested-With,Content-Type,Accept,Connection,User,Agent,Cookie,X-CSRF-TOKEN,withCredentials'
  response['X-CSRF-TOKEN']=csrf_token
  return response

def main(request):
    connected = w3.isConnected()
    if(request.method=='POST'):
        received_json_data=json.loads(request.body) 
        asset_ID = received_json_data['asset_ID']
        test_iot_data_array = received_json_data['test_iot_data_array'].split('+')
        test_yolo_tag_array = received_json_data['test_yolo_tag_array'].split('+')
        test_frame_hash_array = received_json_data['test_frame_hash_array'].split('+')
        tx_hex_data_array = received_json_data['tx_hex_data_array'].split('-')
        mongoID_data_array = received_json_data['mongoID_data_array'].split('-')
        csrf_name = received_json_data['csrf_name']
        check_json={}
        if connected and w3.clientVersion.startswith('Geth'):
            tx_parameter_array = []
            for i in range(len(test_iot_data_array)):
                tx_json={}
                tx_json['asset_ID'] = asset_ID
                tmp_iot_data = test_iot_data_array[i].split('-')
                sensor_ldr_total_value = -1
                sensor_yolo_tag_value = ''
                sensor_frame_hash_value = ''
                for tmp_sensor_ldr_data in tmp_iot_data:
                    sensor_ldr_total_value = sensor_ldr_total_value+int(tmp_sensor_ldr_data)
                tx_json['sensor_idr_total_value_hash'] = hashlib.sha256(str(sensor_ldr_total_value).encode()).hexdigest()
                tmp_iot_data = test_yolo_tag_array[i].split('-')
                for tmp_yolo_tag_data in tmp_iot_data:
                    sensor_yolo_tag_value = sensor_yolo_tag_value+tmp_yolo_tag_data
                tx_json['yolo_tag_total'] = hashlib.sha256(sensor_yolo_tag_value.encode()).hexdigest()
                tmp_iot_data = test_frame_hash_array[i].split('-')
                for tmp_frame_hash_data in tmp_iot_data:
                    sensor_frame_hash_value = sensor_frame_hash_value+tmp_frame_hash_data
                tx_json['frame_hash_total'] = hashlib.sha256(sensor_frame_hash_value.encode()).hexdigest()
                tx_json['mongodb_insert_id'] = mongoID_data_array[i]
                tx_json = json.dumps(tx_json)
                tx_parameter_array.append(tx_json)

            # TransactionReceipt = w3.eth.getTransactionReceipt("0xbfd8e9902ea3294186e19fcbce186a9222848cf7d63ae99bf87cb6b7960e9537")
            # Transaction = w3.eth.getTransaction('0xbfd8e9902ea3294186e19fcbce186a9222848cf7d63ae99bf87cb6b7960e9537')
            # # Transaction_function_hash = Transaction.input[0:10]
            # Transaction_splice = Transaction.input[10:]
            # #會去記錄字串長度
            # # Transaction_parameter2_hash_len = w3.toInt(hexstr=('0x'+Transaction_splice[0:64]))
            # Transaction_splice = Transaction_splice[128:]
            # #把交易轉成16進制
            # print(tx_parameter_array[0])
            # parameter_toHex = w3.toHex(text=tx_parameter_array[0])
            # #取得完整的字串大小
            # Transaction_parameter2_hex = '0x'+Transaction_splice[0:len(parameter_toHex)-2]
            # # print('(1)')
            # # print(Transaction_parameter2_hex)
            # print(w3.toText(hexstr=Transaction_parameter2_hex))
            # for i in range(len(tx_parameter_array[0])):
            #     if((w3.toText(hexstr=Transaction_parameter2_hex)[i]) != (tx_parameter_array[0][i])):
            #         print('fined error Transaction_parameter2_hex: %s , tx_parameter_array[0]: %s',(w3.toText(hexstr=Transaction_parameter2_hex)[i]), (tx_parameter_array[0][i]))
            #         break
            #     else:
            #         print('OK')
            #         print('check:'+str(i))
            # if(('{"asset_ID": "Z001"}') == ('{"asset_ID": "Z001"}')):
            #     print('ok')
            # else:
            #     print('error')
            check_json['item_error'] = []
            if(len(test_iot_data_array) == len(tx_parameter_array)):
                for i in range(len(tx_parameter_array)):
                    # 確定有接收到資料
                    # print(tx_hex_data_array[i])
                    try:
                        TransactionReceipt = w3.eth.getTransactionReceipt(tx_hex_data_array[i])
                        Transaction = w3.eth.getTransaction(tx_hex_data_array[i])
                        # Transaction_function_hash = Transaction.input[0:10]
                        Transaction_splice = Transaction.input[10:]
                        #會去記錄字串長度
                        # Transaction_parameter2_hash_len = w3.toInt(hexstr=('0x'+Transaction_splice[0:64]))
                        Transaction_splice = Transaction_splice[128:]
                        #把交易轉成16進制
                        parameter_toHex = w3.toHex(text=tx_parameter_array[i])
                        #取得完整的字串大小
                        Transaction_parameter2_hex = '0x'+Transaction_splice[0:len(parameter_toHex)-2]
                        # if(i == 0):
                        #     print('(1)')
                        #     print(w3.toText(Transaction_parameter2_hex))
                        # print(w3.toText(hexstr=Transaction_parameter2_hex))
                        # print(chardet.detect(Transaction_parameter2_hex.encode()))
                        # print('------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                            # print('(2)')
                            # print(tx_parameter_array[i])
                        # print(chardet.detect(tx_parameter_array[i].encode()))
                        # print('------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                        if(w3.toText(Transaction_parameter2_hex) == tx_parameter_array[i]):
                            check_json['check'] = 1
                            check_json['error_message'] = ""
                            check_json['item_error'].append('ok')
                            # print('ok')
                        else:
                            check_json['check'] = 0
                            check_json['error_message'] = "validation error"
                            check_json['item_error'].append('validation error')
                            # print('error')
                    except:
                        check_json['check'] = 0
                        check_json['error_message'] = "Transaction cannot be validation"
                        check_json['item_error'].append('Not verified')
            else:
                check_json['error_message'] = "tx number error"
                check_json['check'] = 0

            check_json = json.dumps(check_json)
            print(check_json)
            response = HttpResponse(check_json,content_type="application/json")
            return _acao_response(response,csrf_name)
        else:
            enode = None
            check_json['error_message'] = "Not connect to node"
            check_json['check'] = 0
            check_json = json.dumps(check_json)
            print(check_json)
            response = HttpResponse(check_json,content_type="application/json")
            return _acao_response(response,csrf_name)
    return _acao_response(HttpResponse('json not exit'),'XXXX')