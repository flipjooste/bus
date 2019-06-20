import cv2
import numpy as np
import pytesseract
from PIL import Image
import os
import re

def sort_contours(cnts, method="left-to-right"):
	# initialize the reverse flag and sort index
	reverse = False
	i = 0

	# handle if we need to sort in reverse
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True

	# handle if we are sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1

	# construct the list of bounding boxes and sort them from top to
	# bottom
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))

	# return the list of sorted contours and bounding boxes
	return (cnts, boundingBoxes)

def sort_cnts(contours):
    myContours = []
    # Process the raw contours to get bounding rectangles
    for cnt in reversed(contours):

        epsilon = 0.1*cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,True)

        if len(approx == 4):

            rectangle = cv2.boundingRect(cnt)
            myContours.append(rectangle)

    max_width = max(myContours, key=lambda r: r[0] + r[2])[0]
    max_height = max(myContours, key=lambda r: r[3])[3]
    nearest = max_height * 1.4
    myContours.sort(key=lambda r: (int(nearest * round(float(r[1])/nearest)) * max_width + r[0]))
    return myContours

def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))

def box_extraction(img_for_box_extraction_path, cropped_dir_path,fname,run):
    img = cv2.imread(img_for_box_extraction_path, 0)  # Read the image
    (thresh, img_bin) = cv2.threshold(img, 128, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Thresholding the image
    img_bin = 255 - img_bin  # Invert the image
    cv2.imwrite("Image_bin.jpg", img_bin)

    myfile = open(directory+fname, 'a+')
    # Defining a kernel length
    kernel_length = np.array(img).shape[1] // 180

    # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    # A kernel of (3 X 3) ones.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # Morphological operation to detect verticle lines from an image
    img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=3)
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
    cv2.imwrite("verticle_lines.jpg", verticle_lines_img)
    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
    cv2.imwrite("horizontal_lines.jpg", horizontal_lines_img)
    # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
    alpha = 0.5
    beta = 1.0 - alpha
    # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
    img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
    (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # For Debugging
    # Enable this line to see verticle and horizontal lines in the image which is used to find boxes
    cv2.imwrite("img_final_bin.jpg", img_final_bin)
    # Find contours for image, which will detect all the boxes
    im2, contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #if(run==1):
    #    contours = sort_cnts(contours)
    # Sort all the contours by top to bottom.
    #(contours, boundingBoxes) = sort_contours(contours, method="left-to-right")
    contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[1])
    #contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * img_final_bin.shape[1])
    idx = 0
    biggest=0
    xp=0;yp=0
    outputstr=''
    for c in contours:
        # Returns the location and width,height for every contour
        x, y, w, h = cv2.boundingRect(c)
        # If the box height is greater then 20, widht is >80, then only save it as a box in "cropped/" folder.
        if (h*w > biggest and h*w < 8600080 and run == 0) :
            idx += 1
            cnt=c
            rect = cv2.minAreaRect(cnt)
            print(h*w)
            biggest = h*w
            new_img = img[y:y + h, x:x + w]
            cv2.imwrite(cropped_dir_path + 'biggest.png', new_img)
        if (w > 110 and w < 800 and h > 10 and h < 320) and run==1:
            idx += 1
            new_img = img[y:y + h, x:x + w]
            #new_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(cropped_dir_path +  '_' + sprovider + '_' + str(idx) + '.png', new_img)
            config = ('--oem 3 --psm 6')
            text = pytesseract.image_to_string(new_img,config=config)
            text = re.sub(r"[^a-zA-Z0-9]+", ' ', text)
            #print(text)
            #os.remove(filename)
            if x < xp:
                xp=0
                outputstr=outputstr.split('\n')
                #outputstr=outputstr.rstrip()
                #print(outputstr)
                myfile.write(''.join(outputstr) + ';' +  school_name + ';' + sprovider+'\n')
                print(''.join(outputstr) + ',' +  school_name + ',' + sprovider)
                outputstr=''
            else:
                outputstr=outputstr + ';'
                xp=x
            outputstr = outputstr+text
            #print('x: {0} y: {1} Text: {2} xp:{3}'.format(x,y,text,xp))

    if run == 0:
        p = np.array(rect[1])
        print(str(rect[-1]))
        if p[0] < p[1]:
            print("Angle along the longer side:1 " + str(rect[-1] + 180))
            act_angle = rect[-1] + 180
        else:
            print("Angle along the longer side:2 " + str(rect[-1] + 90))
            act_angle = rect[-1]
        # act_angle gives the angle of the minAreaRect with the vertical

        if act_angle < 90:
            angle = (act_angle)
            print("angleless than -45")

        # otherwise, just take the inverse of the angle to make
        # it positive
        else:
            angle = act_angle - 90
            print("grter than 90")

        if angle < 45:
            angle = 0-angle

        print(angle)
        (h, w) = new_img.shape[:2]
        center = (w // 2, h // 2)
        #M = cv2.getRotationMatrix2D(center, angle+0.1, 1.0)
        #rotated = cv2.warpAffine(new_img, M, (h, w), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        rotated = rotate_bound(new_img,angle+0.6)

        cv2.imwrite("img_final_binR.jpg", rotated)


#emis = input('Emis No :')
school_name =''
sprovider=''
directory = 'c:/Users/flip/Documents/GDE/Bus/L1/'
tesseract_cmd = 'C:\Program Files\Tesseract-OCR\tesseract'
for root, dirs, files in os.walk(directory):
    for file_ in files:

        if file_.find('.jpg') >=0:

            print(os.path.join(root, file_))
            image = Image.open(os.path.join(root, file_))
            config = ('--oem 1 --psm 3')

            lines = pytesseract.image_to_string(image,config=config)  # print ocr text from image
            scanl = lines.split("\n")

            for line in scanl:
                if line.find('NAME OF SCHOOL') >= 0:
                    school_name = line.replace('NAME OF SCHOOL', '')
                if line.find('NAME SERVICE PROVIDER') >= 0:
                    sprovider = line.replace('NAME SERVICE PROVIDER', '')

            fname = os.path.join(root, file_)
            print(root)
            ofname=root.split('/')
            print(ofname[5])
            ofname = ofname[5] +'.csv'
            print(ofname)
            box_extraction(os.path.join(root, file_),directory,ofname,0)
            box_extraction("img_final_binR.jpg",directory,ofname,1)
