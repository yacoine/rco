import numpy as np
import cv2
import skimage.exposure
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import k_means



def load_image(path:str,display:bool):
    
    
    if display:
        img=cv2.imread(path)#read file
        cv2.imshow("Image", img) #display image

        cv2.waitKey(0);cv2.destroyAllWindows(); cv2.waitKey(1)#closes window w/ keystroke
        
        return img
    else:
        img=cv2.imread(path)
        
        return img
    

def mask_image(path:str,lower,upper, display:bool):
    
    img=load_image(path,display=0)
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # lower bound and upper bound for Green color
    
    lower_bound = lower 
    upper_bound = upper

    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
    if display:
        cv2.imshow("Masked image", mask) #display image

        cv2.waitKey(0);cv2.destroyAllWindows(); cv2.waitKey(1)
        
    return mask

def bgremove1(myimage):
 
    # Blur to image to reduce noise
    myimage = cv2.GaussianBlur(myimage,(5,5), 0)
 
    # We bin the pixels. Result will be a value 1..5
    bins=np.array([0,51,102,153,204,255])
    myimage[:,:,:] = np.digitize(myimage[:,:,:],bins,right=True)*51
 
    # Create single channel greyscale for thresholding
    myimage_grey = cv2.cvtColor(myimage, cv2.COLOR_BGR2GRAY)
 
    # Perform Otsu thresholding and extract the background.
    # We use Binary Threshold as we want to create an all white background
    ret,background = cv2.threshold(myimage_grey,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
 
    # Convert black and white back into 3 channel greyscale
    background = cv2.cvtColor(background, cv2.COLOR_GRAY2BGR)
 
    # Perform Otsu thresholding and extract the foreground.
    # We use TOZERO_INV as we want to keep some details of the foregorund
    ret,foreground = cv2.threshold(myimage_grey,0,255,cv2.THRESH_TOZERO_INV+cv2.THRESH_OTSU)  #Currently foreground is only a mask
    foreground = cv2.bitwise_and(myimage,myimage, mask=foreground)  # Update foreground with bitwise_and to extract real foreground
 
    # Combine the background and foreground to obtain our final image
    finalimage = background+foreground
 
    return finalimage

def bgremove2(myimage):
    # First Convert to Grayscale
    myimage_grey = cv2.cvtColor(myimage, cv2.COLOR_BGR2GRAY)
 
    ret,baseline = cv2.threshold(myimage_grey,127,255,cv2.THRESH_TRUNC)
 
    ret,background = cv2.threshold(baseline,126,255,cv2.THRESH_BINARY)
 
    ret,foreground = cv2.threshold(baseline,126,255,cv2.THRESH_BINARY_INV)
 
    foreground = cv2.bitwise_and(myimage,myimage, mask=foreground)  # Update foreground with bitwise_and to extract real foreground
 
    # Convert black and white back into 3 channel greyscale
    background = cv2.cvtColor(background, cv2.COLOR_GRAY2BGR)
 
    # Combine the background and foreground to obtain our final image
    finalimage = background+foreground
    return finalimage

#best background remover, by default choose bg remove 3
def bgremove3(myimage):
    # BG Remover 3
    myimage_hsv = cv2.cvtColor(myimage, cv2.COLOR_BGR2HSV)
     
    #Take S and remove any value that is less than half
    s = myimage_hsv[:,:,1]
    s = np.where(s < 127, 0, 1) # Any value below 127 will be excluded
 
    # We increase the brightness of the image and then mod by 255
    v = (myimage_hsv[:,:,2] + 127) % 255
    v = np.where(v > 127, 1, 0)  # Any value above 127 will be part of our mask
 
    # Combine our two masks based on S and V into a single "Foreground"
    foreground = np.where(s+v > 0, 1, 0).astype(np.uint8)  #Casting back into 8bit integer
 
    background = np.where(foreground==0,255,0).astype(np.uint8) # Invert foreground to get background in uint8
    background = cv2.cvtColor(background, cv2.COLOR_GRAY2BGR)  # Convert background back into BGR space
    foreground=cv2.bitwise_and(myimage,myimage,mask=foreground) # Apply our foreground map to original image
    finalimage = background+foreground # Combine foreground and background
 
    return finalimage

def moment_display(img):
    
    cv2.imshow("Image", img) #display image

    cv2.waitKey(0);cv2.destroyAllWindows(); cv2.waitKey(1)
    
    return 0

def empty(a):
    pass

def assisted_masking(path, lower=np.array([100, 20, 20]), upper=np.array([130, 255, 255]) ):

    fn=path #path
    img=cv2.imread(fn) #reading image
    #cv2.startWindowThread() #this seems to help the closing of window issue


    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #changes color from bgr to hsv
    cv2.namedWindow('image')  


        
    hmin= lower[0]
    hmax= upper[0]

    smin= lower[1]
    smax= upper[1]

    vmin= lower[2]
    vmax= upper[2]
        
    #creating min-max trackbar for hue, saturation, and value
    cv2.createTrackbar('Hue Min','image',hmin,179,empty)
    cv2.createTrackbar('Hue Max','image',hmax,179,empty)
    cv2.createTrackbar('Saturation Min','image',smin,255,empty)
    cv2.createTrackbar('Saturation Max','image',smax,255,empty)
    cv2.createTrackbar('Val Min','image',vmin,255,empty)
    cv2.createTrackbar('Val Max','image',vmax,255,empty)

    #while loop is true until if statement is true, then breaks out of while loop 
    while(True):

        # for button pressing and changing
        k = cv2.waitKey(1) & 0xFF
        #once "ESC" button is pressed, loop breaks (true for linux)
        if k == 27:

            break
        #retrieving the min max values based on track bar position 
        hue_min= cv2.getTrackbarPos('Hue Min', 'image')
        hue_max = cv2.getTrackbarPos('Hue Max', 'image')
        sat_min = cv2.getTrackbarPos('Saturation Min', 'image')
        sat_max = cv2.getTrackbarPos('Saturation Max', 'image')
        val_min = cv2.getTrackbarPos('Val Min', 'image')
        val_max = cv2.getTrackbarPos('Val Max', 'image')
        
        #lower and upper values based on trackbar positions
        lower = np.array([hue_min,sat_min,val_min])
        upper = np.array([hue_max,sat_max,val_max])
        
        #mask range
        mask = cv2.inRange(hsv,lower,upper)

        #######START
        """
        mask = 255 - mask

        # apply morphology opening to mask
        kernel = np.ones((3,3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_ERODE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # antialias mask
        mask = cv2.GaussianBlur(mask, (0,0), sigmaX=3, sigmaY=3, borderType = cv2.BORDER_DEFAULT)
        mask = skimage.exposure.rescale_intensity(mask, in_range=(127.5,255), out_range=(0,255))

        # put white where ever the mask is zero
        
        img[mask==0] = (255,255,255)



        #####END
        """
        #resulting image, showing colors and masked colors in black
        res=cv2.bitwise_and(img,img,mask=mask)
        
        
        cv2.imshow('image',res)

    #closes the window

    cv2.destroyAllWindows();cv2.waitKey(1);
    
    return res


def color_schema(color_name):

    red=[np.array([0, 20, 20]), np.array([10, 255, 255])]
    red_orange=[np.array([10, 20, 20]), np.array([15, 255, 255])]
    orange=[np.array([16, 20, 20]), np.array([23, 255, 255])]
    yellow_orange=[np.array([23, 20, 20]), np.array([27, 255, 255])]
    yellow=[np.array([27, 20, 20]), np.array([56, 255, 255])]
    yellow_green=[np.array([32, 20, 20]), np.array([56, 255, 255])]
    green=[np.array([56, 20, 20]), np.array([86, 255, 255])]
    blue_green=[np.array([86, 20, 20]), np.array([98, 255, 255])]
    blue=[np.array([98, 80, 20]), np.array([122, 255, 255])]
    blue_violet=[np.array([122, 20, 20]), np.array([136, 255, 255])]
    violet=[np.array([136, 20, 20]), np.array([148, 255, 255])]
    red_violet=[np.array([148, 20, 20]), np.array([177, 255, 255])]


    color_list={'red':red, 'red_orange':red_orange, 'orange':orange, 'yellow_orange':yellow_orange,
               'yellow':yellow,'yellow_green':yellow_green,'green':green,'blue_green':blue_green,
               'blue':blue,'blue_violet':blue_violet, 'violet':violet,'red_violet':red_violet}


    return color_list[color_name]

#Traces objects and returns the coordinates of objects with their coordinates 
#and arrow tip superposed on image

def trace_pathx(path ,value):
    
    img=cv2.imread(path) #read file

    imgray = cv2.cvtColor(value, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    v=cv2.drawContours(img, contours, -1, (0,255,0), 3)

    font = cv2.FONT_HERSHEY_COMPLEX

    n_list=[]
    m_list=[]

    # Going through every contours found in the image.
    for cnt in contours :

        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)

        # draws boundary of contours.
        cv2.drawContours(img, [approx], 0, (0, 0, 255), 5) 

        # Used to flatten the array containing
        # the coordinates of the vertices.
        n = approx.ravel() 
        #print(list(n))

        n_list+=list(n)

        i = 0


        for j in n :
            if(i % 2 == 0):
                x = n[i]
                y = n[i + 1]

                

                # String containing the coordinates.
                string = str(x) + " " + str(y) 

                if(i == 0):
                    # text on topmost coordinate.
                    cv2.putText(img, "Arrow tip", (x, y),
                                    font, 0.5, (255, 0, 0))
                    m_list+=list(n)
                else:
                    # text on remaining coordinates.
                    cv2.putText(img, string, (x, y), 
                              font, 0.5, (0, 255, 0)) 
                    
            i += 1

    moment_display(img)
    coordinates= m_list

    #print(m_list)
    #print(n_list)
            
    return img,coordinates

#Plotting coordinates from the opencv contouring numpy list array 
#plots on a x-y axis, which will allow for the next stage of graphing
#recreating human body, hand-feet movement on a wall based on the coordinates
##Takes input coordinates from one list and returns out plot

def simple_plot(coordinates):
    
    x=coordinates[::2] 
    y=coordinates[1::2] 
    
    plt.rcParams["figure.figsize"] = [7.5, 3.50]
    plt.rcParams["figure.autolayout"] = True



    plt.plot(x, y, 'r*')
    plt.axis([min(x)-200 ,max(x)+400 , min(y)-10,max(y)+10 ])

    for i, j in zip(x, y):
       plt.text(i, j+0.5, '({}, {})'.format(i, j))

    plt.show()

def find_centroids(coordinates):
    x=coordinates[::2] 
    y=coordinates[1::2] 

    data={'x':x, 'y':y}
    df=pd.DataFrame(data)
    centroids= k_means(df,n_clusters=23)[0] #round to 2 decimals from k means 
    centroids = np.around(centroids,2)
    #this might have to be manually supported 
    #k-means uses euclidean distance, is this the best for geospatial clustering?
    #look into below code later:
    #df = pd.read_csv('gps.csv')
    #coords = df.as_matrix(columns=['lat', 'lon'])
    #db = DBSCAN(eps=eps, min_samples=ms, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
    
    #returned in one array, easily digestable for simple_plot()
    centroids_coordinates=[item for sublist  in centroids.tolist() for item in sublist]
    
    return centroids_coordinates


