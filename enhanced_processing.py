import cv2
import numpy as np
from datetime import datetime

def apply_enhancements(image):
    # Create copies for different enhancements
    enhanced = image.copy()
    
    # 1. Sharpening using unsharp masking
    gaussian = cv2.GaussianBlur(enhanced, (0, 0), 1.0)
    enhanced = cv2.addWeighted(enhanced, 1.0, gaussian, -0.5, 0)
    
    # 2. Enhance contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization)
    if len(image.shape) == 3:  # Color image
        lab = cv2.cvtColor(enhanced, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        enhanced = cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2BGR)
    
    # 3. Slight color enhancement
    enhanced = cv2.convertScaleAbs(enhanced, alpha=1.1, beta=5)
    
    return enhanced

def crop_and_enhance_image(image_path):
    # print(f"Current Date and Time (UTC - YYYY-MM-DD HH:MM:SS formatted): {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
    # print(f"Current User's Login: MananCoder29")
    
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image from {image_path}")
        return
    cv2.imshow('Original', img)
    height, width = img.shape[:2]
    print(f"\nOriginal image size: {width}x{height}")

    # Define margins
    # top_margin = int(height * 0.40)     # 40% from top
    # bottom_margin = int(height * 0.18)   # 18% from bottom
    # left_margin = int(width * 0.20)      # 20% from left
    # right_margin = int(width * 0.45)     # 45% from right

    # Define margins with your specific values
    top_margin = int(height * 0.42)     # 47% from top
    bottom_margin = int(height * 0.1)   # 13% from bottom
    left_margin = int(width * 0.2)      # 20% from left
    right_margin = int(width * 0.45)     # 48% from right

    # Perform crop
    crop = img[top_margin:height-bottom_margin, left_margin:width-right_margin]
    height_crop, width_crop = crop.shape[:2]
    print(f"\nOriginal image size: {width_crop}x{height_crop}")

    # Apply enhancements
    enhanced = apply_enhancements(crop)
    
    # Display all versions
    
    cv2.imshow('Cropped', crop)
    # cv2.imshow('Enhanced', enhanced)
    
    # Save enhanced version
    output_path = "cropped_" + image_path.split('/')[-1]
    cv2.imwrite(output_path, crop)
    print(f"\nEnhanced image saved as: {output_path}")
    
    print("\nEnhancements applied:")
    print("1. Sharpening using unsharp masking")
    print("2. Contrast enhancement using CLAHE")
    print("3. Slight color boost")
    
    # cv2.imwrite("final_" + image_path.split('/')[-1], enhanced)
    print("Saved final version!")
    cv2.destroyAllWindows()
    # while True:
    #     key = cv2.waitKey(1) & 0xFF
    #     if key == ord('q'):
    #         break
    #     elif key == ord('s'):
    #         cv2.imwrite("final_" + image_path.split('/')[-1], enhanced)
    #         print("Saved final version!")
    #         break

if __name__ == "__main__":
    image_path = "images/received_6.jpg"
    crop_and_enhance_image(image_path)