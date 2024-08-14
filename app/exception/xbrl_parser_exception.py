class TypeOfXBRLIsDifferent(Exception):
    """XBRLの種類が異なる場合に発生するエラー"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"XBRLの種類が異なります。処理を中断します。[詳細]: {self.message}"


class TagNotFoundError(Exception):
    """タグが見つからない場合に発生するエラー"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"タグが見つかりません。処理を中断します。[詳細]: {self.message}"

class DocumentNameTagNotFoundError(Exception):
    """書類名タグが見つからない場合に発生するエラー"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"書類名タグが見つかりません。処理を中断します。[詳細]: {self.message}"
