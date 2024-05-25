from bs4 import BeautifulSoup as bs
from pandas import DataFrame
import unicodedata
import re

class QualitativeParser:
    # 初期化メソッド（コンストラクタ）
    def __init__(self, file_path:str) -> None:
        self.__file_path = file_path  # ファイルパスをプライベート変数に格納
        # BeautifulSoupオブジェクトを作成し、HTMLファイルの解析を行う
        self.soup = bs(open(file_path), features='html.parser')

    # HTMLから特定のデータを抽出するメソッド
    def get_smt_head(self):
        lists = []  # 結果を格納するためのリスト

        head1_title = ""  # 第1レベルの見出しを格納する変数
        head2_title = ""  # 第2レベルの見出しを格納する変数
        for tag in self.soup.find_all(class_=True):  # クラス属性があるすべてのタグを検索
            dict = {}  # 各タグから取得したデータを格納するための辞書
            class_ = tag["class"][0]  # タグの最初のクラス名を取得

            # 第1レベルの見出しの場合
            if class_ == "smt_head1" and not tag.text == head1_title:
                head1_title = tag.text  # 見出しを更新
            # 第2レベルの見出しの場合
            elif class_ == "smt_head2" and not tag.text == head2_title:
                head2_title = tag.text  # 見出しを更新
            # テキストデータの場合
            elif "smt_text" in class_:
                # 既にリストにデータが存在する場合
                if len(lists) > 0:
                    # 前の要素と見出しが異なる場合は新しい辞書を追加
                    if not lists[-1]['title'] == head1_title and lists[-1]['sub_title'] == head2_title:
                        dict['title'] = head1_title
                        dict['sub_title'] = ""
                        dict['text'] = tag.text
                        lists.append(dict)
                    # 前の要素とサブタイトルが同じ場合はテキストを追記
                    elif lists[-1]['sub_title'] == head2_title:
                        lists[-1]['text'] += tag.text
                    else:
                        # 新しい見出しの場合は新しい辞書を作成してリストに追加
                        dict['title'] = head1_title
                        dict['sub_title'] = head2_title
                        dict['text'] = tag.text
                        lists.append(dict)
                else:
                    # リストが空の場合は新しい辞書を作成して追加
                    dict['title'] = head1_title
                    dict['sub_title'] = head2_title
                    dict['text'] = tag.text
                    lists.append(dict)

        # 行のリストを処理
        i = 0
        while i < len(lists):
            row = lists[i]
            # タイトル、サブタイトル、テキストの正規化を行う
            row['title'] = unicodedata.normalize('NFKC', row['title'])
            row['sub_title'] = unicodedata.normalize('NFKC', row['sub_title'])
            row['text'] = re.sub(" ", "", unicodedata.normalize('NFKC', row['text']))

            # タイトルに数字が含まれていない場合、現在の行を削除
            if not re.search(r'\d', row['title']):
                lists.pop(i)  # 現在のインデックスの行をリストから削除
                # インデックスを減らす必要はない。popにより次の要素が現在のインデックスに移動するため。
            else:
                i += 1  # 条件に合わない場合はインデックスを増やして次の要素に進む

        return DataFrame(lists)  # 抽出したデータをDataFrameに変換して返す

# スクリプトが直接実行された場合に以下を実行
if __name__ == '__main__':
    # 解析対象のファイルパス
    file_path = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Attachment/qualitative.htm"
    qp = QualitativeParser(file_path)  # QualitativeParserクラスのインスタンスを作成
    # 抽出したデータを表示（コメントアウトされている）
    # print(qp.get_smt_head())
    qp.get_smt_head().to_csv('qp.csv')  # 抽出したデータをCSVファイルに保存
