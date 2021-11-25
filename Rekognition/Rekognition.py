import os
import boto3
import cv2
import json

access_key_id = 'ASIA4AO7KQFMB5MDRYUQ'
secret_access_key = 'JbgfdE7dcsJnNeIpwRpBfbEYHb3ye3G/SLv7L+JE'
session_token = 'FwoGZXIvYXdzEOT//////////wEaDN+HAMg4IEYTssvI8SLPAbm13hJVWygp461MMOnkFTcfATLjLwvmZ19lDuWvTl6/bP6N59XSOvhOeXqLuqHirUXU9CobEx61+9Uy0ASqlvYKYf0+JhM+O0fs/r3luKRnbPE/M5mDnJ+5UviydrhvDGwv8Jz6n1S8lwX76Y/Tk1/id9e3UJnRGp0Z1BsgYzFA0ARmqO/UKP2K7XNIrETMiC0A4MPOaH5isG/lcFzSm8U3M3ELW13WQVLUku+vGayCbPe1o4O856sR2D8McgP+S47WMooSjkOsUZSp3M6cliiojM6MBjItG8VcvIEAH/vtzNGAu4zsPPS//oMUkfJujA/cAqbL8sAsYDdgfIqBwfAgLZ/0'
region = 'us-east-1'
client = boto3.client('rekognition',
                      region_name=region,
                      aws_access_key_id=access_key_id,
                      aws_secret_access_key=secret_access_key,
                      aws_session_token=session_token)
s3 = boto3.resource(
    service_name='s3',
    region_name=region,
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key,
    aws_session_token=session_token
)
#
# with open(photo,'rb') as source_image:
#     source_bytes=source_image.read()
# response=client.recognize_celebrities(Image={'Bytes': source_bytes})
# if response['CelebrityFaces']==[]:
#     print('true')
# else:
#     print(response['CelebrityFaces'][0]['Name'])
#     print(response['CelebrityFaces'])
# response2=client.start_face_detection(Video={'S3Object': {
#                                          'Bucket': 'rekogniton-bucket',
#                                          'Name': 'Chau bui.mp4'
#
# }})
#
# response4=client.start_face_detection(Video={'S3Object': {
#                                          'Bucket': 'rekogniton-bucket',
#                                          'Name': 'Chau bui 2.mp4'
#
# }})

cam = cv2.VideoCapture("C:\\Users\\Admin\\Downloads\\QC.mp4")
try:
    if not os.path.exists('data'):
        os.makedirs('data')

# if not created then raise error
except OSError:
    print('Error: Creating directory of data')

# frame
currentframe = 0
#
temp = ''
while True:
    ret, frame = cam.read()
    if ret:
        # if video is still left continue creating images
        name = './data/frame' + str(currentframe) + '.jpg'
        # writing the extracted images
        cv2.imwrite(name, frame)
        with open(name, 'rb') as source_image:
            source_bytes = source_image.read()
            with open("Celebrities.json", "r") as fin:
                data = json.load(fin)
                num = 0
                photo = data[num]['CelebID'[0]] + '.jpg'
        response = client.compare_faces(SourceImage={'Bytes': source_bytes}, TargetImage={'Bytes': photo})
        if response['FaceMatches']:
            if temp == '':
                temp = response['FaceMatches']
                print(data[num]['CelebName'][0])
                num += 1
        else:
            num += 1
        currentframe += 1
        num = 0
    else:
        break

# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()
