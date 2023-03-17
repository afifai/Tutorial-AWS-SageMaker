import os
import io
import boto3
import json
import csv

from io import BytesIO
import numpy as np

# Gunakan environment variable
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime= boto3.client('runtime.sagemaker')



def lambda_handler(event, context):
    print("Event yang diterima: " + json.dumps(event, indent=2))
    
    data = json.loads(json.dumps(event))
    payload = data['data']
    
    # Serialisasi NumPy Array sebagai bytefile
    buffer = BytesIO()
    # Payload adalah string, ubah menjadi list
    np.save(buffer, [payload])
    
    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT_NAME, Body=buffer.getvalue(), ContentType="application/x-npy"
    )
    
    result = eval(response["Body"].read().decode())[0]
    
    return {
        'statusCode': 200,
        'data': {'input_sms':payload,
                 'prediksi': result}
    }
