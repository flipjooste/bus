import boto3
import io
from PIL import Image

rekognition = boto3.client('rekognition', region_name='eu-west-1')
dynamodb = boto3.client('dynamodb', region_name='eu-west-1')
s3 = boto3.resource('s3',region_name='eu-west-1')
my_bucket = s3.Bucket('pmmflip')
i=0
f = open('c:/Users/flip/Documents/GDE/faces.csv','w')
f.write('EMIS_NUMBER;NAMES;SCHOOL_NAME;LAT;LON;GPS_TIME;FACE_ID;STUDENT_REKOGNITION_ID;ON_OFF;PHOTONAME,ROUTE_GUID\n')

i=1

for key in my_bucket.objects.filter(Prefix=""):
    fname = key.key
    if (fname.find('_IN_')>=0 or fname.find('_OUT_')>=0):
        print(fname)
        emisnumber = 'NOT AVAILABLE'
        names = 'NOT AVAILABLE'
        schoolname = 'NOT AVAILABLE'
        faceid = 'NOT AVAILABLE'
        studentrekognitionid = 'NOT AVAILABLE'
        sname= fname.split('_')
        lat = sname[3]
        lon = sname[4]
        #snameroute_guid = sname[0].split('/')
        route_guid = sname[0] + '_' + sname[1]
        on_off = sname[2]
        if on_off == 'IN':
            on_off = 'ON'
        else:
            on_off = 'OFF'
        gps_time = sname[5] + ' ' + sname[6]
        copy_source = {
            'Bucket': 'scholartransport',
            'Key': fname
        }
        #bucket = s3.Bucket('pmmflip')
        #bucket.copy(copy_source, 'temp.jpg')
        try:
            response = rekognition.search_faces_by_image(
                CollectionId='pmmfacescollection',
                Image = {
                    "S3Object": {
                        "Bucket": "pmmflip",
                        "Name": fname
                    }
                }
            )
            for match in response['FaceMatches']:
                #   print (match['Face']['FaceId'],match['Face']['Confidence'])

                face = dynamodb.get_item(
                    TableName='pmmfacestable',
                    Key={'RekognitionId': {'S': match['Face']['FaceId']}}
                )

                if 'Item' in face:
                    emisnumber = (face['Item']['emisnumber']['S'])
                    names = (face['Item']['names']['S'])
                    names = names.split('.')[0]
                    schoolname = (face['Item']['schoolname']['S'])
                    studentrekognitionid = (face['Item']['studentrekognitionid']['S'])
                    faceid = match['Face']['FaceId']

                    print('{0}:{1}:{2}:{3}:{4}:{5}:{6}:{7} :{8}:{9}:{10}'
                        .format(emisnumber,names,schoolname,lat,lon,gps_time,faceid,studentrekognitionid,on_off,fname,route_guid))
                    f.write('{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10}\n'
                        .format(emisnumber,names,schoolname,lat,lon,gps_time,faceid,studentrekognitionid,on_off,fname,route_guid))
                else:
                    print ('no match found in person lookup')
                    print('{0}:{1}:{2}:{3}:{4}:{5}:{6}:{7} :{8}:{9}:{10}'
                        .format(emisnumber,names,schoolname,lat,lon,gps_time,faceid,studentrekognitionid,on_off,fname,route_guid))
                    f.write('{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10}\n'
                        .format(emisnumber,names,schoolname,lat,lon,gps_time,faceid,studentrekognitionid,on_off,fname,route_guid))
                break
        except:
            print('Error.....')
    if i % 50 == 0:
        f.flush()
        print('Flush....',i)
    i+=1
f.close()
