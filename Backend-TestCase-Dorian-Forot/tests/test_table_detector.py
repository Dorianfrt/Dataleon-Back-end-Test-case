import os
import pytest
from src.table_detector import TableDetector
from PIL import Image

detector = TableDetector()

def get_files_in_directory(directory, extensions=(".png", ".jpeg", ".pdf")):
    if not os.path.exists(directory):
        pytest.skip(f"Test skipped: Directory '{directory}' not found.")
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.lower().endswith(extensions):
                files.append(os.path.join(root, filename))
    return files

def test_valid_invoice_images():
    """Test detection on all valid invoice images in the 'invoices' folder."""
    directory = "assets/invoices_good"
    files = get_files_in_directory(directory)
    if not files:
        pytest.skip(f"Test skipped: No valid files found in '{directory}'.")
    for image_path in files:
        results = detector.detector(image_path)
        assert isinstance(results, list), f"Results for {image_path} should be a list."
        for item in results:
            assert "score" in item, f"Each result for {image_path} should have a 'score'."
            assert "box" in item, f"Each result for {image_path} should have a 'box'."
            assert 0 <= item["score"] <= 1, f"Score for {image_path} should be between 0 and 1."

def test_valid_bank_document_images():
    """Test detection on all valid bank document images in the 'bank_documents' folder."""
    directory = "assets/bank_documents_good"
    files = get_files_in_directory(directory)
    if not files:
        pytest.skip(f"Test skipped: No valid files found in '{directory}'.")
    for image_path in files:
        results = detector.detector(image_path)
        assert isinstance(results, list), f"Results for {image_path} should be a list."
        for item in results:
            assert "score" in item, f"Each result for {image_path} should have a 'score'."
            assert "box" in item, f"Each result for {image_path} should have a 'box'."
            assert 0 <= item["score"] <= 1, f"Score for {image_path} should be between 0 and 1."

def test_invalid_image_paths():
    """Test detection with invalid image paths."""
    directory = "assets/invalid_files"
    files = get_files_in_directory(directory, extensions=(".txt", ".docx"))
    if not files:
        pytest.skip(f"Test skipped: No invalid files found in '{directory}'.")
    for invalid_path in files:
        with pytest.raises(ValueError, match="Cannot open image"):
            detector.detector(invalid_path)

def test_empty_images():
    """Test detection with empty images."""
    directory = "assets/empty_images"
    files = get_files_in_directory(directory)
    if not files:
        pytest.skip(f"Test skipped: No empty images found in '{directory}'.")
    for empty_image_path in files:
        results = detector.detector(empty_image_path)
        assert results == [], f"Results for {empty_image_path} should be an empty list."

def test_threshold_effect_on_images():
    """Test detection with a higher threshold on all images in the 'threshold_test' folder."""
    directory = "assets/threshold_test"
    files = get_files_in_directory(directory)
    if not files:
        pytest.skip(f"Test skipped: No files found in '{directory}'.")
    high_threshold_detector = TableDetector(threshold=0.9)
    for image_path in files:
        results = high_threshold_detector.detector(image_path)
        assert isinstance(results, list), f"Results for {image_path} should be a list."
        for item in results:
            assert item["score"] >= 0.9, f"Scores for {image_path} should respect the higher threshold."

def test_large_images():
    """Test detection on all large images in the 'large_images' folder."""
    directory = "assets/large_images"
    files = get_files_in_directory(directory)
    if not files:
        pytest.skip(f"Test skipped: No large images found in '{directory}'.")
    for large_image_path in files:
        results = detector.detector(large_image_path)
        assert isinstance(results, list), f"Results for {large_image_path} should be a list."
        for item in results:
            assert "score" in item, f"Each result for {large_image_path} should have a 'score'."
            assert "box" in item, f"Each result for {large_image_path} should have a 'box'."

def test_corrupted_images():
    """Test detection on all corrupted images in the 'corrupted_images' folder."""
    directory = "assets/corrupted_images"
    files = get_files_in_directory(directory)
    if not files:
        pytest.skip(f"Test skipped: No corrupted images found in '{directory}'.")
    for corrupted_image_path in files:
        with pytest.raises(ValueError, match="Cannot open image"):
            detector.detector(corrupted_image_path)