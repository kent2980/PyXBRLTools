from xbrl_manager.xbrl_label_manager import XbrlLabelManager
from xbrl_manager.xbrl_link_manager import XbrlLinkManager, XbrlLinkType
from xbrl_manager.ixbrl_manager import IxbrlManager
import zipfile
import shutil
import os
import time

class XbrlRead:
    def __init__(self, xbrl_zip_path, xbrl_directory_path, load_label_directory):

        # ZIPファイルのパスを設定
        self.__xbrl_zip_path = xbrl_zip_path
        # zipファイルの名前を取得
        self.__xbrl_zip_filename = xbrl_zip_path.split('/')[-1].split('.')[0]
        # ZIPファイルを解凍するディレクトリのパスを設定
        self.__xbrl_directory_path = f"{xbrl_directory_path}/{self.__xbrl_zip_filename}"
        # グローバルラベルファイルをロードするディレクトリのパスを設定
        self.__load_label_directory = load_label_directory
        # zipファイルを解凍
        zipfile.ZipFile(xbrl_zip_path).extractall(self.__xbrl_directory_path)

        # iXBRLマネージャーのインスタンスを作成
        self.__ixbrl_manager = IxbrlManager(self.__xbrl_directory_path)
        # IXBRLラベルマネージャーのインスタンスを作成
        self.__label_manager = XbrlLabelManager(self.__xbrl_directory_path, self.__load_label_directory)
        # IXBRLリンクマネージャーのインスタンスを作成
        self.__link_manager = XbrlLinkManager(self.__xbrl_directory_path, XbrlLinkType.CAL)

        # ラベルLocsを取得
        self.__label_locs = self.__label_manager.get_label_locs()
        # ラベルArcsを取得
        self.__label_arcs = self.__label_manager.get_label_arcs()
        # ラベルを取得
        self.__labels = self.__label_manager.get_labels()

        # リンクlocsを取得
        self.__link_locs = self.__link_manager.get_link_locs()
        # リンクArcsを取得
        self.__link_arcs = self.__link_manager.get_link_arcs()

    def __del__(self):
        """ デストラクタ """

        # 解凍したファイルを削除
        if os.path.exists(self.__xbrl_directory_path):
            shutil.rmtree(self.__xbrl_directory_path)

    def get_ix_non_fractions(self):
        """
        iXBRLファイルの非分数を取得するメソッドです。
        """
        # ix_non_fractionsを取得
        ix_non_fractions = self.__ixbrl_manager.ix_non_fractions
        # ix_non_fractionsのnameを取得
        ix_non_fractions_name = list(set(ix_non_fractions['name'].to_list()))

        # label_locsを取得
        label_locs = self.__label_locs[self.__label_locs['xlink_href'].isin(ix_non_fractions_name)]
        # label_locsのxlink_labelを取得
        label_locs_xlink_label = list(set(label_locs['xlink_label'].to_list()))
        # label_arcsを取得
        label_arcs = self.__label_arcs[self.__label_arcs['xlink_from'].isin(label_locs_xlink_label)]
        # label_arcsのxlink_toを取得
        label_arcs_xlink_to = list(set(label_arcs['xlink_to'].to_list()))
        # labelを取得
        labels = self.__labels[self.__labels['xlink_label'].isin(label_arcs_xlink_to)]

        # link_arcsを取得
        print(self.__link_arcs)
        link_arcs = self.__link_arcs[self.__link_arcs['xlink_to'].isin(ix_non_fractions_name)]

        # ix_non_fractions, label_arcs, label_locs, labelsを返す
        return ix_non_fractions, label_arcs, label_locs, labels, link_arcs

    def get_ix_non_numerics(self):
        """
        iXBRLファイルの非数値を取得するメソッドです。
        """
        # ix_non_numericsを取得
        ix_non_numerics = self.__ixbrl_manager.ix_non_numerics
        # ix_non_numericsのnameを取得
        ix_non_numerics_name = list(set(ix_non_numerics['name'].to_list()))

        # label_locsを取得
        label_locs = self.__label_locs[self.__label_locs['xlink_href'].isin(ix_non_numerics_name)]
        # label_locsのxlink_labelを取得
        label_locs_xlink_label = list(set(label_locs['xlink_label'].to_list()))
        # label_arcsを取得
        label_arcs = self.__label_arcs[self.__label_arcs['xlink_from'].isin(label_locs_xlink_label)]
        # label_arcsのxlink_toを取得
        label_arcs_xlink_to = list(set(label_arcs['xlink_to'].to_list()))
        # labelを取得
        labels = self.__labels[self.__labels['xlink_label'].isin(label_arcs_xlink_to)]

        # ix_non_numerics, label_arcs, label_locs, labelsを返す
        return ix_non_numerics, label_arcs, label_locs, labels


if __name__ == '__main__':
    # 処理時間を計測
    start = time.time()

    xbrl_zip_path = '/Users/user/Vscode/python/PyXBRLTools/doc/081220240327560965.zip'
    xbrl_direrctory_path = '/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRL'
    load_xbrl_directory_path = '/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/labels'

    xbrl_read = XbrlRead(xbrl_zip_path, xbrl_direrctory_path, load_xbrl_directory_path)

    ix_non_fractions, label_arcs, label_locs, labels, link_arcs = xbrl_read.get_ix_non_fractions()

    print(ix_non_fractions)
    print(label_locs)
    print(label_arcs)
    print(labels)
    print(link_arcs)
    labels.to_csv('non_fractions_labels.csv', index=False)
    link_arcs.to_csv('non_fractions_link_arcs.csv', index=False)

    ix_non_numerics, label_arcs, label_locs, labels = xbrl_read.get_ix_non_numerics()
    print(ix_non_numerics)
    print(label_locs)
    print(label_arcs)
    print(labels)

    labels.to_csv('non_numerics_labels.csv', index=False)

    # 処理時間を表示
    elapsed_time = time.time() - start

    print(f"処理時間：{elapsed_time}秒")