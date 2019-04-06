from imutils import paths
import cv2
import requests
import os
import uuid
import datetime
import json

"""
    The following is miiCloud's publicly accessible Token.  If you would like to keep you test data separate, email dev@miicloud.io to get your unique Token.  There is no cost to get a token and use the miiCloud Sandbox environment.
    """
auth_token = 'Token 0e653da4969a757d21de0ffa6387d5fbd6401131'
enroll_endpoint = 'https://sandbox.miicloud.io/miicloud/person'
#enroll_endpoint = 'https://mc-sandbox-elb-507714033.us-east-1.elb.amazonaws.com/miicloud/enroll'
match_faces_endpoint = 'https://sandbox.miicloud.io/miicloud/match_faces'
delete_endpoint = 'https://sandbox.miicloud.io/miicloud/person'
get_endpoint = 'https://sandbox.miicloud.io/miicloud/person'
enrollment_image_dir = list(paths.list_images('input/persons'))
test_image_dir = list(paths.list_images('input/test_images'))
output_persons_path = 'output/persons/'
output_test_img_path = 'output/test_images/'


prev_name = ''

##ENROLL VERIFIED PEOPLE IN THE DATABASE##
#Go through each image, generate a unique_id per person and enroll all images in the person's folder
for (i, image_path) in enumerate(enrollment_image_dir):
    #Identify the name of the person being enrolled from folder structure
    curr_name = image_path.split(os.path.sep)[-2]
    
    #Generate a unique identifier per person
    if prev_name != curr_name:
        unique_id = uuid.uuid4().hex
        temp_id = unique_id #temp_id is used to test GET and DELETE operations later on
        prev_name = curr_name

    # Get the actual image from directory
    filename = os.path.basename(image_path)
    #print('image_path %s' % image_path)
    #print('filename %s' % filename.split("."))
    
    #Build a JSON object with Unique Identifier and image
    enrollment_payload = {'customer_person_id': unique_id}
    file = {'image_path': (filename, open(image_path, 'rb'), "multipart/form-data")}

    #Send the Enrollment payload to miiCloud
    print("Enrolling image {}/{}".format(i + 1, len(enrollment_image_dir)) + " for " + curr_name + " w/ Unique ID-> " + unique_id)
    enroll_response = requests.post(enroll_endpoint, headers={'Authorization': auth_token}, data = enrollment_payload, files = file)

    #Check if the enrollment failed
    if enroll_response.status_code != 200:
        print('---API Error---')
        print(enroll_response)
    #print(enroll_response.text)
    #If enrollement is successfull, draw a bounding box around the face, and store the image in output/persons/ folder with timestamp
    else:
        print('  -Enrollment Successful!\n')
        #print(enroll_response.json())
        bounding_box = enroll_response.json()['bounding_box']
        image = cv2.imread(image_path)
        time_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        fn, ext = filename.split(".")
        output_file = output_persons_path + fn + '_' + time_stamp + '.' + ext
        cv2.rectangle(image, (bounding_box['left_x'], bounding_box['left_y']), (bounding_box['right_x'], bounding_box['right_y']), (255,255,0), 2)
        cv2.imwrite(output_file, image)

##MATCH FACES IN TEST IMAGES##
for (i, image_path) in enumerate(test_image_dir):
    
    #Build a JSON object with Unique Identifier and image
    filename = os.path.basename(image_path)
    match_faces_payload = {'image_path': image_path}
    file = {'image_path': (filename, open(image_path, 'rb'), "multipart/form-data")}
    
    #print('image_path %s' % image_path)
    #print('filename %s' % filename.split("."))
    
    #Send the Payload to miiCloud
    print("Processing test image {}/{}".format(i + 1, len(test_image_dir)) + 'file-> ' + filename)
    match_faces_response = requests.post(match_faces_endpoint, headers={'Authorization': auth_token}, data = match_faces_payload, files = file)

    #Check if the API request failed
    if match_faces_response.status_code != 200:
        print('---API Error---')
        print(match_faces_response)
        print()
    #If request is successful, get all the faces from API Response.  Draw a RED box around "unknown" faces and GREEN box around "known" faces.  Then save the image in output/test_images/ folder with timestamp
    else:
        print('  -Match Faces Complete! See results in: ' + output_test_img_path + '\n')
        if len(match_faces_response.json()['faces']) > 0:
            faces = match_faces_response.json()['faces']
            #print(faces)
            image = cv2.imread(image_path)
            time_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            fn, ext = filename.split(".")
            output_file = output_test_img_path + fn + '_' + time_stamp + '.' + ext
            for face in faces:
                bounding_box = face['bounding_box']
                if face['match_status'] == 'unknown':
                    cv2.rectangle(image, (bounding_box['left_x'], bounding_box['left_y']), (bounding_box['right_x'], bounding_box['right_y']), (0,0,255), 2)
                else:
                    cv2.rectangle(image, (bounding_box['left_x'], bounding_box['left_y']), (bounding_box['right_x'], bounding_box['right_y']), (0,255,0), 2)
                    cv2.rectangle(image, (bounding_box['left_x'],bounding_box['right_y']),(bounding_box['right_x'], bounding_box['right_y']+20), (0,255,0), -1)
                    cv2.putText(image, 'Known ' + str(round(face['match_confidence'] * 100, 2)) , (bounding_box['left_x'],bounding_box['right_y']+18), cv2.cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
                  
            cv2.imwrite(output_file, image)



#Testing GET
response = requests.get(get_endpoint + '/' + temp_id, headers={'Authorization': auth_token})
print('Testing successfull Get Person for id: '+ temp_id)
if response.status_code != 200:
    print('  ---GET API Error---')
    print(response.content)
else:
    print(' \'-->GET successfull! ' + '\n  ' + str(response.json()))
    print()


#Testing DELETE
response = requests.delete(delete_endpoint + '/' + temp_id, headers={'Authorization': auth_token})
print('\nTesting successfull Delete Person on id: '  + temp_id)
if response.status_code != 200:
    print('  ---DELETE API Error---')
    print(response.content)
    print('  Could not delete id-> ' + str(temp_id))
else:
    print(' \'-->DELETE successfull for ID-> ' + temp_id )
    print()




