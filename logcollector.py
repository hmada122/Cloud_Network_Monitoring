#!/usr/bin/env python



import logging
import socket
import sys
import boto3
import json
import time

#logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='', filename=LOG_FILE, filemode='a')


HOST = '127.0.0.1'
PORT = 514
kinesisClient = boto3.client('kinesis', region_name='eu-west-1')
cloudWatchLogsClient = boto3.client('logs', region_name='eu-west-1')
my_stream_name = 'TU766'

class kinesis():
    def put_to_stream(severity_level, property_value, property_timestamp):
        payload = {
                    'prop': str(property_value),
                    'timestamp': str(property_timestamp),
                    'severity_level': str(severity_level)
                  }

        put_response = kinesisClient.put_record(
                        StreamName=my_stream_name,
                        Data=json.dumps(payload),
                        PartitionKey = '1' )

        if '200' in str(put_response):
            print("Data put success" + "  " + str(put_response) )
           # print( property_value  + '#########' + str(payload) )
        else: 
            print("Error occured while adding records" +  "  " + str(put_response) )
        return str(put_response)

class cloudWatchLogs():
    def putLog(data):
        timestamp = int(round(time.time() * 1000))
        try: 
            response = cloudWatchLogsClient.put_log_events(
                       logGroupName='TU766',
                       logStreamName='allLogs',
                       logEvents=[
                            {
                            'timestamp': timestamp,
                            'message': str(data)
                            },
                        ],             
            sequenceToken='49609702753926248264334932233451343426240057745401376610'
             )
        except Exception as err :
            nextToken = str(err).split(':')[2].replace(' ','')    #Get next token in Cloudwatch logs for assigning it in the put request below
            print("token >>>>>>>>" + nextToken)
            response2 = cloudWatchLogsClient.put_log_events(
                       logGroupName='TU766',
                       logStreamName='allLogs',
                       logEvents=[
                            {
                            'timestamp': timestamp,
                            'message': str(data)
                            },
                        ],
            sequenceToken = nextToken        
	    )
            print(response2)


class logs():
    def logClassifier(data): 
            severity_level = data.decode("utf-8").split(' ')[5].split('-')[2] # Extract severity level form the logs
            property_value = data.decode("utf-8").split('%')[1]               # Extract log message
            property_timestamp = data.decode("utf-8").split(':')[1].replace("*",'')  + ':' +data.decode("utf-8").split(':')[2]+':'+data.decode("utf-8").split(':')[3].replace("'",'')          # Extract time stamp

            logging.basicConfig(filename='example.log',  level=logging.DEBUG)
            if '7' in data.decode("utf-8").split(' ')[5]: #start parsing cisco logs based on logging level refer to https://www.cisco.com/c/en/us/td/docs/routers/access/wireless/software/guide/SysMsgLogging.html
                logging.debug(data.decode("utf-8"))
                kinesis.put_to_stream("debug",property_value,property_timestamp)
                cloudWatchLogs.putLog(data.decode("utf-8"))
            elif '6' in data.decode("utf-8").split(' ')[5] or '5' in data.decode("utf-8").split(' ')[5]:
                logging.info(data.decode("utf-8"))
                kinesis.put_to_stream("info",property_value,property_timestamp)
                cloudWatchLogs.putLog(data.decode("utf-8"))
            elif '4' in data.decode("utf-8").split(' ')[5] :
                logging.warning(data.decode("utf-8"))
                kinesis.put_to_stream("warning",property_value,property_timestamp)
                cloudWatchLogs.putLog(data.decode("utf-8"))
            elif '3' in data.decode("utf-8").split(' ')[5] or'2' in data.decode("utf-8").split(' ')[5] :
                logging.error(data.decode("utf-8"))
                kinesis.put_to_stream("error",property_value,property_timestamp)
                cloudWatchLogs.putLog(data.decode("utf-8"))
            else:
                logging.critical(data.decode("utf-8"))
                kinesis.put_to_stream("critical",property_value,property_timestamp) 
                cloudWatchLogs.putLog(data.decode("utf-8"))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(( HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
            print(data)
            logs.logClassifier(data) 

