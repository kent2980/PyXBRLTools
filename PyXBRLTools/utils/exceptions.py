class MyException(Exception):
    """自作例外クラスの基底クラス
    Args:
        Exception (_type_): エラーメッセージ
    """

    def __init__(self, arg: str = "") -> None:
        self.arg = arg


class XbrlValueNoneException(MyException):
    """参照したXBRLタグが存在しない場合に発生する例外
    Args:
        MyException (_type_): 自作例外クラス
    """

    def __init__(self, arg: str = "") -> None:
        super().__init__(arg)

    def __str__(self) -> str:
        return f"XBRLタグ [{self.arg}] の値が存在しません。"


class NoneXbrlZipPathSetting(Exception):
    """ZIPファイルのパスが未設定の場合に発生する例外
    Args:
        Exception (_type_): 例外基底クラス
    """

    def __str__(self) -> str:
        return "ZIPファイルのパスを指定してください。"


class LinkListEmptyException(MyException):

    def __init__(self, arg: str = "") -> None:
        super().__init__(arg)

    def __str__(self) -> str:
        return f"リンクファイルが読み込めませんでした。\n[{self.arg}]"
