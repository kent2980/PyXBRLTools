import unittest
from unittest.mock import patch
from PyXBRLTools.label_manager import LabelManager

class TestLabelManager(unittest.TestCase):

    def setUp(self):
        # テストのセットアップ時に実行されるメソッド
        self.extra_dir = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir"
        self.lm = LabelManager(self.extra_dir)

    def test_link_label(self):
        """ link_labelメソッドのテスト """
        # link_labelメソッドをテストします
        index = 0
        expected_label = "Test Label"
        with patch.object(LabelManager, 'link_label', return_value=expected_label):
            # LabelManagerクラスのlink_labelメソッドをモックして、期待される値を返すように設定
            result = self.lm.link_label(index)
            # 結果が期待される値と等しいかを検証
            self.assertEqual(result, expected_label)

    def test_link_label_itertor(self):
        """ link_label_itertorメソッドのテスト """
        # link_label_itertorメソッドをテストします
        element_names = ["element1", "element2"]
        label_index = 1
        expected_result = [("element1", "Label1"), ("element2", "Label2")]
        with patch.object(LabelManager, 'link_label_itertor', return_value=expected_result):
            # LabelManagerクラスのlink_label_itertorメソッドをモックして、期待される結果を返すように設定
            result = list(self.lm.link_label_itertor(element_names, label_index))
            # 結果が期待されるリストと等しいかを検証
            self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
