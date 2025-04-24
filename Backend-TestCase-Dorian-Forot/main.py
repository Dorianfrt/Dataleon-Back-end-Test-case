import sys
import os
from src.table_detector import TableDetector

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [path_to_image]")
        return

    image_path = sys.argv[1]

    if not os.path.exists(image_path):
        print(f"[ERROR] File not found: {image_path}")
        return

    try:
        print("Running Table Detection...")
        detector = TableDetector()
        results = detector.detector(image_path)  
        print(f"Tables detected in '{image_path}':")
        for i, item in enumerate(results):
            print(f"  Table {i+1}: score={item['score']:.3f}, box={item['box']}")

    except Exception as e:
        print(f"[ERROR] Prediction failed: {e}")

if __name__ == "__main__":
    main()
