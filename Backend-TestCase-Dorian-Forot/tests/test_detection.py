import os
import sys
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from table_detector import TableDetector
from PIL import Image
from pdf2image import convert_from_path

@pytest.fixture
def detector_instance():
    return TableDetector()

@pytest.fixture
def high_threshold_detector():
    return TableDetector(threshold=0.9)

def get_files_in_directory(directory, extensions=(".png", ".jpeg", ".pdf")):
    if not os.path.exists(directory):
        pytest.skip(f"Test skipped: Directory '{directory}' not found.")
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.lower().endswith(extensions):
                files.append(os.path.join(root, filename))
    return files

def test_valid_invoice_images(detector_instance):
    """Test detection on all valid invoice images in the 'invoices' folder."""
    directory = "assets/dataset/invoices_good"
    files = get_files_in_directory(directory)
    if not files:
        pytest.skip(f"Test skipped: No valid files found in '{directory}'.")
    for image_path in files:
        results = detector_instance.detector(image_path)
        assert isinstance(results, list), f"Results for {image_path} should be a list."
        if image_path.lower().endswith('.pdf'):
            try:
                images = convert_from_path(image_path)
                return images
            except Exception as e:
                raise ValueError(f"Cannot convert PDF to images: {e}")

        with Image.open(image_path) as img:
            width, height = img.size
        for item in results:
            assert "score" in item, f"Each result for {image_path} should have a 'score'."
            assert "box" in item, f"Each result for {image_path} should have a 'box'."
            assert 0 <= item["score"] <= 1, f"Score for {image_path} should be between 0 and 1."
            box = item["box"]
            assert isinstance(box, (list, tuple)) and len(box) == 4, f"Box must be a list or tuple of 4 numbers in {image_path}."
            x1, y1, x2, y2 = box
            
            assert 0 <= x1 <= width, f"x1 = {x1} is out of bounds for {image_path}."
            assert 0 <= y1 <= height, f"y1 = {y1} is out of bounds for {image_path}."
            assert 0 <= x2 <= width, f"x2 = {x2} is out of bounds for {image_path}."
            assert 0 <= y2 <= height, f"y2 = {y2} is out of bounds for {image_path}."
            
            assert x1 < x2, f"x1 = {x1} is greater than or equal to x2 = {x2} for {image_path}."
            assert y1 < y2, f"y1 = {y1} is greater than or equal to y2 = {y2} for {image_path}."


def test_valid_bank_document_images(detector_instance):
    """Test detection on all valid bank document images in the 'bank_documents' folder."""
    directory = "assets/dataset/bank_documents_good"
    files = get_files_in_directory(directory)
    if not files:
        pytest.skip(f"Test skipped: No valid files found in '{directory}'.")
    for image_path in files:
        results = detector_instance.detector(image_path)
        assert isinstance(results, list), f"Results for {image_path} should be a list."
        if image_path.lower().endswith('.pdf'):
            try:
                images = convert_from_path(image_path)
                return images
            except Exception as e:
                raise ValueError(f"Cannot convert PDF to images: {e}")
        with Image.open(image_path) as img:
            width, height = img.size
        for item in results:
            assert "score" in item, f"Each result for {image_path} should have a 'score'."
            assert "box" in item, f"Each result for {image_path} should have a 'box'."
            assert 0 <= item["score"] <= 1, f"Score for {image_path} should be between 0 and 1."
            box = item["box"]
            assert isinstance(box, (list, tuple)) and len(box) == 4, f"Box must be a list or tuple of 4 numbers in {image_path}."
            x1, y1, x2, y2 = box
            
            assert 0 <= x1 <= width, f"x1 = {x1} is out of bounds for {image_path}."
            assert 0 <= y1 <= height, f"y1 = {y1} is out of bounds for {image_path}."
            assert 0 <= x2 <= width, f"x2 = {x2} is out of bounds for {image_path}."
            assert 0 <= y2 <= height, f"y2 = {y2} is out of bounds for {image_path}."
            
            assert x1 < x2, f"x1 = {x1} is greater than or equal to x2 = {x2} for {image_path}."
            assert y1 < y2, f"y1 = {y1} is greater than or equal to y2 = {y2} for {image_path}."


def test_invalid_images(detector_instance):
    """Test detection with invalid image paths."""
    directory = "assets/dataset/invalid_files"
    files = get_files_in_directory(directory, extensions=(".txt", ".odt", ".docx", ".epub", ".rtf", ".md"))
    if not files:
        pytest.skip(f"Test skipped: No invalid files found in '{directory}'.")
    for invalid_path in files:
        with pytest.raises(ValueError, match="Cannot open image"):
            detector_instance.detector(invalid_path)

def test_empty_images(detector_instance):
    """Test detection with empty images."""
    directory = "assets/dataset/empty_images"
    files = get_files_in_directory(directory)
    if not files:
        pytest.skip(f"Test skipped: No empty images found in '{directory}'.")
    for image_path in files:
        results = detector_instance.detector(image_path)
        assert results == [], f"Results for {image_path} should be an empty list."

def test_threshold_images(high_threshold_detector):
    """Test detection with a higher threshold on all images in the 'threshold_test' folder."""
    directory = "assets/dataset/threshold_test"
    files = get_files_in_directory(directory)
    if not files:
        pytest.skip(f"Test skipped: No files found in '{directory}'.")
    for image_path in files:
        results = high_threshold_detector.detector(image_path)
        assert isinstance(results, list), f"Results for {image_path} should be a list."
        for item in results:
            assert item["score"] >= 0.9, f"Scores for {image_path} should respect the higher threshold."

def test_wrong_dimensions_images(detector_instance):
    """Test detection on all large images in the 'large_images' folder."""
    directory = "assets/dataset/wrong_dimensions_images"
    files = get_files_in_directory(directory)
    if not files:
        pytest.skip(f"Test skipped: No large images found in '{directory}'.")
    for large_image_path in files:
        with pytest.raises(ValueError, match="Image"): 
            detector_instance.detector(large_image_path)

def test_corrupted_images(detector_instance):
    """Test detection on all corrupted images in the 'corrupted_images' folder."""
    directory = "assets/dataset/corrupted_images"
    files = get_files_in_directory(directory)
    if not files:
        pytest.skip(f"Test skipped: No corrupted images found in '{directory}'.")
    for corrupted_image_path in files:
        with pytest.raises(ValueError, match="Cannot open image"):
            detector_instance.detector(corrupted_image_path)