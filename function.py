import cv2
import numpy as np

def splitBoxestest(img):
    rows = np.hsplit(img, 4)
    cv2.imshow("Split1", rows[3]) 
    cv2.waitKey(0) 
    
def splitBoxes(img, rows, cols):
    row_splits = np.vsplit(img, rows)
    boxes = []
    for r in row_splits:
        col_splits = np.hsplit(r, cols)
        boxes.extend(col_splits)  
    return boxes

def finalResponseValues(pixelArray):
    final_responses = []

    for x in pixelArray:
        if x[0] < 100 and x[1] < 100 and x[2] < 100 and x[3] < 100:
            final_responses.append(' ')
            continue
        finResp, maxPVal = 0, max(x)
        for ix, pVal in enumerate(x):
            if pVal == maxPVal:
                finResp = ix + 1
                break
        if finResp > 0:
            final_responses.append(chr(97 + finResp - 1))
        else:
            final_responses.append(' ')
    return final_responses