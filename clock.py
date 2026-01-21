import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import time
import math

M = 768
N = 1024

cx = N // 2   # tọa độ X của tâm ảnh
cy = M // 2   # tọa độ Y của tâm ảnh

img = np.zeros((M, N,3), dtype=np.uint8)


# Vẽ mặt và tâm đồng hồ
cv.circle(img, (N//2, M//2), 300, (225,0,255), -1)
cv.circle(img, (N//2, M//2), 5, (225, 255, 255), -1)

# Số La Mã 
roman = ["XII", "I", "II", "III", "IV", "V",
         "VI", "VII", "VIII", "IX", "X", "XI"]

#vẽ số la mã
for i in range(12):
    angle = i * (360 / 12)
    x = int(N//2 + 250 * np.sin(np.radians(angle)))
    y = int(M//2 - 250 * np.cos(np.radians(angle)))
    cv.putText(img, roman[i], (x-20, y+10),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
# vẽ vạch phút
for i in range(60):
    angle = math.radians(i * 6)  # 360 / 60

    r1 = 300
    r2 = 280 if i % 5 == 0 else 290

    x1 = int(cx + r1 * math.sin(angle))
    y1 = int(cy - r1 * math.cos(angle))
    x2 = int(cx + r2 * math.sin(angle))
    y2 = int(cy - r2 * math.cos(angle))

    cv.line(img, (x1, y1), (x2, y2),
            (255, 255, 255), 2 if i % 5 == 0 else 1)

# vòng lặp chạy đồng hồ
while True:
    img_copy = img.copy()

    t = time.localtime()

    hour = t.tm_hour % 12
    minute = t.tm_min
    second = t.tm_sec

# kim giây
    second_angle = second * 6
    sx = int(cx + 250 * math.sin(math.radians(second_angle)))
    sy = int(cy - 250 * math.cos(math.radians(second_angle)))
    cv.line(img_copy, (cx, cy), (sx, sy), (0, 0, 255), 2)
    
# kim phút
    minute_angle = minute * 6
    mx = int(cx + 220 * math.sin(math.radians(minute_angle)))
    my = int(cy - 220 * math.cos(math.radians(minute_angle)))
    cv.line(img_copy, (cx, cy), (mx, my), (0, 255, 0), 5)
    
# kim giờ
    hour_angle = hour * 30 + minute * 0.5
    hx = int(cx + 180 * math.sin(math.radians(hour_angle)))
    hy = int(cy - 180 * math.cos(math.radians(hour_angle)))
    cv.line(img_copy, (cx, cy), (hx, hy), (255, 0, 0), 7)

    cv.imshow("Clock", img_copy)

    if cv.waitKey(1000) == ord('q'):
        break

cv.destroyAllWindows()
