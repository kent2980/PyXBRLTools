# BaseXBRLParser

`BaseXBRLParser`はXBRLを解析するための基底クラスです。
このクラスを継承したクラスには以下の機能を提供します。

## 機能

`BaseXBRLParser`クラスは以下の機能を提供します:

- XBRLのダウンロード
- XBRLの解析
- XBRLの情報取得
- 出力形式の選択

## 引数

-`xbrl_url` (str): XBRLのURL、またはローカルパス
-`output_path` (str): ファイルの保存先

## プロパティ

-`data` (list[dict]): 解析結果のデータ

## メソッド

-`read_xbrl()`: XBRLを読み込む

-`parse_xbrl()`: XBRLを解析する

-`fetch_url()`: URLからXBRLを取得する

-`is_url_in_local()`: URLがローカルに存在するか判定する

-`create()`: `BaseXBRLParser`の初期化を行うクラスメソッド

-`to_csv()`: CSV形式で出力する

-`to_DataFrame()`: DataFrame形式で出力する

-`to_json()`: JSON形式で出力する

-`to_dict()`: 辞書形式で出力する

## 使用方法

```python
parser = BaseXBRLParser.create(xbrl_path, output_dir)
df = parser.to_DataFrame()
```

# IxbrlParser

`IxbrlParser`はiXBRLを解析するためのクラスです。このクラスは `BaseXBRLParser`を継承しており、iXBRLの解析に関する機能を提供します。

## 引数

- `xbrl_url` (str): XBRLのURL、またはローカルパス
- `output_path` (str): ファイルの保存先

## プロパティ

- `data` (list[dict]): 解析結果のデータ

## メソッド

- `ix_non_numeric()`: iXBRLの非数値情報を取得します。
- `ix_non_fractions()`: iXBRLの非分数情報を取得します。

## 使用例

```python
parser = IxbrlParser.create(xbrl_path)
df = parser.ix_non_numeric().to_DataFrame()
```
