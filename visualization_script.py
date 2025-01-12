import cv2
import pandas as pd

filename = "1.png"
img = cv2.imread(filename)

xy = pd.read_csv('detloc.csv', sep=';')
xy.describe()

def z_to_color(z):
    if 20 < z < 30:
        return (0, 0, 255)  # red
    elif 10 < z < 20:
        return (255, 0, 0)  # blue
    elif 3 < z < 10:
        return (0, 255, 255)  # yellow
    elif 2 < z < 3:
        return (75, 0, 130)  # indigo
    elif 1 < z < 2:
        return (0, 255, 0)  # green
    elif 0.9 < z < 1:
        return (128, 0, 128)  # purple
    elif 0.8 < z < 0.9:
        return (50, 205, 50)  # LawnGreen
    elif 0.7 < z < 0.8:
        return (128, 128, 128)  # grey
    elif 0.6 < z < 0.7:
        return (255, 228, 196)  # Moccasin
    elif 0.5 < z < 0.6:
        return (189, 183, 107)  # DarkKhaki
    elif 0.4 < z < 0.5:
        return (255, 0, 255)  # Fuchsia
    elif 0.3 < z < 0.4:
        return (216, 191, 216)  # Thistle
    else:
        return (238, 130, 238)  # violet

for i, row in xy.iterrows():
    cv2.circle(img, (int(row['X']), int(row['Y'])), 3, z_to_color(row['Z']), -1)

cv2.imwrite("procesed.png", img)
cv2.imshow("processed.png", img)
cv2.waitKey(0)
cv2.destroyAllWindows()