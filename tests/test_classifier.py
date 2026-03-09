import pytest
from classifier import classifier

def test_classifier_single_industry():
    result = classifier("Corporate Banking and Markets Graduate Scheme")
    assert result == ["Finance"]
    
def test_classifier_multiple_industries():
    result = classifier("Intelligence and Data Analyst Development Programme (I&DADP)")
    assert result == ["Technology", "Government/Public Sector"]
    
def test_classifier_unknown():
    result = classifier("Unknown Graduate Scheme")
    assert result == "Unknown"