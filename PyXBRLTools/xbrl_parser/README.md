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

# LabelParser

## 概要

`LabelParser` クラスは XBRL のラベル情報を取得するためのクラスです。このクラスは `BaseXBRLParser` を継承しており、XBRL のラベル情報を解析し、取得します。

## 特徴

- **ラベル情報の取得**: XBRL ファイルからラベル情報を抽出します。

## 属性

- `xbrl_url`: `str`
  - XBRL の URL
- `output_path`: `str`
  - ファイルの保存先

## プロパティ

- `data`: `list[dict]`
  - 解析結果のデータ

## メソッド

- `link_labels`
  - `link:label` 要素を取得する
- `link_locs`
  - `link:loc` 要素を取得する
- `link_label_arcs`
  - `link:labelArc` 要素を取得する
- `role_refs`
  - `roleRef` 要素を取得する

## 使用例

```python
from xbrl_parser.label_parser import LabelParser

parser = LabelParser.create(file_path)
print(parser.label().to_dataframe())
```

## 詳細メソッド

### `link_labels`

`link:label` 要素を取得するメソッド。

#### 戻り値

- `self`: `LabelParser`

#### 使用例

```python
parser = XmlLabelParser("**-lab.xml")
df = parser.link_labels()

# 取得する DataFrame の例
# xlink_type (str): resource
# xlink_label (str): label_EquityClassOfShares
# xlink_role (str): http://www.xbrl.org/2003/role/label
# xml_lang (str): ja
# id (str): label_EquityClassOfShares
# label (str): 株式の種類
```

### `link_locs`

`link:loc` 要素を取得するメソッド。

#### 戻り値

- `self`: `LabelParser`

#### 使用例

```python
parser = XmlLabelParser("**-lab.xml")
df = parser.link_locs()

# 取得する DataFrame の例
# xlink_type (str): locator
# xlink_schema (str): http://disclosure.edinet-fsa.go.jp/taxonomy/jppfs/2021-12-01/jppfs_cor_2023-12-01.xsd
# xlink_href (str): jppfs_cor_EquityClassOfShares
# xlink_label (str): label_EquityClassOfShares
```

### `link_label_arcs`

`link:labelArc` 要素を取得するメソッド。

#### 戻り値

- `self`: `LabelParser`

#### 使用例

```python
parser = XmlLabelParser("**-lab.xml")
df = parser.link_label_arcs()

# 取得する DataFrame の例
# xlink_type (str): arc
# xlink_arcrole (str): http://www.xbrl.org/2003/arcrole/concept-label
# xlink_from (str): EquityClassOfShares
# xlink_to (str): label_EquityClassOfShares
```

### `role_refs`

`roleRef` 要素を取得するメソッド。

#### 戻り値

- `self`: `LabelParser`

#### 使用例

```python
parser = XmlLabelParser("**-lab.xml")
df = parser.role_refs()

# 取得する DataFrame の例
# Role_URI (str): http://disclosure.edinet-fsa.go.jp/jpcrp/std/alt/role/label
# xlink_type (str): simple
# xlink_schema (str): jpcrp_rt_2023-12-01.xsd
# xlink_href (str): rol_std_altLabel
```

# CalLinkParser

## 概要

`CalLinkParser` クラスは XBRL の計算リンク情報を取得するためのクラスです。このクラスは `BaseXBRLParser` を継承しており、XBRL ファイルから計算リンク情報を解析し取得します。

## 特徴

- **計算リンク情報の取得**: XBRL ファイルから計算リンク情報を抽出します。

## メソッド

- `link_roles`
  - `link:role` 要素を取得する
- `link_locs`
  - `link:loc` 要素を取得する
- `link_arcs`
  - `link:arc` 要素を取得する
- `link_base`
  - `link:base` 要素を取得する
- `calculationLink`
  - `link` 要素を取得する

## 使用例

```python
from xbrl_parser.cal_link_parser import CalLinkParser

parser = CalLinkParser.create(file_path)
df_roles = parser.link_roles().to_dataframe()
df_locs = parser.link_locs().to_dataframe()
df_arcs = parser.link_arcs().to_dataframe()
df_base = parser.link_base().to_dataframe()
df_calc_link = parser.calculationLink().to_dataframe()
```

## 詳細メソッド

### `link_roles`

`link:role` 要素を取得するメソッド。

#### 戻り値

- `DataFrame`: `link:role` 要素を含む DataFrame

#### 使用例

```python
parser = XmlLabelParser("**-lab.xml")
df = parser.link_roles().to_dataframe()

# 取得する DataFrame の例
# xlink_type (str): simple
# xlink_href (str): http://disclosure.edinet-fsa.go.jp/taxonomy/jppfs/2023-12-01/jppfs_cor_2023-12-01.xsd
# role_uri (str): http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_ConsolidatedBalanceSheet
```

