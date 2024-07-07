class NotXbrlDirectoryException(Exception):
    """XBRLディレクトリが見つからない場合に発生するエラー"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"無効なXBRLファイルです。{self.message}"


class NotXbrlTypeException(Exception):
    """XBRLファイルの種類が不正な場合に発生するエラー"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"
