import boto3
import cx_Oracle

s3 = boto3.resource('s3')
my_bucket = s3.Bucket('pmmfacesbucket')
i=1
j=85443

array=[]
connection = cx_Oracle.connect("scholar", "scholar123", "130.61.26.162/PDB1.svcsubnetad1.svcvcn.oraclevcn.com")
cursor = connection.cursor()
print('Connected to Oracle.....')
for key in my_bucket.objects.all():
    fname = key.key
    #if fname.find('.')>=0:
    array.append((j,fname,key.last_modified))
    j+=1
    i+=1
    if i%1000 == 0:
        print('.')
    if i > 10000:
        print('Commited 10000 , Total : ',j)
        cursor.executemany('insert into photos (id,photoname,date_modified) values (:id,:photoname,:date_modified)',array)
        array=[]
        i=1
        connection.commit()

cursor.executemany('insert into photos (id,photoname,date_modified) values (:id,:photoname,:date_modified)',array)
connection.commit()
cursor.close()
connection.close()