### `link_locs`

`link:loc` 要素を取得するメソッド。

#### 戻り値

- `DataFrame`: `link:loc` 要素を含む DataFrame

#### 使用例

```python
parser = XmlLabelParser("**-lab.xml")
df = parser.link_locs().to_dataframe()

# 取得する DataFrame の例
# xlink_type (str): locator
# xlink_href (str): jppfs_cor_2023-12-01.xsd
# xlink_label (str): jppfs_cor_EquityClassOfShares
```

### `link_arcs`

`link:arc` 要素を取得するメソッド。

#### 戻り値

- `DataFrame`: `link:arc` 要素を含む DataFrame

#### 使用例

```python
parser = XmlLabelParser("**-lab.xml")
df = parser.link_arcs().to_dataframe()

# 取得する DataFrame の例
# xlink_type (str): arc
# xlink_from (str): jppfs_cor_AccountsPayableOther
# xlink_to (str): jppfs_lab_AccountsPayableOther
# xlink_arcrole (str): http://www.xbrl.org/2003/arcrole/concept-label
# xlink_order (int): 1
# xlink_weight (int): 1
```

### `link_base`

`link:base` 要素を取得するメソッド。

#### 戻り値

- `DataFrame`: `link:base` 要素を含む DataFrame

#### 使用例

```python
parser = XmlLabelParser("**-lab.xml")
df = parser.link_base().to_dataframe()

# 取得する DataFrame の例
# xmlns_xlink (str): http://www.w3.org/1999/xlink
# xmlns_xsi (str): http://www.w3.org/2001/XMLSchema-instance
# xmlns_link (str): http://www.xbrl.org/2003/linkbase
```

### `calculationLink`

`link` 要素を取得するメソッド。

#### 戻り値

- `DataFrame`: `link` 要素を含む DataFrame

#### 使用例

```python
parser = XmlLabelParser("**-lab.xml")
df = parser.calculationLink().to_dataframe()

# 取得する DataFrame の例
# xlink_type (str) : extended
# xlink_role (str) : http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_ConsolidatedBalanceSheet
```

---

# DefLinkParser

## 概要

`DefLinkParser` クラスは XBRL の定義リンク情報を取得するためのクラスです。このクラスは `BaseXBRLParser` を継承しており、XBRL ファイルから定義リンク情報を解析し取得します。

## 特徴

- **定義リンク情報の取得**: XBRL ファイルから定義リンク情報を抽出します。

## メソッド

- `link_roles`
  - `link:role` 要素を取得する
- `link_locs`
  - `link:loc` 要素を取得する
- `link_arcs`
  - `link:arc` 要素を取得する
- `link_base`
  - `link:base` 要素を取得する
- `definitionLink`
  - `link` 要素を取得する

## 使用例

```python
from xbrl_parser.def_link_parser import DefLinkParser

parser = DefLinkParser.create(file_path)
df_roles = parser.link_roles().to_dataframe()
df_locs = parser.link_locs().to_dataframe()
df_arcs = parser.link_arcs().to_dataframe()
df_base = parser.link_base().to_dataframe()
df_def_link = parser.definitionLink().to_dataframe()
```

## 詳細メソッド

### `link_roles`

`link:role` 要素を取得するメソッド。

#### 戻り値

- `DataFrame`: `link:role` 要素を含む DataFrame

#### 使用例

```python
parser = DefLinkParser("**-def.xml")
df = parser.link_roles().to_dataframe()

# 取得する DataFrame の例
# xlink_type (str): simple
# xlink_href (str): http://disclosure.edinet-fsa.go.jp/taxonomy/jppfs/2023-12-01/jppfs_cor_2023-12-01.xsd
# role_uri (str): http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_ConsolidatedBalanceSheet
```

### `link_locs`

`link:loc` 要素を取得するメソッド。

#### 戻り値

- `DataFrame`: `link:loc` 要素を含む DataFrame

#### 使用例

```python
parser = XmlLabelParser("**-def.xml")
df = parser.link_locs().to_dataframe()

# 取得する DataFrame の例
# xlink_type (str): locator
# xlink_href (str): jppfs_cor_2023-12-01.xsd
# xlink_label (str): jppfs_cor_EquityClassOfShares
```

### `link_arcs`

`link:arc` 要素を取得するメソッド。

#### 戻り値

- `DataFrame`: `link:arc` 要素を含む DataFrame

#### 使用例

```python
parser = XmlLabelParser("**-def.xml")
df = parser.link_arcs().to_dataframe()

# 取得する DataFrame の例
# xlink_type (str): arc
# xlink_from (str): jppfs_cor_AccountsPayableOther
# xlink_to (str): jppfs_lab_AccountsPayableOther
# xlink_arcrole (str): http://www.xbrl.org/2003/arcrole/concept-label
# xlink_order (int): 1
# xlink_weight (int): 1
```

