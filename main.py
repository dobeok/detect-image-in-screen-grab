import numpy as np
import cv2
from mss import mss
from PIL import Image
import glob # to get all templates
import matplotlib.pyplot as plt

# template
# in reality, will need to loop through each template and search
# template_path = './heroes-portraits'
template_path = './image-downscale'

hero_list = ['sniper', 'anti']

template_files = []
for hero in hero_list:
    template_files += glob.glob(f'{template_path}/images/*{hero}*.png')

print(template_files)


template_list = [cv2.imread(template) for template in template_files]
template_list = [cv2.cvtColor(template, cv2.COLOR_BGR2GRAY) for template in template_list]

# template = cv2.imread(template_files[0])
# template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
# w, h = template.shape[::-1]

# screen area to grab
bounding_box = {
    'top': 300,
    'left': 400,
    'width': 700,
    'height': 400}

sct = mss()


# check if template is inside of the grabbed image
# img = sct.grab(bounding_box)
# img_colored = np.array(img)
# img = cv2.cvtColor(img_colored, cv2.COLOR_BGR2GRAY)

# debug - save bounding box to image
# cv2.imwrite('bounding_box.png', img)

# add info text to top left of image
font = cv2.FONT_HERSHEY_SIMPLEX
font_color = (0, 0, 255)



# # continuously grab and refresh screen
# # used to degbugging, will not need in real use
while True:
    sct_img = sct.grab(bounding_box)
    

    # sct_img_colored is the canvas that we will be drawing on
    sct_img_colored = np.array(sct_img)
    
    # template matching steps:
    # 1. convert to grayscale
    # 2. choose a method
    # 3. call matchTemplate and get the rectangle of the highest match
    sct_img_gray = cv2.cvtColor(sct_img_colored, cv2.COLOR_BGR2GRAY)
    method = cv2.TM_CCOEFF

    # loop through each template and draw
    for template in template_list:
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(sct_img_gray, template, method)

        # TODO: add threshold to filter out false positive
        # threshold = .8
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        
        # draw rectangle on sct_img_colored canvas
        cv2.rectangle(sct_img_colored,top_left, bottom_right, (255, 0, 255), 2)
        
    # add text to indicate coordinates
    # and confidence
    # cv2.putText(
    #     sct_img_colored,
    #     f'Match found at {top_left}, {bottom_right}    Min {min_val:,}    Max{max_val:,}    {res.shape}',
    #     org=(50,50),
    #     fontFace=font,
    #     color=font_color, fontScale=.50)


    # show the updated image
    # the rectangle will change depending screenshot
    cv2.imshow('screen', sct_img_colored)


    # cv2.waitKey(0): pause screen and wait infinitely for keyPress
    # cv2.waitKey(1): wait for keyPress for 1 ms and will continue to refresh the frame
    
    # debug - manual adjust screen grab position
    # if (cv2.waitKey(1) & 0xFF) == ord('d'):
    #     bounding_box['left'] = bounding_box['left'] + 50

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break