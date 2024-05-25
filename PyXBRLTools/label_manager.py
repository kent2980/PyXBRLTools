from pandas import DataFrame
import re
from bs4 import BeautifulSoup as bs
from utils import Utils
import time
import os
from xbrl_parser.xml_label_parser import XmlLocalLabel, XmlGlobalLabel

class LabelManager:

    def __init__(self, xbrl_dir_path:str):
        print("init")
        self.xbrl_dir_path = xbrl_dir_path
        self.taxonomy_dir = '/Users/user/Vscode/python/disclosure_api2/doc/taxnomy'
        self.label_links_df:DataFrame = DataFrame()
        self.label_pd:DataFrame = DataFrame()

        # labelデータレームの初期化を行います。
        self.init_label_df()

    def init_label_df(self):
        # ラベルリンクのDataFrameを取得します。
        label_links_df: DataFrame = self.find_label_links_df()
        # 取得したラベルファイルをtaxonomy_dirにダウンロードします。
        self.get_label_files(label_links_df, self.taxonomy_dir)
        # ローカルパスを設定したDataFrameを更新します。
        self.label_links_df = self.set_local_path(label_links_df, self.taxonomy_dir)
        # ローカルラベルのDataFrameを取得します。
        self.get_local_label_df()
        # グローバルラベルのDataFrameを取得します。
        self.get_global_label_df(self.label_links_df)


    def find_label_links_df(self) -> DataFrame:
        # ラベルリンクの情報を格納するためのリストを初期化します。
        label_links = []
        print(self.xbrl_dir_path)
        # 指定されたディレクトリ内で正規表現にマッチするファイル名を検索します。
        files = Utils.find_filename_with_regex(self.xbrl_dir_path, "^.*xsd$")

        # 各ファイルに対して処理を行います。
        for file in files:
            # ファイルタイプを決定します（'Attachment'が含まれる場合は'Attachment'、それ以外は'Summary'）。
            type = "Attachment" if "Attachment" in file else "Summary"

            # 対象のファイルをスクレイピングするためにBeautifulSoupオブジェクトを作成します。
            soup = bs(open(file), features='xml')

            # ラベルリンクを参照する要素を全て検索します。
            link_refs = soup.find_all(attrs={'xlink:role':'http://www.xbrl.org/2003/role/labelLinkbaseRef'})

            # 取得したラベルリンク参照に対して処理を行います。
            for link_ref in link_refs:
                # 'xlink:href'属性からラベルリンクを取得します。
                label_link = link_ref.get('xlink:href')

                # リンクがラベルXMLファイルを指しているか確認します。
                if re.search('^.*lab.xml$', label_link):
                    # リンクに関する情報を辞書に格納します。
                    link_dic = {}
                    link_dic['doc_type'] = type
                    # リンクタイプを決定します（'http'を含む場合は'global'、それ以外は'local'）。
                    link_dic['link_type'] = 'global' if 'http' in label_link else 'local'
                    link_dic['link'] = label_link
                    # 辞書をリストに追加します。
                    label_links.append(link_dic)

        # リストからDataFrameを作成します。
        label_links_df = DataFrame(label_links)
        # 空のカラム'local_path'をDataFrameに追加します。
        label_links_df['local_path'] = ''
        # DataFrameを返却します。
        return label_links_df

    def get_label_files(self, label_links_df: DataFrame, taxonomy_dir: str):
        # データフレームからlink_typeが'global'である行を取得します。
        global_label_df = label_links_df.query("link_type == 'global'")

        # タクソノミーディレクトリを走査してファイルをダウンロードします。
        for index, row in global_label_df.iterrows():
            # タクソノミーディレクトリ内にファイルが存在しない場合、ダウンロードを実施
            file_name = os.path.basename(row['link'])
            local_file_path = os.path.join(taxonomy_dir, file_name)
            if not os.path.isfile(local_file_path):
                # リンクからファイルをダウンロードして、タクソノミーディレクトリに保存します。
                download_file_to_dir(row['link'], taxonomy_dir)
                # ダウンロードしたファイルのパスをDataFrameに記録します。
                label_links_df.at[index, 'local_path'] = local_file_path
                # サーバーへの負荷を防ぐために、次の処理まで2秒間待機します。
                time.sleep(2)

    def set_local_path(self,label_links_df:DataFrame, taxonomy_dir:str):
        # タクソノミーディレクトリを再度走査して、各ファイルのローカルパスを更新します。
        for root, dirs, files in os.walk(taxonomy_dir):
            for file in files:
                # すべてのラベルリンクについてチェックし、対応するローカルパスをDataFrameに設定します。
                for index, row in label_links_df.iterrows():
                    if file in row['link']:
                        # ここでfileではなくos.path.join(root, file)を使用して正しいパスを設定します。
                        label_links_df.at[index, 'local_path'] = os.path.join(root, file)

        # 結果のDataFrameを出力します。
        print(label_links_df)
        return label_links_df

    def get_local_label_df(self) -> DataFrame:

        # ローカルラベルファイルを抽出する
        local_filename = self.label_links_df.query("link_type == 'local'")
        for index, row in local_filename.iterrows():
            files = Utils.find_filename_with_keyword(self.xbrl_dir_path, row['link'])
            for file in files:
                labels = XmlLocalLabel(file)
                local_label_df = labels.link_labels

        return local_label_df

    def get_global_label_df(self, label_files_df:DataFrame)-> DataFrame:
        label_files_df = label_files_df.query("link_type == 'global'")
        for index, row in label_files_df.iterrows():
            print(row['local_path'])
            soup = bs(open(row['local_path']), features='xml')
            print(soup)

if __name__ == '__main__':
    zip_path:str = "/Users/user/Vscode/python/disclosure_api2/doc/dummy.zip"
    extra_dir:str = "/Users/user/Vscode/python/disclosure_api2/doc/extract_to_dir"
    Utils.extract_zip(zip_path,extra_dir)

    lm = LabelManager(extra_dir)

    Utils.initialize_directory(extra_dir)
