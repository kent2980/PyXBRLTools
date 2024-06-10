# XbrlReader

`XbrlReader` は、XBRLファイルのZIPファイルを読み込み、iXBRLデータの非分数および非数値情報を取得するためのクラスです。

## 使用方法

### 初期化

`XbrlReader` クラスを使用する前に、XBRLファイルのZIPファイルパス、解凍ディレクトリパス、グローバルラベルファイルをロードするディレクトリパスを指定して初期化します。

```python
from xbrl_manager.xbrl_label_manager import XbrlLabelManager
from xbrl_manager.xbrl_link_manager import XbrlLinkManager, XbrlLinkType
from xbrl_manager.ixbrl_manager import IxbrlManager

xbrl_zip_path = '/path/to/your/xbrl.zip'
xbrl_directory_path = '/path/to/extract/directory'
load_label_directory = '/path/to/label/directory'

xbrl_reader = XbrlReader(xbrl_zip_path, xbrl_directory_path, load_label_directory)
```

### iXBRL 非分数情報の取得

iXBRLファイルの非分数情報を取得するには、`get_ix_non_fractions` メソッドを使用します。

```python
ix_non_fractions = xbrl_reader.get_ix_non_fractions()
for key, value in ix_non_fractions.items():
    print(f'{key}: {value}')
```

### iXBRL 非数値情報の取得

iXBRLファイルの非数値情報を取得するには、`get_ix_non_numerics` メソッドを使用します。

```python
ix_non_numerics = xbrl_reader.get_ix_non_numerics()
for key, value in ix_non_numerics.items():
    print(f'{key}: {value}')
```

## クラス

### XbrlReader

#### プロパティ

- `xbrl_zip_path`：XBRLファイルのZIPファイルのパス
- `xbrl_directory_path`：XBRLファイルを解凍するディレクトリのパス
- `load_label_directory`：グローバルラベルファイルをロードするディレクトリのパス

#### メソッド

- `get_ix_non_fractions()`: iXBRLファイルの非分数を取得するメソッド。辞書形式で返されます。
    - `ix_non_fractions`
    - `ix_non_fractions_label_arcs`
    - `ix_non_fractions_label_locs`
    - `ix_non_fractions_labels`
    - `ix_non_fractions_cal_link_locs`
    - `ix_non_fractions_cal_link_arcs`
    - `ix_non_fractions_def_link_locs`
    - `ix_non_fractions_def_link_arcs`
    - `ix_non_fractions_pre_link_locs`
    - `ix_non_fractions_pre_link_arcs`
- `get_ix_non_numerics()`: iXBRLファイルの非数値を取得するメソッド。辞書形式で返されます。
    - `ix_non_numerics`
    - `ix_non_numerics_label_arcs`
    - `ix_non_numerics_label_locs`
    - `ix_non_numerics_labels`

## ライセンス

このプロジェクトは MIT ライセンスの下でライセンスされています。詳細については、LICENSEファイルを参照してください。

---

このREADMEは、`XbrlReader`クラスの基本的な使い方と主要メソッドを簡潔に説明しています。必要に応じて、詳細な説明や追加の例を追加することもできます。