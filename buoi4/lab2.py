import cv2 as cv
import numpy as np

cap = cv.VideoCapture("bang_chuyen.mp4") #thay tên file = kênh camera 0, ip,...
count = 0 # biến đếm
vat_the = []   # danh sách vật thể
next_id = 0
line_x = 600
DIST_THRESHOLD = 50

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY) #chuyển từ màu sang đen trắng 
    gray = cv.medianBlur(gray, 5) #làm sạch nhiễu

    circles = cv.HoughCircles(
        gray,
        cv.HOUGH_GRADIENT,
        dp =1,
        minDist = 20,
        param1= 50,
        param2= 30,
        minRadius= 5,
        maxRadius= 50
    )

    if circles is not None:
        circles = np.round(circles).astype(int)

        for circle in circles[0, :]:
            x, y, r = circle
            cv.circle(frame, (x, y), r, (0, 0, 255), 2)
            cv.circle(frame, (x-1, y-1), r-1, (0, 0, 255), 2)

            matched = False

            # so khớp với vật thể cũ
            for obj in vat_the:
                if abs(obj["x"] - x) < DIST_THRESHOLD:
                    obj["x"] = x
                    matched = True

                    # ĐẾM ĐÚNG 1 LẦN
                    if not obj["counted"] and x > line_x:
                        count += 1
                        obj["counted"] = True
                        print(f"Vat the thu {count} da di qua")

                    break

            # nếu là vật thể mới
            if not matched:
                vat_the.append({
                    "id": next_id,
                    "x": x,
                    "counted": x > line_x
                })
                next_id += 1

    cv.imshow("f", frame)
    if cv.waitKey(10) == ord('q'):
        break
cv.destroyAllWindows()