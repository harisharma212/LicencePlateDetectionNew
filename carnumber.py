import cv2
import os
import imutils
import pytesseract
import time

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def parse_image(file):
    try:
        file = r'{}'.format(file)
        original_image = cv2.imread(file)

        # Get Height & Width of the image
        original_image = imutils.resize(original_image, width=500)

        # Convert into GrayScalee
        gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)

        edged_image = cv2.Canny(gray_image, 30, 200)

        # Find and normalize the colors
        contours, new = cv2.findContours(
            edged_image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        img1 = original_image.copy()
        cv2.drawContours(img1, contours, -1, (0, 255, 0), 3)
        # Uncomment the below statement to display the GrayScale image
        # cv2.imshow("img1", img1)

        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]

        # stores the license plate contour
        screenCnt = None
        img2 = original_image.copy()

        # draws top 30 contours
        cv2.drawContours(img2, contours, -1, (0, 255, 0), 3)
        # Uncomment the below statement to display the resultant image
        # cv2.imshow("img2", img2)

        count = 0
        idx = 7

        for c in contours:
            # approximate the license plate contour
            contour_perimeter = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * contour_perimeter, True)

        # Look for contours with 4 corners
            if len(approx) == 4:
                screenCnt = approx

        # find the coordinates of the license plate contour
                x, y, w, h = cv2.boundingRect(c)
                new_img = original_image[y: y + h, x: x + w]

        # stores the new image
                cv2.imwrite('./'+str(idx)+'.png', new_img)
                idx += 1
                break

        # draws the license plate contour on original image
        cv2.drawContours(original_image, [screenCnt], -1, (0, 255, 0), 3)
        # Uncomment the below statement to display the resultant image
        # cv2.imshow("detected license plate", original_image)

        # filename of the cropped license plate image
        cropped_License_Plate = './7.png'
        # Uncomment the below statement to display the Cropped image

        # cv2.imshow("cropped license plate", cv2.imread(cropped_License_Plate))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # converts the license plate characters to string
        st = pytesseract.image_to_string(cropped_License_Plate, lang='eng')

        return f"License plate numbe is: {st}"
    except:
        return "Invalid Image"
    

BASE_PATH = os.path.join(os.getcwd(), 'inputs')


for file in os.listdir(BASE_PATH):
    print(file, parse_image(os.path.join(BASE_PATH, file)))
    

