class XbrlListEmptyError(Exception):
    """XBRLのリストが空の場合に発生するエラー"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"XBRLのリストが空です。処理を中断します。[詳細]: {self.message}"


class XbrlDirectoryNotFoundError(Exception):
    """XBRLディレクトリが見つからない場合に発生するエラー"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"XBRLディレクトリが見つかりません。処理を中断します。[詳細]: {self.message}"


class OutputPathNotFoundError(Exception):
    """出力先のパスが見つからない場合に発生するエラー"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"出力先のパスが見つかりません。処理を中断します。[詳細]: {self.message}"


class SetLanguageNotError(Exception):
    """言語の設定が不正な場合に発生するエラー"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"言語の設定が不正です。処理を中断します。[詳細]: {self.message}"
