class XbrlListEmptyError(Exception):
    """ XBRLのリストが空の場合に発生するエラー"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"XBRLのリストが空です。処理を中断します。[詳細]: {self.message}"