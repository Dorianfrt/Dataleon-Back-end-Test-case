import os
import sys
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from table_detector import TableDetector
from PIL import Image

@pytest.fixture
def detector_instance():
    return TableDetector()

directory = "assets/dataset/unit_tests"

def test_single_table_image(detector_instance):
    """Test detection on single table image (1_table.jpeg)"""
    file_path = os.path.join(directory, "1_table.jpeg")
    results = detector_instance.detector(file_path)
    assert isinstance(results, list), f"Results for {file_path} should be a list."
    assert len(results) == 1, f"Should detect 1 table in {file_path}."

def test_two_tables_image(detector_instance):
    """Test detection on image with 2 tables (2_tables.jpeg)"""
    file_path = os.path.join(directory, "2_tables.jpeg")
    results = detector_instance.detector(file_path)
    assert isinstance(results, list), f"Results for {file_path} should be a list."
    assert len(results) == 2, f"Should detect 2 tables in {file_path}."

def test_three_tables_image(detector_instance):
    """Test detection on image with 3 tables (3_tables.png)"""
    file_path = os.path.join(directory , "3_tables.png")
    results = detector_instance.detector(file_path)
    assert isinstance(results, list), f"Results for {file_path} should be a list."
    assert len(results) == 3, f"Should detect 3 tables in {file_path}."

def test_six_tables_image(detector_instance):
    """Test detection on image with 4 tables (4_tables.png)"""
    file_path = os.path.join(directory, "6_tables.png")
    results = detector_instance.detector(file_path)
    assert isinstance(results, list), f"Results for {file_path} should be a list."
    assert len(results) == 6, f"Should detect 6 tables in {file_path}."

def test_corrupted_pdf(detector_instance):
    """Test detection on corrupted PDF file (corrupt_file.pdf)"""
    file_path = os.path.join(directory, "corrupt_file.pdf")
    with pytest.raises(ValueError, match="Cannot open image"):
        detector_instance.detector(file_path)

def test_valid_pdf(detector_instance):
    """Test detection on a valid PDF file (IC-Basic-Invoice-Template-10768_PDF.pdf)"""
    file_path = os.path.join(directory, "classic_doc.pdf")
    results = detector_instance.detector(file_path)
    assert isinstance(results, list), f"Results for {file_path} should be a list."
    assert len(results) > 0, f"Should detect at least one table in {file_path}."

def test_non_image_file(detector_instance):
    """Test detection on a non-image file (not_an_image.txt)"""
    file_path = os.path.join(directory, "not_an_image.txt")
    with pytest.raises(ValueError, match="Cannot open image"):
        detector_instance.detector(file_path)

def test_detector_with_small_image_raises_error(detector_instance):
    file_path = os.path.join(directory, "image_20x20.png")
    with pytest.raises(ValueError, match="Image"):
        detector_instance.detector(file_path)

def test_empty_image_no_tables(detector_instance):
    """Test detection on an empty white image (empty_image.png)"""
    file_path = os.path.join(directory, "empty_image.png")
    results = detector_instance.detector(file_path)
    assert isinstance(results, list), f"Results for {file_path} should be a list."
    assert len(results) == 0, f"No tables should be detected in a blank image {file_path}."

def test_random_noise_image(detector_instance):
    """Test detection on a random noisy image (noise_image.png)"""
    file_path = os.path.join(directory, "noise_image.png")
    results = detector_instance.detector(file_path)
    assert isinstance(results, list), f"Results for {file_path} should be a list."
    assert len(results) == 0, f"No tables should be detected in random noise {file_path}."

def test_very_large_image(detector_instance):
    """Test detection on a very large image (large_image.png)"""
    file_path = os.path.join(directory, "large_image.png")
    with pytest.raises(ValueError, match="Image"): 
        detector_instance.detector(file_path)

def test_unsupported_file_format(detector_instance):
    """Test detection on unsupported file format (1.c)"""
    file_path = os.path.join(directory, "1.c")
    with pytest.raises(ValueError, match="Cannot open image"):
        detector_instance.detector(file_path)

def test_detector_with_none_input(detector_instance):
    """Test detection when input is None"""
    with pytest.raises(Exception):
        detector_instance.detector(None)

def test_detector_with_nonexistent_file(detector_instance):
    """Test detection with a path that does not exist"""
    file_path = os.path.join(directory, "this_file_does_not_exist.png")
    with pytest.raises(ValueError, match="Cannot open image"):
        detector_instance.detector(file_path)

def test_valid_box_coordinates(detector_instance):
    """Test that the bounding box coordinates are within valid image dimensions."""
    file_path = os.path.join(directory, "bound_image.jpeg")
    
    with Image.open(file_path) as img:
        width, height = img.size
        
    results = detector_instance.detector(file_path)
        
    for item in results:
        assert "box" in item, f"Each result for {file_path} should have a 'box'."
        box = item["box"]
        score = item["score"]
            
        assert 0 <= score <= 1, f"Invalid score: {score} for {file_path}"
        assert isinstance(box, (list, tuple)) and len(box) == 4, f"Box should be a list/tuple of 4 coordinates."
            
        x1, y1, x2, y2 = box
        assert 0 <= x1 <= width, f"x1 = {x1} is out of bounds for {file_path}."
        assert 0 <= y1 <= height, f"y1 = {y1} is out of bounds for {file_path}."
        assert 0 <= x2 <= width, f"x2 = {x2} is out of bounds for {file_path}."
        assert 0 <= y2 <= height, f"y2 = {y2} is out of bounds for {file_path}."
            
        assert x1 < x2, f"x1 = {x1} is greater than or equal to x2 = {x2} for {file_path}."
        assert y1 < y2, f"y1 = {y1} is greater than or equal to y2 = {y2} for {file_path}."
        
        assert 100 < x1 < 110, f"wrong x1 = {x1} for {file_path}."
        assert 700 < y1 < 710, f"wrong y1 = {y1} for {file_path}."
        assert 600 < x2 < 610, f"wrong x2 = {x2} for {file_path}."
        assert 780 < y2 < 790, f"wrong y2 = {y2} for {file_path}."