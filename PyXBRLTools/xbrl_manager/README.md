# XBRLManagerモジュール

このモジュール群はディレクトリパスから、ファイル単体の解析クラスへ接続します。ディレクトリ内の全てのファイルを解析した結果を受け取り出力します。

# XbrlkPathManagerクラス

XbrlkPathManagerクラスは、Xbrlkアプリケーションのパス管理を担当するクラスです。

## 使用方法
ß
XbrlkPathManagerクラスを使用するには、以下の手順を実行します。

1. XbrlkPathManagerのインスタンスを作成します。

```python
from Xbrlkpathmanager import XbrlkPathManager

directory_path = "/user/doc/XBRLData"
path_manager = XbrlkPathManager(directory_path)
```

## サポートされているプロパティ

以下のがXbrlkPathManagerクラスでサポートされています。

```python
path_manager.ixbrl_path
```


## ライセンス

XbrlkPathManagerクラスはMITライセンスのもとで提供されています。
