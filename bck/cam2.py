import cv2
img= cv2.VideoCapture(0)
# Check success
if not img.isOpened():
    raise Exception("Could not open video device")
# Read picture. ret === True on success
ret, frame = img.read()
isWritten = cv2.imwrite('D:/image-2.png', img)

if isWritten:
	print('Image is successfully saved as file.')
# Close device
img.release()