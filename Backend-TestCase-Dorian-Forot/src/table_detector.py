from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image, ImageFile, UnidentifiedImageError
from PIL.Image import DecompressionBombError
import requests
from pdf2image import convert_from_path


def validate_image_dimensions(image):
    """Check if the image dimensions are within the required bounds"""
    width, height = image.size  

    if width < 50 or height < 50:
        raise ValueError("Image is too small. Minimum dimensions are 50x50 pixels.")
    elif width > 10000 or height > 10000:
        raise ValueError("Image is too large. Maximum dimensions are 10000x10000 pixels.")
    else:
        return True 

def is_pdf(file_path):
    """Check if the file is a PDF"""
    return file_path.lower().endswith(".pdf")
    
def convert_pdf_to_images(pdf_path):
    """Convert PDF to images (each page)"""
    try:
        images = convert_from_path(pdf_path)
        return images
    except Exception as e:
        raise ValueError(f"Cannot convert PDF to images: {e}")
    
class TableDetector:

    def __init__(self, model_name="TahaDouaji/detr-doc-table-detection", threshold=0.7):
        """Init pretrained model"""
        self.processor = DetrImageProcessor.from_pretrained(model_name)
        self.model = DetrForObjectDetection.from_pretrained(model_name)
        self.threshold = threshold

    def process_image(self, image):
        """Process image for table detection"""
        # inputs is a dictionary containing informations the model needs to process the image
        inputs = self.processor(images=image, return_tensors="pt")
        # outputs is a DetrObjectDetectionOutput containing logits (class prediction for each object detected) and pred_boxes
        outputs = self.model(**inputs)

        target_sizes = torch.tensor([image.size[::-1]])
        results = self.processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=self.threshold)[0]

        tables = []
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            tables.append({"score": round(score.item(), 3), "box": box})
        
        return tables

    def detector(self, file_path):
        """Detect tables in PDF or image files"""
        if is_pdf(file_path):
            final_table = []
            try:
                images = convert_pdf_to_images(file_path)
            except DecompressionBombError as e:
                raise ValueError(f"Image too large, too small or unsafe to open: {e}")
            except Exception as e:
                raise ValueError(f"Cannot open image: {e}")

            for image in images:
                if validate_image_dimensions(image):
                    tables = self.process_image(image)
                    final_table.extend(tables) 
            return final_table

        else:
            try:
                image = Image.open(file_path).convert("RGB")
                if not validate_image_dimensions(image):
                    return []
            except DecompressionBombError as e:
                raise ValueError(f"Image too large, too small or unsafe to open: {e}")
            except Exception as e:
                raise ValueError(f"Cannot open image: {e}")

            tables = self.process_image(image)
            return tables

