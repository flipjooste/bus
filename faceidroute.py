import boto3
import io
from PIL import Image
import cx_Oracle
import csv

#connection = cx_Oracle.connect("scholar", "scholar123", "130.61.26.162/PDB1.svcsubnetad1.svcvcn.oraclevcn.com")
#cursor = connection.cursor()
#print('Connected to Oracle.....')

rekognition = boto3.client('rekognition', region_name='eu-west-1')
dynamodb = boto3.client('dynamodb', region_name='eu-west-1')
s3 = boto3.resource('s3')
my_bucket = s3.Bucket('pmmflip')
bucket = 'pmmflip'

i=0
cnt=0
fw=1
f = open('g:/gde/facesFlipPmm.csv','w')
f.write('EMIS_NUMBER;NAMES;SCHOOL_NAME;LAT;LON;GPS_TIME;FACE_ID;STUDENT_REKOGNITION_ID;ON_OFF;PHOTONAME;ROUTE_GUID;AGENT;DRIVER;REGNUMBER;CONFIDENCE;SIMiLARITY\n')
print('File opened.....')
for key in my_bucket.objects.all():
    fname = key.key

    print(fname)

    if ((fname.find('_IN_')>=0 or fname.find('_OUT_')>=0) and fname.find('COMPLETED')<0) and fname.find('_-24') < 0:
        cnt+=1
        #cursor.execute('select photoname from sr_new where photoname = :fname',fname=fname)
        #if cursor.fetchone():
        if cnt == 0:
            pass
            print('Read header...')
        else:
            emisnumber = 'NOT AVAILABLE'
            names = 'NOT AVAILABLE'
            schoolname = 'NOT AVAILABLE'
            faceid = 'NOT AVAILABLE'
            user = ''
            driver = ''
            regnumber  = ''
            studentrekognitionid = 'NOT AVAILABLE'
            sname= fname.split('_')
            route_guid = sname[0][6:] + '_' + sname[1]
            if sname[3].startswith('-') or sname[3].startswith('0.0'):
                lat = sname[3]
                lon = sname[4]
                gps_time = sname[5] + ' ' + sname[6]
            elif sname[3].startswith('BUS'):
                lat=sname[7]
                lon=sname[8]
                gps_time = sname[9] + ' ' + sname[10]
                user = sname[3]
                driver = sname[4]
                regnumber = sname[5]
            else:
                lat = sname[4]
                lon = sname[5]
                gps_time = sname[6] + ' ' + sname[7]

            on_off = sname[2]
            if on_off == 'IN':
                on_off = 'ON'
            else:
                on_off = 'OFF'
            #s3.Bucket('pmmflip').download_file(fname,'rekon.jpg' )
            try:
                #image = Image.open('rekon.jpg')
                #stream = io.BytesIO()
                #image.save(stream,format="JPEG")
                #image_binary = stream.getvalue()
                response = rekognition.search_faces_by_image(
                    CollectionId='pmmfacescollection',
                    FaceMatchThreshold = 99,
                    Image={'S3Object': {'Bucket': bucket, 'Name': fn ame}}
                )
                for match in response['FaceMatches']:
                    print (match['Face']['FaceId'],match['Face']['Confidence'])
                    print (match['Similarity'])

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
                        confidence = match['Face']['Confidence']
                        similarity = match['Similarity']
                        if studentrekognitionid.find('_') == -1:
                            studentrekognitionid = studentrekognitionid[0:-4:]+'_'+studentrekognitionid[-4:]

                        #print('\n{0}:{1}:{2}:{3}:{4}:{5}:{6}:{7} :{8}:{9}:{10}:{11}:{12}:{13}'
                        #    .format(emisnumber,names,schoolname,lat,lon,gps_time,faceid,studentrekognitionid,on_off,fname,route_guid,user,driver,regnumber))
                        f.write('{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11};{12};{13};{14};{15}\n'
                            .format(emisnumber,names,schoolname,lat,lon,gps_time,faceid,studentrekognitionid,on_off,fname,route_guid,user,driver,regnumber, confidence,similarity))
                        fw+=1
                        if fw % 10 == 0:
                            f.flush()
                            print('Flush......')
                    else:
                        print ('no match found in person lookup')
                        print('{0}:{1}:{2}:{3}:{4}:{5}:{6}:{7} :{8}:{9}'
                            .format(emisnumber,names,schoolname,lat,lon,gps_time,faceid,studentrekognitionid,on_off,fname))
                        f.write('{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11};{12};{13}\n'
                            .format(emisnumber,names,schoolname,lat,lon,gps_time,faceid,studentrekognitionid,on_off,fname,route_guid,user,driver,regnumber))
                    break
            except:
                print('\nerror with file',cnt)
                print ('no match found in person lookup')
                print('{0}:{1}:{2}:{3}:{4}:{5}:{6}:{7} :{8}:{9}'
                    .format(emisnumber,names,schoolname,lat,lon,gps_time,faceid,studentrekognitionid,on_off,fname))
                f.write('{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11};{12};{13}\n'
                    .format(emisnumber,names,schoolname,lat,lon,gps_time,faceid,studentrekognitionid,on_off,fname,route_guid,user,driver,regnumber))
                match = ''
                responce=''

        #key.delete()
f.close()
