# モジュール群のREADME

このディレクトリには、各種XBRLをパースするモジュールが含まれます。
対応するXBRLファイルを下記に記します。
マークダウンで表を作成するには、以下のような書式を使用します。

<table>
    <tr style="height: 50px">
        <th>対応する<br/>ファイル名</th>
        <th>モジュール名</th>
        <th>説明</th>
    </tr>
    <tr style="height: 80px">
        <td style="text-align: center">**-ixbrl.htm</td>
        <td style="text-align: center">xbrl_ixbrl_parser.py</td>
        <td>短信サマリー、各財務諸表の数値、非数値情報を取得します。</td>
    </tr>
    <tr style="height: 80px">
        <td style="text-align: center">qualitative.htm</td>
        <td style="text-align: center">xbrl_qualitative_parser.py</td>
        <td>決算短信の「経営状況の概要」など、定性的情報を取得します。</td>
    </tr>
    <tr style="height: 80px">
        <td style="text-align: center">**.xsd</td>
        <td style="text-align: center">xml_schema_parser.py</td>
        <td>XBRLのデータ構造を定義しており、関連ファイルを取得します。</td>
    </tr>
    <tr style="height: 80px">
        <td style="text-align: center">**-lab.xml</td>
        <td style="text-align: center">xml_label_parser.py</td>
        <td>各財務諸表の数値、非数値データと関連づけられた名称ラベルを取得します。</td>
    </tr>
    <tr style="height: 80px">
        <td style="text-align: center">**-cal.xml<br/>**-def.xml<br/>*-pre.xml</td>
        <td style="text-align: center">xml_link_parser.py</td>
        <td>計算リンク、表示リンク、定義リンクから順序関係に関するデータを取得します。</td>
    </tr>
</table>


以下に、各モジュールの概要と使用方法について説明します。

## 1.xbrl_ixbrl_parser.py

このモジュールは、XBRLから財務諸表の数値、非数値データを取得する機能を提供するために作成されました。以下の手順に従って、モジュールを使用することができます。

1. モジュールからクラスをインポートします。

```python
from xbrl_ixbrl_parser import XbrlIxbrlParser
```

2. パーサーのインスタンスを作成します。

```python
parser = XbrlIxbrlParser('path_to_ixbrl_file')
```

3. 必要なデータを取得します。

```python
financial_data = parser.parse_financials()
notes = parser.parse_notes()
```

## 2.xbrl_qualitative_parser.py

このモジュールは、決算短信の定性的情報を抽出するために使用されます。使い方は以下の通りです。

1. モジュールをインポートします。

```python
from xbrl_qualitative_parser import XbrlQualitativeParser
```

2. パーサーのインスタンスを作成し、ファイルを読み込みます。

```python
parser = XbrlQualitativeParser('path_to_qualitative_file')
```

3. 定性的情報を取得します。

```python
qualitative_data = parser.get_qualitative_data()
```

## 3.xml_schema_parser.py

このモジュールは、XBRLのXMLスキーマファイルを解析し、タクソノミの構造を理解するために使用されます。以下の手順で使用します。

1. モジュールのインポート:

```python
from xml_schema_parser import XmlSchemaParser
```

2. スキーマファイルのパーサーを初期化:

```python
parser = XmlSchemaParser('path_to_xsd_file')
```

3. スキーマ情報の取得:

```python
schema_info = parser.parse_schema()
```

## 4.xml_label_parser.py

このモジュールは、ラベルリンクベースを解析して、要素に対するラベル情報を抽出します。使い方は次のとおりです。

1. モジュールをインポートします。

```python
from xml_label_parser import XmlLabelParser
```

2. ラベルパーサーをインスタンス化します。

```python
parser = XmlLabelParser('path_to_lab_file')
```

3. ラベルデータを取得します。

```python
labels = parser.get_labels()
```

## 5.xml_link_parser.py

このモジュールは、計算、表示、定義リンクベースを解析して、要素間の関係性を取得するために使用されます。以下の手順に従います。

1. モジュールをインポートします。

```python
from xml_link_parser import XmlLinkParser
```

2. リンクパーサーをインスタンス化します。

```python
parser = XmlLinkParser('path_to_linkbase_file')
```

3. リンクデータを取得します。

```python
link_data = parser.get_links()
```

これで、各モジュールの基本的な使い方を説明しました。実際のコードでは、適切なファイルパスや追加の処理が必要になる場合があります。