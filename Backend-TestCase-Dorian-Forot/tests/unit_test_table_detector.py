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

def test_multiple_tables_image(detector_instance):
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
