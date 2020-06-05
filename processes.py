#%%
import os
import re
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

list = [110010,110014,90222,80121,90227,90230,80123,90232,80125,
        100001,100003,170021,180009]



file = open('processesList.csv','w')
file.write('processid;state;user;tasktype;taskid;action;pmmid;region;priority;'
           'updatedDate;checklistqa;version;facilityName;facility;user;'
           'function_structure;floors;x;y;local_mun;district_mun;digit_21code;'
           'description;address;comments\n')
PARAMS = {'processState':'OPEN','LIMIT':'0'}
dpw = 'https://db.profmapcloud.com/ords/PDB1/dpw/buildings/'
response = requests.get('https://integration227992-pmmopc.integration.ocp.'
                        'oraclecloud.com:443/bpm/api/4.0/processes?processState=OPEN&processState=COMPLETED&limit=5000',
                        auth=('flip@profmap.com', '!Flip1944!'))
data = response.json()
cnt=0
items = data['items']
headers = {'Accept': 'application/json'}
for i in items:  #Loop all processes
    processId = i['processId']
    print(processId)
    if int(processId) not in list:
        print('In List')
        processState = i['state']
        v = re.search('!(.+?)~',i['processDN'])
        if v:
            version = v.group(1)
        response_process = requests.get('https://integration227992-pmmopc.integration.ocp.oraclecloud.com:443/bpm/api/4.0/processes/'+str(i['processId']+'/audit?graphicFlag=False'),
                                auth=('flip@profmap.com', '!Flip1944!'))
        data_process = response_process.json()
        history = data_process['processHistory']
        for h in history:
            #tasknumber = 0
            #taskstate = ''
            activityName = h['activityName'].rstrip('\n')
            activityType = h['activityType']
            tempstr = h['updatedDate'].split('T')
            activityDate=tempstr[0]
            if activityType == 'USER_TASK':
                taskHistory = h['taskHistory']
                for th in taskHistory:
                    tasknumber = th['number']
                    taskstate = th['state']
                    #print(tasknumber)
        urlstr = 'https://integration227992-pmmopc.integration.ocp.oraclecloud.com:443/bpm/api/4.0/tasks/' + str(
            tasknumber) + '/payload'

        response_payload = requests.get(urlstr, auth=('flip@profmap.com', '!Flip1944!'), headers=headers)
        data_payload = response_payload.json()
        pmmbld = data_payload['inputTextPmmBldId']
        print(pmmbld)
        try:
                numberFloors = data_payload['numberFloors']
                bldresponse = requests.get(dpw + pmmbld, verify=False)
                blddata = bldresponse.json()
                # print(data_payload)
                region = blddata['region']
                center_x = blddata['center_x']
                center_y = blddata['center_y']
                local_mun = blddata['local_mun']
                district_mun = blddata['district_mun']
                digit_21code = blddata['digit_21code']
                description = blddata['description']

                priority = blddata['priority']
                checklistqa = data_payload['checklistQA']
                facilityname = data_payload['inputTextFacilityName']
                facility = data_payload['selectFacility']
                user = data_payload['selectUser']
                textAreaAddress = data_payload['textAreaAddress']
                textAreaComments = data_payload['textAreaComments']
                try:
                    textAreaComments = textAreaComments.replace('\n', ',')
                except:
                    textAreaComments
                try:
                    textAreaAddress = textAreaAddress.replace('\n', ',')
                except:
                    textAreaAddress

                print(textAreaAddress)
                print('....\n')
                print(textAreaComments)
                print('')

                try:
                    func = data_payload['selectFuncStruct']
                except:
                    func = ''

                # print('{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11};{12};{13};{14};{15}\n'.
                # format(processId,processState,activityName,activityType,tasknumber, taskstate,pmmbld,region,priority,activityDate,checklistqa,version,facilityname,facility,user,func))
                file.write('{0};{1};{2};{3};{4};{5};{6};'
                           '{7};{8};{9};{10};{11};{12};{13};'
                           '{14};{15};{16};{17};{18};{19};{20};{21};{22};{23};{24}\n'.
                           format(processId, processState, activityName, activityType,
                                  tasknumber, taskstate, pmmbld, region, priority, activityDate,
                                  checklistqa, version, facilityname, facility, user,
                                  func, numberFloors, center_x, center_y, local_mun,
                                  district_mun, digit_21code, description, textAreaAddress, textAreaComments))
        except:
            print('......')
            print('Error')
            print(processId)
            print('.....')
    cnt+=1

        #if cnt > 20:
        #    break

file.close()
#os.system("aws s3 cp /home/ec2-user/dpw/processes.csv s3://pmmdpw/instructions/processes.csv")
print(cnt)
