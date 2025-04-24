from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image
import requests

class TableDetector:

    # only keep detections with score > 0.9
    def __init__(self, model_name="TahaDouaji/detr-doc-table-detection", threshold=0.5):
        """  Init pretrained model """
    
        self.processor = DetrImageProcessor.from_pretrained(model_name)
        self.model = DetrForObjectDetection.from_pretrained(model_name)
        self.threshold = threshold
    
    def detector(self, image_path):
        """ Return a list of dictionaries containing score and box """
        try:
            image = Image.open(image_path).convert("RGB")
            image = image.resize((800, 800))
        except Exception as e:
            raise ValueError(f"Cannot open image: {e}")
        # inputs is a dictionary containing informations the model needs to process the image
        inputs = self.processor.__call__(images=image, return_tensors="pt")
        # outputs is a DetrObjectDetectionOutput containing logits (class prediction for each object detected) and pred_boxes
        outputs = self.model.__call__(**inputs)

        target_sizes = torch.tensor([image.size[::-1]])
        results = self.processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=self.threshold)[0]

        tables = []
        for score, box in zip(results["scores"], results["boxes"]):
            tables.append({"score": score.item(), "box": box.tolist()})
        
        return tables
