import boto3

def detect_text(bucket, key, region="us-east-1"):
	rekognition = boto3.client("rekognition", region)
	response = rekognition.detect_text(
		Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		#MaxLabels=max_labels,
		#MinConfidence=min_confidence,
	)
	return response['TextDetections']

s3 = boto3.client('s3')
bucket='schools2017'
prefix = 'mobiles/STICKER'
file = open('schools2017.csv','w')

for i in s3.list_objects(Bucket=bucket,Prefix=prefix)['Contents']:
    photo=i['Key']
    print(photo)
    try:
        for label in detect_text(bucket, photo):
            print(label['DetectedText'])
            file.write(photo+';'+label['DetectedText'])
    except:
        print('File Error')
file.close()
