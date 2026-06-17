import cv2
import numpy as np

# Load image
image = cv2.imread('gear.jpg')
if image is None:
    print("Error: Image not found!")
    exit()

print("Image loaded successfully!")

# Step 1: Convert to Grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
print("Step 1: Grayscale conversion - Done")

# Step 2: Apply Gaussian Blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
print("Step 2: Gaussian Blur - Done")

# Step 3: Apply Threshold
_, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
print("Step 3: Thresholding - Done")

# Step 4: Find Contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(f"Step 4: Found {len(contours)} contours")

# Step 5: Select largest contour
if len(contours) == 0:
    print("RESULT: FAIL - No part detected!")
    exit()

main_contour = max(contours, key=cv2.contourArea)

# Step 6: Compute Convex Hull
hull = cv2.convexHull(main_contour, returnPoints=False)
print("Step 6: Convex Hull computed")

# Step 7: Find Convexity Defects
defects = cv2.convexityDefects(main_contour, hull)

# Step 8: Count significant defects
THRESHOLD = 15.0
defect_count = 0
result_image = image.copy()

if defects is not None:
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        depth = d / 256.0
        if depth > THRESHOLD:
            defect_count += 1
            far = tuple(main_contour[f][0])
            cv2.circle(result_image, far, 10, (0, 0, 255), -1)

print(f"Step 8: Detected {defect_count} defects")

# Step 9: PASS/FAIL Decision
if defect_count > 0:
    status = "FAIL"
    color = (0, 0, 255)
    print("FINAL RESULT: FAIL - Defect detected!")
else:
    status = "PASS"
    color = (0, 255, 0)
    print("FINAL RESULT: PASS - Part is OK!")

# Step 10: Save result image
cv2.putText(result_image, status, (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 2, color, 3)
cv2.drawContours(result_image, [main_contour], -1, (255, 0, 0), 2)
cv2.imwrite('result.jpg', result_image)
print("Result image saved as: result.jpg")
