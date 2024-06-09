from xbrl_parser.ixbrl_parser import IxbrlParser
from xbrl_manager.xbrl_path_manager import XbrlPathManager
import os
from abc import abstractmethod
from pandas import DataFrame
import pandas as pd

class IxbrlType:
    """ iXBRLの種類を表すクラスです。 """
    # キャッシュフロー計算書
    CASHFLOW_STATEMENT = 'cf'
    # 貸借対照表
    BALANCE_SHEET = 'bs'
    # 損益計算書
    INCOME_STATEMENT = 'pl'
    # 財務状態計算書
    STATEMENT_OF_FINANCIAL_POSITION = 'fs'
    # 包括利益計算書
    STATEMENT_OF_COMPREHENSIVE_INCOME = 'ci'
    # 株主資本変動計算書,持訳変動計算書
    STATEMENT_OF_CHANGES_IN_EQUITY = 'ss'
    # 中間連結損益及び包括利益計算書
    STATEMENT_OF_INCOME_AND_COMPREHENSIVE_INCOME = 'pc'

class BaseIxbrlManager(XbrlPathManager):

    def __init__(self, xbrl_directory_path:str) -> None:
        super().__init__(xbrl_directory_path)
        # xbrl_directory_pathが有効かどうかを確認
        if not os.path.exists(xbrl_directory_path):
            raise ValueError('指定されたパスが存在しません。')

        # xbrl_directory_pathを設定
        self.__xbrl_directory_path = xbrl_directory_path

        # iXBRLファイルのパスを取得
        self.__ixbrl_files_path = self.ixbrl_path

        # ixbrlパーサーのインスタンスを作成
        self.__parser = IxbrlParser()

        # DataFrameの初期化
        self.__ix_non_fractions = None
        self.__ix_non_numerics = None
        self.__xbrli_contexts = None

    @property
    def xbrl_directory_path(self):
        return self.__xbrl_directory_path

    @xbrl_directory_path.setter
    def xbrl_directory_path(self, value):
        self.__xbrl_directory_path = value

    @property
    def ixbrl_files_path(self):
        return self.__ixbrl_files_path

    @property
    @abstractmethod
    def ix_non_fractions(self):
        pass

    @property
    @abstractmethod
    def ix_non_numerics(self):
        pass

    @property
    @abstractmethod
    def xbrli_contexts(self):
        pass

    @abstractmethod
    def _get_ixbrl_file_paths(self):
        pass

