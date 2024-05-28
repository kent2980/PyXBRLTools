import unittest
from unittest.mock import patch
from PyXBRLTools.label_manager import LabelManager
import pandas as pd

class TestLabelManager(unittest.TestCase):

    def setUp(self):
        self.extra_dir = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir"
        self.lm = LabelManager(self.extra_dir)

    def test_link_label(self):
        # Test the link_label method
        index = 0
        expected_label = "Test Label"
        with patch.object(LabelManager, 'link_label', return_value=expected_label):
            result = self.lm.link_label(index)
            self.assertEqual(result, expected_label)

    def test_link_label_itertor(self):
        # Test the link_label_itertor method
        element_names = ["element1", "element2"]
        label_index = 1
        expected_result = [("element1", "Label1"), ("element2", "Label2")]
        with patch.object(LabelManager, 'link_label_itertor', return_value=expected_result):
            result = list(self.lm.link_label_itertor(element_names, label_index))
            self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()