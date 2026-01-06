import cv2
import pytesseract
import tkinter as tk
from tkinter import messagebox

pytesseract.pytesseract.tesseract_cmd = "C:/Users/saumi/OneDrive/Desktop/vehicle plat/Tesseract-OCR/tesseract.exe"


def extract_license_plate_text(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(thresh, config='--psm 7')
    cleaned_text = text.strip().replace('\n', ' ')
    return cleaned_text

def start_scanning():
    haracascade = "C:/Users/saumi/OneDrive/Desktop/vehicle plat/model/haarcascade_russian_plate_number (1).xml"
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    min_area = 560
    count = 5
    
    
    

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to capture image")
            break

        plate_cascade = cv2.CascadeClassifier(haracascade)
        img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        plates = plate_cascade.detectMultiScale(img_grey, 1.1, 4)

        for (x, y, w, h) in plates:
            area = w * h
            if area > min_area:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, "Number plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)
                img_roi = img[y:y + h, x:x + w]
                cv2.imshow("ROI", img_roi)

        cv2.imshow("Result", img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            image_path = f"plates/scanned_img_{count}.jpg"
            cv2.imwrite(image_path, img_roi)
            cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, "Plate Saved", (150, 265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)
            cv2.imshow("Results", img)
            cv2.waitKey(500)
            license_plate_text = extract_license_plate_text(image_path)
            print(f"Extracted License Plate Text: {license_plate_text}")
            messagebox.showinfo("License Plate Text", f"Extracted Text: {license_plate_text}")
            count += 1

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Create GUI
root = tk.Tk()
root.title("License Plate Scanner")
root.geometry("300x150")

label = tk.Label(root, text="Click below to start scanning", font=("Arial", 12))
label.pack(pady=20)

start_button = tk.Button(root, text="Start Scanning", command=start_scanning, font=("Arial", 12), bg="green", fg="white")
start_button.pack()

root.mainloop()