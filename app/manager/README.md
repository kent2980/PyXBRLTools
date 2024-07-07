# BaseXbrlManager

XBRLディレクトリの解析をするための基底クラスです。

このクラスを継承したクラスには下記の機能を提供します。

## 機能

* ファイルの一覧
* 書類の種類を表示
* ファイルを抽出

## メソッド

| メソッド               | 機能                           | 戻り値    |
| ------------------ | ---------------------------- | ------ |
| to_filelist        | ディレクトリ内のファイルをlistで返します。      | ファイル一覧 |
| xbrl_type          | XBRLの種類を確認します。               | 書類品種   |
| set_linkbase_files | 関係ファイルのリストを設定します。            | インスタンス |
| set_htmlbase_files | htmlbaseファイルのリストを設定します。      | インスタンス |
| get_roles          | ディレクトリ内に存在するファイルのroleを取得します。 | list   |
| to_csv             | 取得データをCSVに出力します。             | 取得データ  |
| to_DataFrame       | 取得データをDataFrameで出力します。       | 取得データ  |
| to_json            | 取得データをJSONで出力します。            | 取得データ  |
| to_dict            | 取得データを辞書形式で出力します。            | 取得データ  |

# IxbrlManager

XBRLディレクトリ内のixbrl.htmファイルを解析するクラスです。

決算サマリー、各財務諸表からデータを受け取り出力します。

## 機能

* 全て、または指定ファイルからデータを取得・出力
*

## メソッド

| メソッド            | 機能                             | 戻り値       |
| ------------------- | -------------------------------- | ------------ |
| set_ix_non_fraction | 取得データを非分数に設定します。 | インスタンス |
| set_ix_non_numeric  | 取得データを非数値に設定します。 | インスタンス |