### `link_base`

`link:base` 要素を取得するメソッド。

#### 戻り値

- `DataFrame`: `link:base` 要素を含む DataFrame

#### 使用例

```python
parser = XmlLabelParser("**-lab.xml")
df = parser.link_base().to_dataframe()

# 取得する DataFrame の例
# xmlns_xlink (str): http://www.w3.org/1999/xlink
# xmlns_xsi (str): http://www.w3.org/2001/XMLSchema-instance
# xmlns_link (str): http://www.xbrl.org/2003/linkbase
```

### `definitionLink`

`link` 要素を取得するメソッド。

#### 戻り値

- `DataFrame`: `link` 要素を含む DataFrame

#### 使用例

```python
parser = XmlLabelParser("**-lab.xml")
df = parser.definitionLink().to_dataframe()

# 取得する DataFrame の例
# xlink_type (str) : extended
# xlink_role (str) : http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_ConsolidatedBalanceSheet
```

---

# PreLinkParser

## 概要

`PreLinkParser` クラスは XBRL のプレゼンテーションリンク情報を取得するためのクラスです。このクラスは `BaseXBRLParser` を継承しており、XBRL ファイルからプレゼンテーションリンク情報を解析し取得します。

## 特徴

- **プレゼンテーションリンク情報の取得**: XBRL ファイルからプレゼンテーションリンク情報を抽出します。

## メソッド

- `link_roles`
  - `link:role` 要素を取得する
- `link_locs`
  - `link:loc` 要素を取得する
- `link_arcs`
  - `link:arc` 要素を取得する
- `link_base`
  - `link:base` 要素を取得する
- `presentationLink`
  - `link` 要素を取得する

## 使用例

```python
from xbrl_parser.pre_link_parser import PreLinkParser

parser = PreLinkParser.create(file_path)
df_roles = parser.link_roles().to_dataframe()
df_locs = parser.link_locs().to_dataframe()
df_arcs = parser.link_arcs().to_dataframe()
df_base = parser.link_base().to_dataframe()
df_pres_link = parser.presentationLink().to_dataframe()
```

## 詳細メソッド

### `link_roles`

`link:role` 要素を取得するメソッド。

#### 戻り値

- `DataFrame`: `link:role` 要素を含む DataFrame

#### 使用例

```python
parser = XmlLabelParser("**-lab.xml")
df = parser.link_roles().to_dataframe()

# 取得する DataFrame の例
# xlink_type (str): simple
# xlink_href (str): http://disclosure.edinet-fsa.go.jp/taxonomy/jppfs/2023-12-01/jppfs_cor_2023-12-01.xsd
# role_uri (str): http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_ConsolidatedBalanceSheet
```

### `link_locs`

`link:loc` 要素を取得するメソッド。

#### 戻り値

- `DataFrame`: `link:loc` 要素を含む DataFrame

#### 使用例

```python
parser = XmlLabelParser("**-lab.xml")
df = parser.link_locs().to_dataframe()

# 取得する DataFrame の例
# xlink_type (str): locator
# xlink_href (str): jppfs_cor_2023-12-01.xsd
# xlink_label (str): jppfs_cor_EquityClassOfShares
```

### `link_arcs`

`link:arc` 要素を取得するメソッド。

#### 戻り値

- `DataFrame`: `link:arc` 要素を含む DataFrame

#### 使用例

```python
parser = XmlLabelParser("**-lab.xml")
df = parser.link_arcs().to_dataframe()

# 取得する DataFrame の例
# xlink_type (str): arc
# xlink_from (str): jppfs_cor_AccountsPayableOther
# xlink_to (str): jppfs_lab_AccountsPayableOther
# xlink_arcrole (str): http://www.xbrl.org/2003/arcrole/concept-label
# xlink_order (int): 1
# xlink_weight (int): 1
```

### `link_base`

`link:base` 要素を取得するメソッド。

#### 戻り値

- `DataFrame`: `link:base` 要素を含む DataFrame

#### 使用例

```python
parser = XmlLabelParser("**-lab.xml")
df = parser.link_base().to_dataframe()

# 取得する DataFrame の例
# xmlns_xlink (str): http://www.w3.org/1999/xlink
# xmlns_xsi (str): http://www.w3.org/2001/XMLSchema-instance
# xmlns_link (str): http://www.xbrl.org/2003/linkbase
```

### `presentationLink`

`link` 要素を取得するメソッド。

#### 戻り値

- `DataFrame`: `link` 要素を含む DataFrame

#### 使用例

