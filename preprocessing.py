import cv2
import numpy as np
import torch
import torchvision.transforms as T
from torchvision.models.segmentation import deeplabv3_mobilenet_v3_large
import cv2
import numpy as np
from PIL import Image

def draw_fixed_bbox(image_path, output_crop_path, box_size=(512, 512)):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image: {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("No object (apple) found in image.")

    largest = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest)
    cx = x + w // 2
    cy = y + h // 2

    bw, bh = box_size
    x1 = max(cx - bw // 2, 0)
    y1 = max(cy - bh // 2, 0)
    x2 = min(x1 + bw, image.shape[1])
    y2 = min(y1 + bh, image.shape[0])
    x1 = x2 - bw
    y1 = y2 - bh

    cropped = image[y1:y2, x1:x2]
    cv2.imwrite(output_crop_path, cropped)
    print(f"Cropped and saved to {output_crop_path}")



device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load segmentation model
model = deeplabv3_mobilenet_v3_large(pretrained=True).to(device)
model.eval()

# Preprocessing
transform = T.Compose([
    T.Resize((520, 520)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def segment_and_crop(image_path, output_path, box_size=(512, 512)):
    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(input_tensor)["out"][0]
    mask = output.argmax(0).cpu().numpy()

    # Assume the apple is the main foreground object — get largest connected region
    binary_mask = (mask != 0).astype(np.uint8)
    cv2.imwrite("mask.jpg",binary_mask)
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("No object found.")

    largest = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest)
    cx, cy = x + w // 2, y + h // 2

    # Resize to original image size to map coords
    orig = np.array(image)
    h_orig, w_orig = orig.shape[:2]

    scale_x = w_orig / 520
    scale_y = h_orig / 520
    cx = int(cx * scale_x)
    cy = int(cy * scale_y)

    bw, bh = box_size
    x1 = max(cx - bw // 2, 0)
    y1 = max(cy - bh // 2, 0)
    x2 = min(x1 + bw, w_orig)
    y2 = min(y1 + bh, h_orig)
    x1 = x2 - bw
    y1 = y2 - bh

    cropped = orig[y1:y2, x1:x2]
    cv2.imwrite(output_path, cropped)
    print(f"Saved cropped apple to {output_path}")

# Example usage:
segment_and_crop("received.jpg", "apple_crop.jpg", box_size=(512, 512))


# Example usage
#draw_fixed_bbox("received.jpg", "apple_crop.jpg", box_size=(512, 512))
