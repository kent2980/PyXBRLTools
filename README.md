# XbrlReaderクラス

## 概要

`XbrlReader`クラスは、XBRLファイルを読み込み、必要なデータを抽出するためのクラスです。このクラスは、XBRLファイルを解凍し、iXBRLファイルの非分数や非数値データを取得する機能を提供します。

## 使用方法

### 初期化

```python
from xbrl_manager.xbrl_label_manager import XbrlLabelManager
from xbrl_manager.xbrl_link_manager import XbrlLinkManager, XbrlLinkType
from xbrl_manager.ixbrl_manager import IxbrlManager
import zipfile
import shutil
import os
import time
from db_connector.postgre_sql_connector import PostgreSqlConnector

# XBRLファイルのパスを指定
xbrl_zip_path = '/path/to/your/xbrl.zip'
xbrl_directory_path = '/path/to/extract/directory'
load_label_directory = '/path/to/label/directory'

# XbrlReaderのインスタンスを作成
xbrl_reader = XbrlReader(xbrl_zip_path, xbrl_directory_path, load_label_directory)
```

### 非分数データの取得

```python
# iXBRLファイルの非分数データを取得
ix_non_fractions = xbrl_reader.get_ix_non_fractions()

# 取得したデータを表示
for key, value in ix_non_fractions.items():
    print(f'{key}: {value}')
```

### 非数値データの取得

```python
# iXBRLファイルの非数値データを取得
ix_non_numerics = xbrl_reader.get_ix_non_numerics()

# 取得したデータを表示
for key, value in ix_non_numerics.items():
    print(f'{key}: {value}')
```

## クラス詳細

### コンストラクタ

```python
def __init__(self, xbrl_zip_path, xbrl_directory_path, load_label_directory):
```

- `xbrl_zip_path` (str): XBRLファイルのZIPファイルのパス
- `xbrl_directory_path` (str): XBRLファイルを解凍するディレクトリのパス
- `load_label_directory` (str): グローバルラベルファイルをロードするディレクトリのパス

### プロパティ

- `xbrl_zip_path` (str): XBRLファイルのZIPファイルのパスを取得
- `xbrl_directory_path` (str): XBRLファイルを解凍するディレクトリのパスを取得
- `load_label_directory` (str): グローバルラベルファイルをロードするディレクトリのパスを取得

### メソッド

#### `get_ix_non_fractions`

iXBRLファイルの非分数データを取得するメソッド。

```python
def get_ix_non_fractions(self):
```

- 戻り値: 非分数データを含む辞書

#### `get_ix_non_numerics`

iXBRLファイルの非数値データを取得するメソッド。

```python
def get_ix_non_numerics(self):
```

- 戻り値: 非数値データを含む辞書

## 使用例

```python
xbrl_zip_path = '/Users/user/Vscode/python/PyXBRLTools/doc/081220240327560965.zip'
xbrl_directory_path = '/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRL'
load_label_directory = '/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/labels'

xbrl_reader = XbrlReader(xbrl_zip_path, xbrl_directory_path, load_label_directory)

ix_non_fractions = xbrl_reader.get_ix_non_fractions()
for key, value in ix_non_fractions.items():
    print(f'{key}: {value}')

ix_non_numerics = xbrl_reader.get_ix_non_numerics()
for key, value in ix_non_numerics.items():
    print(f'{key}: {value}')
```

## 注意点

- 使用後は解凍したファイルが自動的に削除されます。
- 依存関係のライブラリが正しくインストールされていることを確認してください。