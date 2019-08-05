import boto3

if __name__ == "__main__":

    bucket = 'scholartransport-ireland'
    collectionId = 'pmmfaces'
    fileName = 'faces/HGG7127PTSP120190614_100214_OUT_BUS33_5402195336089_FL87LWGP_NM3VO1EM_-25.6509753_28.0823913_20190614_1055.JPG'
    threshold = 70
    maxFaces = 2

    client = boto3.client('rekognition')

    response = client.search_faces_by_image(CollectionId=collectionId,
                                            Image={'S3Object': {'Bucket': bucket, 'Name': fileName}},
                                            FaceMatchThreshold=threshold,
                                            MaxFaces=maxFaces)

    faceMatches = response['FaceMatches']
    print ('Matching faces')
    for match in faceMatches:
        print ('FaceId:' + match['Face']['FaceId'])
        print ('ExternalImageId:' + match['Face']['ExternalImageId'])
        print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
        print
