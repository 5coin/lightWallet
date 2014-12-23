import requests
import json
from ctypes import c_uint64

serverURL = 'http://localhost:19091/json_rpc'


def transferFundsRPCCall(amount, address, mixin, paymentid):
    """function to transfer funds to a single address"""
    atomicamount = c_uint64(int((float(amount)*1e12)))
    address = str(address)
    mixin = int(mixin)
    paymentid = str(paymentid)
    mro_fee = c_uint64(int(1e10))
    if len(paymentid) > 1:
        payload = json.dumps({
            "jsonrpc":"2.0",
            "method":"transfer",
            "params":{
                "destinations":[
                {
                    "amount":atomicamount.value,
                    "address":address
                }
                ],
                "fee":mro_fee.value,
                "mixin":mixin,
                "unlock_time":0,
                "payment_id":paymentid
            }
        })
    else:
        payload = json.dumps({
            "jsonrpc":"2.0",
            "method":"transfer",
            "params":{
                "destinations":[
                {
                    "amount":atomicamount.value,
                    "address":address
                }
                ],
                "fee":mro_fee.value,
                "mixin":mixin,
                "unlock_time":0
            }
        })
    print payload

    try:
        headers = {'content-type': 'application/json'}
        resp = requests.get(serverURL, headers=headers, data=payload)
        output = json.loads(resp.text)
        print output
        txid = output[u'result'][u'tx_hash']
        return True, txid

    except:
        error = output[u'error'][u'message']
        return False, error


if __name__ == "__main__":
    transferFundsRPCCall()