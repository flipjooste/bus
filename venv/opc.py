import requests

resp = requests.get('https://integration227992-pmmopc.integration.ocp.oraclecloud.com:443/bpm/api/4.0/tasks',
                    auth=('flip@profmap.com', '!Flip1944!'))


data = resp.json()

#for todo_item in resp.json():
    #print('{} {}'.format(todo_item['id'], todo_item['summary']))