```python
parser = XmlLabelParser("**-lab.xml")
df = parser.presentationLink().to_dataframe()

# 取得する DataFrame の例
# xlink_type (str) : extended
# xlink_role (str) : http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_ConsolidatedBalanceSheet
```

---

# SchemaParser

## 概要

`SchemaParser` クラスは、XBRL スキーマファイルからスキーマ情報を解析し取得するためのクラスです。このクラスは `BaseXBRLParser` を継承しており、スキーマファイル内の `import` 要素、`linkbaseRef` 要素、及び `element` 要素を解析します。

## 特徴

- **スキーマインポート情報の取得**: スキーマファイル内の `import` 要素を解析し、スキーマインポート情報を抽出します。
- **リンクベース参照情報の取得**: スキーマファイル内の `linkbaseRef` 要素を解析し、リンクベース参照情報を抽出します。
- **要素情報の取得**: スキーマファイル内の `element` 要素を解析し、要素に関する情報を抽出します。

## メソッド

### `import_schemas`

`import` 要素を取得するメソッド。

#### 戻り値

- `self`: インスタンス自体を返します。

#### 使用例

```python
parser = SchemaParser("path_to_schema_file.xsd")
parser.import_schemas()
df_imports = parser.to_dataframe()

# 取得する DataFrame の例
# schema_location (str): http://www.xbrl.org/taxonomy/int/fr/ifrs/ifrs-gp-2005-05-15.xsd
# name_space (str): http://www.xbrl.org/2003/instance
```

### `link_base_refs`

`linkbaseRef` 要素を取得するメソッド。

#### 戻り値

- `self`: インスタンス自体を返します。

#### 使用例

```python
parser = SchemaParser("path_to_schema_file.xsd")
parser.link_base_refs()
df_linkbases = parser.to_dataframe()

# 取得する DataFrame の例
# xlink_type (str): simple
# xlink_href (str): linkbase.xml
# xlink_role (str): http://www.xbrl.org/2003/role/link
# xlink_arcrole (str): http://www.xbrl.org/2003/arcrole/definitionLinkbaseRef
```

### `elements`

`element` 要素を取得するメソッド。

#### 戻り値

- `self`: インスタンス自体を返します。

#### 使用例

```python
parser = SchemaParser("path_to_schema_file.xsd")
parser.elements()
df_elements = parser.to_dataframe()

# 取得する DataFrame の例
# id (str): ifrs-full_Assets
# xbrli_balance (str): debit
# xbrli_period_type (str): instant
# name (str): Assets
# nillable (bool): True
# substitution_group (str): xbrli:item
# type (str): monetaryItemType
# abstract (bool): False
```

## 使用方法

以下のように `SchemaParser` クラスを使用して、スキーマファイルから必要な情報を取得できます。

```python
from your_module import SchemaParser

# スキーマファイルのパスを指定してインスタンスを作成
parser = SchemaParser("path_to_schema_file.xsd")

# import 要素を取得
parser.import_schemas()
df_imports = parser.to_dataframe()

# linkbaseRef 要素を取得
parser.link_base_refs()
df_linkbases = parser.to_dataframe()

# element 要素を取得
parser.elements()
df_elements = parser.to_dataframe()
```

---

# QualitativeParser

## 概要

`QualitativeParser` クラスは、XBRL ドキュメントから定性的なデータを解析し取得するためのクラスです。このクラスは `BaseXBRLParser` を継承しており、特定の HTML クラス名を持つ要素を解析します。

## 特徴

- **見出しとテキストの抽出**: HTML 要素のクラス名に基づいて、見出し (`smt_head1`, `smt_head2`) とテキスト (`smt_text`) を抽出し、構造化されたデータとして保存します。
- **数値が含まれるタイトルのフィルタリング**: タイトルに数値が含まれる項目のみをフィルタリングします。

## メソッド

### `smt_head`

`smt_head1` および `smt_head2` クラスの見出しと `smt_text` クラスのテキストを取得するメソッド。

#### 戻り値

- `self`: インスタンス自体を返します。

#### 使用例

```python
parser = QualitativeParser("path_to_xbrl_document.html")
parser.smt_head()
df_qualitative = parser.to_dataframe()

# 取得する DataFrame の例
# title (str): "Section 1"
# sub_title (str): "Subsection A"
# text (str): "This is the qualitative description."
```

## 使用方法

以下のように `QualitativeParser` クラスを使用して、XBRL ドキュメントから必要な情報を取得できます。

```python
from your_module import QualitativeParser

# XBRL ドキュメントのパスを指定してインスタンスを作成
parser = QualitativeParser("path_to_xbrl_document.html")

# 見出しとテキストを取得
parser.smt_head()
df_qualitative = parser.to_dataframe()
```

---
