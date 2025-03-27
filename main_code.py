import numpy as np
import cv2 
import function
from pyzbar.pyzbar import decode
import pandas as pd
import json
import sys
from PIL import Image
import urllib.request
import os


def emptyStoredFiles():
    image_files = [os.path.join('OMR_Image', x) for x in os.listdir('OMR_Image')]
    csv_files = [os.path.join('OMR_Output', x) for x in os.listdir('OMR_Output')]
    print(image_files)
    print(csv_files)
    for x in image_files:
        os.unlink(x)
    for x in csv_files:
        os.unlink(x)
    print('Cached Files Removed')


def everything(FTP_Path, FTP_Paper_ID, FTP_Student_ID):
    try:
        emptyStoredFiles()

        urllib.request.urlretrieve(FTP_Path + '/' + FTP_Paper_ID + '/OMR_Image/' + FTP_Student_ID + '.jpg','OMR_Image/' +  FTP_Student_ID + '.jpg')
        image_path = 'OMR_Image/' + FTP_Student_ID + '.jpg'

        img = cv2.imread(image_path)

        if img is None:
            raise Exception('Image file not found.')


        widthImg = 900
        heightImg = 900
        img = cv2.resize(img, (widthImg, heightImg))

        # Convert to grayscale
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)

        # Apply Canny edge detection
        imgCanny = cv2.Canny(imgBlur, 50, 150)  # Adjusted thresholds for better edge detection

        # Finding all contours
        imgContours = img.copy()
        contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 1) 

        #Crop the image 
        #For Roll number
        top, bottom, left, right = 242, 498, 65, 250
        imgCrop = img[top:-bottom, left:-right] 

        #Question number 1 -25
        top, bottom, left, right = 410, 192, 100, 705
        imgCrop1_25 = img[top:-bottom, left:-right] 

        #Question number 26 -50
        top, bottom, left, right = 410, 192, 252, 550
        imgCrop26_50 = img[top:-bottom, left:-right] 

        #Question number 51 -75
        top, bottom, left, right = 410, 192, 405, 400
        imgCrop51_75 = img[top:-bottom, left:-right] 

        #Question number 76-100
        top, bottom, left, right = 410, 192, 555, 250
        imgCrop76_100 = img[top:-bottom, left:-right] 

        #Crop for Set Number
        top, bottom, left, right = 142, 740, 710, 72
        imgCropSet = img[top:-bottom, left:-right] 

        #Resize image if needed
        imgCrop_resized = cv2.resize(imgCrop, (576, 160))
        imgCrop1_25_resized = cv2.resize(imgCrop1_25, (160, 275))
        imgCrop26_50_resized =cv2.resize(imgCrop26_50 ,(100,300))
        imgCrop51_75_resized =cv2.resize(imgCrop51_75 ,(100,300))
        imgCrop76_100_resized =cv2.resize(imgCrop76_100 ,(100,300))
        imgCropSet_resized =cv2.resize(imgCropSet ,(120,18))

        # Convert cropped image  to grayscale
        imgGray = cv2.cvtColor(imgCrop_resized, cv2.COLOR_BGR2GRAY)
        imgGray1_25 = cv2.cvtColor(imgCrop1_25_resized ,cv2.COLOR_BGR2GRAY)
        imgGray26_50 = cv2.cvtColor(imgCrop26_50_resized ,cv2.COLOR_BGR2GRAY)
        imgGray51_75 = cv2.cvtColor(imgCrop51_75_resized ,cv2.COLOR_BGR2GRAY)
        imgGray76_100 = cv2.cvtColor(imgCrop76_100_resized ,cv2.COLOR_BGR2GRAY)
        imgGraySet = cv2.cvtColor(imgCropSet_resized ,cv2.COLOR_BGR2GRAY)

        # Apply threshold 
        imgThreshrollnum = cv2.threshold(imgGray, 150, 255, cv2.THRESH_BINARY_INV)[1]
        imgThresh1_25 = cv2.threshold(imgGray1_25, 150, 255, cv2.THRESH_BINARY_INV)[1]
        imgThresh26_50 = cv2.threshold(imgGray26_50, 150, 255, cv2.THRESH_BINARY_INV)[1]
        imgThresh51_75 = cv2.threshold(imgGray51_75, 150, 255, cv2.THRESH_BINARY_INV)[1]
        imgThresh76_100 = cv2.threshold(imgGray76_100, 150, 255, cv2.THRESH_BINARY_INV)[1]
        imgThreshSet = cv2.threshold(imgGraySet, 150, 255, cv2.THRESH_BINARY_INV)[1]
        #cv2.imshow("Crop", imgThreshSet)
        # cv2.waitKey(0)

        #This is for Roll Number Split Boxes
        boxes = function.splitBoxes(imgThreshrollnum, 10, 16)
        myPixelVal = np.zeros((10, 16))
        countC = 0
        countR = 0

        for image in boxes:
            # Convert to grayscale only if it's not already
            if len(image.shape) == 3 and image.shape[2] == 3:
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray_image = image
            totalPixels = cv2.countNonZero(gray_image)
            if countR < 10 and countC < 16:
                myPixelVal[countR][countC] = totalPixels
            countC += 1
            if countC == 16:
                countR += 1
                countC = 0
        #print(myPixelVal)
        myIndex = np.argmax(myPixelVal, axis=0)
        #print("Roll Number:", myIndex)

        #This is for Question 1-25 Split Boxes

        boxes1_25 = function.splitBoxes(imgThresh1_25, 25, 4)
        myPixelVal1_25 = np.zeros((25, 4))
        countC = 0
        countR = 0

        for image in boxes1_25:
            # Convert to grayscale only if it's not already
            if len(image.shape) == 3 and image.shape[2] == 3:
                gray_image1_25 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray_image1_25 = image
            totalPixels1_25 = cv2.countNonZero(gray_image1_25)
            if countR < 25 and countC < 4:
                myPixelVal1_25[countR][countC] = totalPixels1_25
            countC += 1
            if countC == 4:
                countR += 1
                countC = 0
        # print("myPixelVal1_25",myPixelVal1_25)

        #Apply Conditon if value < 200 have multiple value then 0

        myPixelVal1_25 = np.where(myPixelVal1_25 < 200, 0, myPixelVal1_25)
        mask = (myPixelVal1_25 > 200).sum(axis=1) > 1
        myPixelVal1_25[mask] = 0
        myPixelVal1_25[(myPixelVal1_25 == 0).all(axis=1)] = 0
        myIndex1_25 = np.argmax(myPixelVal1_25, axis=1) + 1
        myIndex1_25[(myPixelVal1_25 == 0).all(axis=1)] = 0
        #print("1-25:", myIndex1_25)


        #This is for Question 26-50 Split Boxes

        boxes26_50 = function.splitBoxes(imgThresh26_50, 25, 4)
        myPixelVal26_50 = np.zeros((25, 4))
        countC = 0
        countR = 0

        for image in boxes26_50:
            # Convert to grayscale only if it's not already
            if len(image.shape) == 3 and image.shape[2] == 3:
                gray_image26_50 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray_image26_50 = image
            totalPixels26_50 = cv2.countNonZero(gray_image26_50)
            if countR < 25 and countC < 4:
                myPixelVal26_50[countR][countC] = totalPixels26_50
            countC += 1
            if countC == 4:
                countR += 1
                countC = 0
        #print("myPixelVal26_50",myPixelVal26_50)

        #Apply Conditon if value < 100 have multiple value then 0
        myPixelVal26_50 = np.where(myPixelVal26_50 < 100, 0, myPixelVal26_50)
        mask = (myPixelVal26_50 > 100).sum(axis=1) > 1
        myPixelVal26_50[mask] = 0
        myPixelVal26_50[(myPixelVal26_50 == 0).all(axis=1)] = 0
        myIndex26_50 = np.argmax(myPixelVal26_50, axis=1) + 1
        myIndex26_50[(myPixelVal26_50 == 0).all(axis=1)] = 0
        #print("26_50:", myIndex26_50)

        #This is for Question 51-75 Split Boxes
        boxes51_75 = function.splitBoxes(imgThresh51_75, 25, 4)
        myPixelVal51_75 = np.zeros((25, 4))
        countC = 0
        countR = 0

        for image in boxes51_75:
            # Convert to grayscale only if it's not already
            if len(image.shape) == 3 and image.shape[2] == 3:
                gray_image51_75 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray_image51_75 = image
            totalPixels51_75 = cv2.countNonZero(gray_image51_75)
            if countR < 25 and countC < 4:
                myPixelVal51_75[countR][countC] = totalPixels51_75
            countC += 1
            if countC == 4:
                countR += 1
                countC = 0
        #print(myPixelVal51_75)

        #Apply Conditon if value < 100 have multiple value then 0
        myPixelVal51_75 = np.where(myPixelVal51_75 < 100, 0, myPixelVal51_75)
        mask = (myPixelVal51_75 > 100).sum(axis=1) > 1
        myPixelVal51_75[mask] = 0
        myPixelVal51_75[(myPixelVal51_75 == 0).all(axis=1)] = 0
        myIndex51_75 = np.argmax(myPixelVal51_75, axis=1) + 1
        myIndex51_75[(myPixelVal51_75 == 0).all(axis=1)] = 0
        #print("51-75:", myIndex51_75)

        #This is for Question 76-100 Split Boxes
        boxes76_100 = function.splitBoxes(imgThresh76_100, 25, 4)
        myPixelVal76_100 = np.zeros((25, 4))
        countC = 0
        countR = 0

        for image in boxes76_100:
            # Convert to grayscale only if it's not already
            if len(image.shape) == 3 and image.shape[2] == 3:
                gray_image76_100 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray_image76_100 = image
            totalPixels76_100 = cv2.countNonZero(gray_image76_100)
            if countR < 25 and countC < 4:
                myPixelVal76_100[countR][countC] = totalPixels76_100
            countC += 1
            if countC == 4:
                countR += 1
                countC = 0
        #print(myPixelVal76_100)

        #Apply Conditon if value < 100 have multiple value then 0
        myPixelVal76_100 = np.where(myPixelVal76_100 < 100, 0, myPixelVal76_100)
        mask = (myPixelVal76_100 > 100).sum(axis=1) > 1
        myPixelVal76_100[mask] = 0
        myPixelVal76_100[(myPixelVal76_100 == 0).all(axis=1)] = 0
        myIndex76_100 = np.argmax(myPixelVal76_100, axis=1) + 1
        myIndex76_100[(myPixelVal76_100 == 0).all(axis=1)] = 0
        #print("51-75:", myIndex76_100)

        #This is for Set Number Split Boxes
        boxSet = function.splitBoxes(imgThreshSet,1, 4)
        myPixelValSet = np.zeros((1, 4)) 

        countC = 0

        for image in boxSet:  
            if len(image.shape) == 3 and image.shape[2] == 3:
                gray_imageSet = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray_imageSet = image
                
            totalPixelsSet = cv2.countNonZero(gray_imageSet)
            
            myPixelValSet[0][countC] = totalPixelsSet
            
            countC += 1
            
        # print(myPixelValSet)
        myIndexSet =np.argmax(myPixelValSet ,axis=1)+1
        #print("Set Number :" ,myIndexSet)

        myPixelValSet = np.where(myPixelValSet < 200, 0, myPixelValSet)
        mask = (myPixelValSet > 200).sum(axis=1) > 1
        myPixelValSet[mask] = 0
        myPixelValSet[(myPixelValSet == 0).all(axis=1)] = 0
        myIndexSet = np.argmax(myPixelValSet, axis=1) + 1
        myIndexSet[(myPixelValSet == 0).all(axis=1)] = 0
        # print("Set:", myIndexSet)

        #This is for Bar code Reading 
        
        def read_barcode(image_path) :
            img =Image.open(image_path)
            decode_object =decode(img)
            for obj in decode_object :
                return obj.data.decode('utf-8')

        #This code is for write csv file

        finalSetNumber = '' if myIndexSet[0] == 0 else chr(65 + myIndexSet[0] - 1)
        finalRollNumber = ''.join(map(str, myIndex))
        # print(finalSetNumber, finalRollNumber)

        allAnswer = np.concatenate((myIndex1_25, myIndex26_50, myIndex51_75, myIndex76_100))
        # print("All Answer :" ,allAnswer)
        finalAns = [finalSetNumber, f"'{read_barcode(image_path)}", f"'{finalRollNumber}"] + [' ' if x == 0 else chr(97 + x - 1) for x in allAnswer]
        # print(len(finalAns))

        columnName = ['Set Number', 'Barcode Value', 'Roll Number']
        for xi in range(100):
            columnName.append('Ans' + str(xi + 1))

        finalResponseRow = [' '] * 103

        finalResultDf = pd.DataFrame([finalAns], columns=columnName)
        finalResultDf.to_csv(f'./OMR_Output/' + FTP_Student_ID + '.csv', encoding='utf-8', index=False)
        # print(finalResultDf)
        return (1, 'success')
    except Exception as e:
        error_msg = str(e)
        return (0, error_msg)