import boto3
import cx_Oracle
import pandas as pd


array=[]
connection = cx_Oracle.connect("scholar", "scholar123", "130.61.26.162/PDB1.svcsubnetad1.svcvcn.oraclevcn.com")
cursor = connection.cursor()
s=pd.read_sql_table('student_rekognition',connection)
#cursor.arraysize = 10
#cursor.execute('Select learner_guid,emis_no,learner_name from learners')
#cursor.prepare('insert into faces (id,photoname,date_modified) values (:id,:photoname,:date_modified)')

for key in my_bucket.objects.filter(Prefix=""):
    fname = key.key
    if fname.find('_IN_')>=0 or fname.find('_OUT_')>=0:
        #versions = s3.Bucket('scholartransport').object_versions.filter(Prefix=fname)
        #for version in versions:
        #    obj = version.get()
        #    print(obj.get('VersionId'), obj.get('ContentLength'), obj.get('LastModified'))
        #    array.append((j,fname,key.last_modified,obj.get('VersionId')))
        #    print(array[j-1])
        array.append((j,fname,key.last_modified))
        j+=1
        i+=1
        if i > 10000:
             print('Commited 10000 , Total : ',j)
             cursor.executemany('insert into faces (id,photoname,date_modified) values (:id,:photoname,:date_modified)',array)
             array=[]
             i=0
             connection.commit()

cursor.executemany('insert into faces (id,photoname,date_modified) values (:id,:photoname,:date_modified)',array)
connection.commit()
cursor.close()
connection.close()


 i=0
while True:
    rows = cursor.fetchmany()
    if rows == [] or i>100:
        print('Read 100 records....')
        break;
    print("Fetched {} rows".format(len(rows)))
    for learner_guid,emis_no,learner_name in rows:
        print('GUID : {} , EMIS: {} , NAME: {}'.format(learner_guid,emis_no,learner_name))
        i+=1

cursor.close()
connection.close()
