import requests
import json
import time

s = requests.Session()

def streaming():
    # payload = {'symbols': ','.join(symbols)}
    headers = {'connection': 'keep-alive', 'content-type': 'application/json', 'x-powered-by': 'Express', 'transfer-encoding': 'chunked'}
    req = requests.Request("GET",'http://128.199.176.197:7551/streaming',
                           headers=headers,
                           auth=('a57de080-f7bc-4022-93dc-612d2af58d31', '')).prepare()

    resp = s.send(req, stream=True)

    for line in resp.iter_lines():
        if line:
            # print(line)
            line = line.decode('UTF-8')
            yield line


def read_stream():
    buffer = ""
    while (True):
        for line in streaming():
            
            if line == '[{':
                buffer = "{"
            elif line == '},{':
                buffer += '}'
                yield json.loads(buffer)
                time.sleep(1)
                buffer = '{'  
            elif line == '  }' and "7b4700b2-0801-4626-8cf1-33c8f71dd9f4" in buffer:
                buffer += '}}'
                yield json.loads(buffer)
                time.sleep(1)
                break
            else:
                buffer += line

if __name__ == '__main__':
    for i in read_stream():
        print(i)
        print()
        pass