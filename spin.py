import json
import cv2
import numpy as np

points_file = open("points.txt", "r")

paths = []

lines = points_file.readlines()
points_file.close()

x = 0
y = 0

zoom_after = 125

step = 1

w = 380
h = 320

grow = True

start = False

iteration = 0

while (True):
    for i in xrange(0, len(lines), 2):
        iteration += 1

        if (iteration > zoom_after):
            start = True

        dest_points = [[x, y],[w + x, y],[w + x, h + y],[x,h + y]]
        dst = np.array(dest_points, dtype = "float32")

        points = json.loads(lines[i + 1])

        image = cv2.imread('images/' + lines[i].strip())

        src = np.array(points, dtype = "float32")
        
        M = cv2.findHomography(src, dst)

        warp = cv2.warpPerspective(image, M[0], (w + 2 * x, h + 2 * y))
        
        fixed = cv2.resize(warp, (w * 2, h * 2)) 

        cv2.imshow('fixed_size', fixed)
        cv2.waitKey(1)

        if (start and grow):
            x += step
            y += step
        elif (start):
            x -= step
            y -= step

        if (x > 500):
            grow = False
        elif (x <= 0):
            x = 0
            y = 0
        
        name = str(iteration).zfill(5)

        cv2.imwrite('saved/' + name + '.png', fixed)