class IxbrlManager(BaseIxbrlManager):

    def _get_ixbrl_file_paths(self):
        """ iXBRLファイルのパスを取得するメソッドです。

        Returns:
            iXBRLファイルのパスと種類を返します。

        Examples:
            >>> for ixbrl_file_path, document in self._get_ixbrl_file_paths():
            >>>     print(ixbrl_file_path, document)
            output:
            /Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/jpcrp030000-asr-001_E03001-000_2021-03-31_01_2021-06-25_ixbrl.htm cf
            /Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/jpcrp030000-asr-001_E03001-000_2021-03-31_01_2021-06-25_ixbrl.htm sm
        """

        # iXBRLファイルのパスをDataFrameに変換
        ixbrl_files_path_df = DataFrame(self.ixbrl_files_path)

        for index, row in ixbrl_files_path_df.iterrows():
            ixbrl_file_path = row['file_path']
            document = row['document']

            yield ixbrl_file_path, document

    @property
    def ix_non_fractions(self, ixbrl_type:str = None) -> DataFrame:
        """ 非分数データを含むDataFrameを返します。

        Returns:
            ix_non_fractions_df(DataFrame): 非分数データを含むDataFrame

        Examples:
            >>> print(self.ix_non_fractions)
            output:
            document  context_ref  unit_ref  decimals  scale  value
            0        cf  FY2021Q1  JPY  0  0  1.000000e+09
            1        cf  FY2021Q1  JPY  0  0  1.000000e+09
        """
        if self._BaseIxbrlManager__ix_non_fractions is not None:
            return self._BaseIxbrlManager__ix_non_fractions

        # non_fractions_df(DataFrame)を初期化
        non_fractions_df = None

        # ixbrlファイルのパスを取得
        for ixbrl_file_path, document in self._get_ixbrl_file_paths():

            # ixbrl_typeが指定されている場合は、documentと一致するか確認
            if ixbrl_type is not None and document != ixbrl_type:
                continue

            # ixbrl_parserのインスタンスを読み込む
            parser:IxbrlParser = self._BaseIxbrlManager__parser
            parser.file_path = ixbrl_file_path

            # 非分数データを取得
            non_fractions = parser.ix_non_fractions

            # non_fractions(DataFrame)にdocument列を追加
            non_fractions['document'] = document

            # non_fractions_df(DataFrame)にnon_fractionsを追加
            if non_fractions_df is None:
                non_fractions_df = non_fractions
            else:
                non_fractions_df = pd.concat([non_fractions_df, non_fractions], ignore_index=True)

        # 非分数データを保持するプロパティに代入
        self._BaseIxbrlManager__ix_non_fractions = non_fractions_df

        # 非分数データを返す
        return self._BaseIxbrlManager__ix_non_fractions

    @property
    def ix_non_numerics(self, ixbrl_type:str = None) -> DataFrame:
        """ 非数値データを含むDataFrameを返します。

        Args:
            ixbrl_type (str): iXBRLの種類を指定します。

        Returns:
            ix_non_numerics_df(DataFrame): 非数値データを含むDataFrame

        Examples:
            >>> print(self.ix_non_numerics)
            output:
            document  context_ref  unit_ref  decimals  scale  value
            0        cf  FY2021Q1  JPY  0  0  1.000000e+09
            1        cf  FY2021Q1  JPY  0  0  1.000000e+09
        """
        if self._BaseIxbrlManager__ix_non_numerics is not None:
            return self._BaseIxbrlManager__ix_non_numerics

        # non_numerics_df(DataFrame)を初期化
        non_numerics_df = None

        # ixbrlファイルのパスを取得
        for ixbrl_file_path, document in self._get_ixbrl_file_paths():

            # ixbrl_typeが指定されている場合は、documentと一致するか確認
            if ixbrl_type is not None and document != ixbrl_type:
                continue

            # ixbrl_parserのインスタンスを読み込む
            parser:IxbrlParser = self._BaseIxbrlManager__parser
            parser.file_path = ixbrl_file_path

            # 非数値データを取得
            non_numerics = parser.ix_non_numerics

            # non_numerics(DataFrame)にdocument列を追加
            non_numerics['document'] = document

            # non_numerics_df(DataFrame)にnon_numericsを追加
            if non_numerics_df is None:
                non_numerics_df = non_numerics
            else:
                non_numerics_df = pd.concat([non_numerics_df, non_numerics], ignore_index=True)

        # 非数値データを保持するプロパティに代入
        self._BaseIxbrlManager__ix_non_numerics = non_numerics_df

        # 非数値データを返す
        return self._BaseIxbrlManager__ix_non_numerics

    @property
    def xbrli_contexts(self, ixbrl_type:str = None) -> DataFrame:
        """ 文脈情報を含むDataFrameを返します。

        Args:
            ixbrl_type (str): iXBRLの種類を指定します。

        Returns:
            xbrli_contexts_df(DataFrame): 文脈情報を含むDataFrame

        Examples:
            >>> print(self.xbrli_contexts)
            output:
            document  context_ref  entity  period  scenario  segment
            0        cf  FY2021Q1  2021-04-01  2021-06-30  None  None
            1        cf  FY2021Q1  2021-04-01  2021-06-30  None  None
        """
        if self._BaseIxbrlManager__xbrli_contexts is not None:
            return self._BaseIxbrlManager__xbrli_contexts

        # xbrli_contexts_df(DataFrame)を初期化
        xbrli_contexts_df = None

        # ixbrlファイルのパスを取得
        for ixbrl_file_path, document in self._get_ixbrl_file_paths():

            # ixbrl_typeが指定されている場合は、documentと一致するか確認
            if ixbrl_type is not None and document != ixbrl_type:
                continue

            # ixbrl_parserのインスタンスを読み込む
            parser:IxbrlParser = self._BaseIxbrlManager__parser
            parser.file_path = ixbrl_file_path

            # 文脈情報を取得
            xbrli_contexts = parser.xbrli_contexts

            # xbrli_contexts(DataFrame)にdocument列を追加
            xbrli_contexts['document'] = document

            # xbrli_contexts_df(DataFrame)にxbrli_contextsを追加
            if xbrli_contexts_df is None:
                xbrli_contexts_df = xbrli_contexts
            else:
                xbrli_contexts_df = pd.concat([xbrli_contexts_df, xbrli_contexts], ignore_index=True)

        # 文脈情報を保持するプロパティに代入
        self._BaseIxbrlManager__xbrli_contexts = xbrli_contexts_df

        # 文脈情報を返す
        return self._BaseIxbrlManager__xbrli_contexts
