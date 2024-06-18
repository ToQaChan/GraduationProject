import sys
import cv2
import numpy as np
from rembg import remove
import easyocr
import matplotlib.pyplot as plt



def GetCornerPoints(largestContour):
    perimeter =cv2.arcLength(largestContour,closed=True)
    # get the perimeter of polygon by contour
    # are the polygon closed? T/F


    corners =cv2.approxPolyDP(largestContour, 0.02*perimeter ,closed= True)
    #get min points that act as corners of polygon then calc the perimeter by this points 
    # and combare it with perimeter calculated by original contours...

    #acceptable error (epsilon)

    return np.squeeze(corners)
    #return list without unused []
    #before: 
    # [
    #     [[1,2]],
    #     [[1,2]],
    #     [[1,2]],
    # ]

    #after:
    # [
    #     [1,2],
    #     [1,2],
    #     [1,2],
    # ]

def OrderCornerPointClockwise(points):
    rectangel = np.zeros((4,2),dtype="float32")

    axis_sum = np.sum(points,axis=1)
    rectangel[0] = points[np.argmin(axis_sum)]
    rectangel[2] = points[np.argmax(axis_sum)]

    
    axis_diff = np.diff(points,axis=1)
    rectangel[1] = points[np.argmin(axis_diff)]
    rectangel[3] = points[np.argmax(axis_diff)]

    return rectangel

def DrawPointsOnImage(img,points,imgName):
    if len(points) == 4 :
        p1,p2,p3,p4 = points   
        cv2.circle(img,tuple(p1),6,(255,0,0),-1)
        cv2.circle(img,tuple(p2),6,(255,0,255),-1)
        cv2.circle(img,tuple(p3),6,(0,255,0),-1)
        cv2.circle(img,tuple(p4),6,(0,255,255),-1)

    return img

def ApplyTopView(img,points):
    (tl,tr,br,bl) = points

    widthA = np.sqrt(((br[0]-bl[0])**2) + ((br[1]-bl[1])**2))
    widthB = np.sqrt(((tr[0]-tl[0])**2) + ((tr[1]-tl[1])**2))
    maxWidth = min(int(widthA),int(widthB))

    heightA = np.sqrt(((tr[0]-br[0])**2) + ((tr[1]-br[1])**2))
    heightB = np.sqrt(((tl[0]-bl[0])**2) + ((tl[1]-bl[1])**2))
    maxheight = min(int(heightA),int(heightB))


    dst = np.array([
        [0,0],
        [maxWidth -1 , 0],
        [maxWidth-1,maxheight-1],
        [0,maxheight-1]
    ], dtype="float32")

    M =cv2.getPerspectiveTransform(points,dst)
    warrped =cv2.warpPerspective(img,M,(maxWidth,maxheight))
    
    # Resize the warped image to the fixed size
    fixed_size = (400, 600)  # Set this to your desired fixed size
    warrped_resized = cv2.resize(warrped, fixed_size)

    return warrped_resized


def PreProcessing(img):
    try:
        original_height, original_width = img.shape[:2]
        img_width, img_height = 400,600
        small_img = cv2.resize(img,(img_width, img_height))

        # Convert the image to bytes
        is_success, im_buf_arr = cv2.imencode(".jpg", small_img)
        byte_im = im_buf_arr.tobytes()

        # Remove the background
        nobg_img_bytes = remove(byte_im)

        # Convert the bytes back to a numpy array
        nobg_img = cv2.imdecode(np.frombuffer(nobg_img_bytes, np.uint8), -1)

        imggray = cv2.cvtColor(nobg_img,cv2.COLOR_BGR2GRAY)
        ret, thresholded = cv2.threshold(imggray, 20, 255, cv2.THRESH_BINARY)
        small_img_copy = small_img.copy()

        contours = cv2.findContours(thresholded,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        largest_contour = sorted(contours, key = cv2.contourArea, reverse=True)[0]

        cv2.drawContours(small_img_copy, [largest_contour],-1,(0,0,255),2)

        unOrdered_corners = GetCornerPoints(largest_contour)
        drawed_Img_Corners = DrawPointsOnImage(small_img_copy.copy(),unOrdered_corners,"unOrdered_corners")
        ordered_corners_clockwise = OrderCornerPointClockwise(unOrdered_corners)

        warrped_img = ApplyTopView(small_img,np.float32(ordered_corners_clockwise))

        height, width = warrped_img.shape[:2]
        if height > width:
            warrped_img = cv2.rotate(warrped_img, cv2.ROTATE_90_CLOCKWISE)
        
        return warrped_img
    except Exception as e:
        print(e)
        return 0










def pipline():
    # one time call pipline
    return easyocr.Reader(['ar','en'])
    
def fix180RotationDegree(text_reader,warrped_img):
    try:
        
        image180 = cv2.rotate(warrped_img, cv2.ROTATE_180)

        imageResults= text_reader.readtext(warrped_img)
        image180Results= text_reader.readtext(image180)
        
        if len(imageResults) <1 and len(image180Results) <1:
            return warrped_img

        elif len(imageResults) <1:
            return warrped_img

        elif len(image180Results) <1:
            return warrped_img
        
        prediction1 = [pred[2] for pred in imageResults ]
        prediction2 = [pred[2] for pred in image180Results ]
        
        
        words = [pred[1] for pred in imageResults ]
        words2 = [pred[1] for pred in image180Results ]
        
        xx=sum(prediction1)
        yy=sum(prediction2)
        
        
        
        avdPrediction1 =sum(prediction1)/len(imageResults)
        avdPrediction2 =sum(prediction2)/len(image180Results)
        
        """ print(words)
        print("*****************")
        print(words2) """
        
        if (avdPrediction1 >= avdPrediction2):  
            return warrped_img
        else:
            return image180
    except Exception as e:
        print(e)
        return 0


""" if __name__ == "__main__":
    
    # Use the command line argument as the image path
    imagePath = sys.argv[1]

    # Process the image and get the final result
    image = cv2.imread(imagePath)
    croppedImages = PreProcessing(image)
    textReader = pipline()
    croppedImages22 = fix180RotationDegree(textReader,croppedImages)

    plt.imshow(croppedImages22, cmap='gray', interpolation='bicubic')
    plt.title("final image")
    plt.show() """