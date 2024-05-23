import unittest
from unittest.mock import patch, mock_open
# your_moduleは関数が定義されているモジュール名に置き換えてください
from disclosure_api2.utils import extract_zip, format_date

class TestUtils(unittest.TestCase):
    """
    `TestUtils` クラスは、utilsモジュールの関数の単体テストを行います。

    このクラスでは `format_date` 関数と `extract_zip` 関数のテストケースを含んでいます。
    """

    def test_format_date_with_era(self):
        """
        和暦を含む日付文字列を正しい西暦の日付形式に変換することをテストします。
        """
        self.assertEqual(format_date('令和4年10月3日'), '2022-10-03')

    def test_format_date_with_year(self):
        """
        西暦年を含む日付文字列を正しいフォーマットに変換することをテストします。
        """
        self.assertEqual(format_date('2023年10月3日'), '2023-10-03')

    def test_format_date_with_dash(self):
        """
        ハイフンを含む日付文字列が正しいフォーマットに変換されることをテストします。
        """
        self.assertEqual(format_date('2023-10-3'), '2023-10-03')

    def test_format_date_raises_value_error(self):
        """
        無効な日付文字列が与えられた場合に `ValueError` を発生させることをテストします。
        """
        with self.assertRaises(ValueError):
            format_date('無効な日付')

    @patch('os.path.exists', return_value=True)
    @patch('zipfile.ZipFile')
    def test_extract_zip_success(self, mock_zipfile, mock_exists):
        """
        ZIPファイルが存在し、解凍に成功することをテストします。
        """
        extract_zip('dummy.zip', 'extract_to_dir')
        mock_zipfile.assert_called_with('dummy.zip', 'r')

    @patch('os.path.exists', return_value=False)
    def test_extract_zip_file_not_found(self, mock_exists):
        """
        存在しないZIPファイルを解凍しようとした時に `FileNotFoundError` を発生させることをテストします。
        """
        with self.assertRaises(FileNotFoundError):
            extract_zip('nonexistent.zip')

    @patch('os.path.exists', return_value=True)  # os.path.existsをモックし、常にTrueを返すように設定します。
    @patch('zipfile.ZipFile.extractall', side_effect=Exception('error'))  # zipfile.ZipFile.extractallをモックし、呼び出された際にExceptionを発生させます。
    def test_extract_zip_extraction_fails(self, mock_extractall, mock_exists):
        """
        ZIPファイルの解凍中にエラーが発生した場合に例外を発生させることをテストします。
        """
        with self.assertRaises(Exception) as context:  # Exceptionが発生することを期待してコードブロックを実行します。
            extract_zip('dummy.zip', 'extract_to_dir')  # テスト対象の関数を実行します。この関数はモックによって例外を投げるはずです。
            exception_message = str(context.exception)  # 発生した例外のメッセージを取得します。
            self.assertTrue('error' in exception_message)  # 取得した例外メッセージに'error'が含まれていることを確認します。


if __name__ == '__main__':
    unittest.main()
