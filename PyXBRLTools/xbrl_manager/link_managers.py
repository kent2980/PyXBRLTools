class BaseLinkManager:
    def __init__(self, dir_path: str):

        # ディレクトリパスを設定
        self._dir_path = dir_path

    @property
    def dir_path(self) -> str:
        """dir_path属性のゲッター。"""
        return self._dir_path

    @dir_path.setter
    def dir_path(self, dir_path: str) -> None:
        """dir_path属性のセッター。

        Args:
            dir_path (str): パースするディレクトリのパス。
        """
        self._dir_path = dir_path

    def to_link_df(self):
        pass

class CalculationLinkManager:
    def __init__(self, xbrl_zip_path):
        ...

    def to_cal_link_df(self):
        ...


class DefinitionLinkManager:
    def __init__(self, xbrl_zip_path):
        ...

    def to_def_link_df(self):
        ...


class PresentationLinkManager:
    def __init__(self, xbrl_zip_path):
        ...

    def to_pre_link_df(self):
        ...
