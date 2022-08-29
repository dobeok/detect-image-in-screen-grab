import cv2

img = cv2.imread('sharp.png', cv2.IMREAD_UNCHANGED)

print('original dims', img.shape)

# orig = 144 x 256
# desired = 82 x 144

width = 144
height = 82

resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

cv2.imwrite('resized.png', resized)