
class XbrlRole:
    """
    EDINET タクソノミの各科目に対する表示名を設定する定数クラス。
    """

    # http://www.xbrl.org/2003/role/
    LABEL = "http://www.xbrl.org/2003/role/label"
    """標準ラベル: 標準に設定するラベル"""

    VERBOSE_LABEL = "http://www.xbrl.org/2003/role/verboseLabel"
    """冗長ラベル: 全ての要素で一意のラベル"""

    TOTAL_LABEL = "http://www.xbrl.org/2003/role/totalLabel"
    """合計ラベル: 合計を示すラベル（例：資産合計）"""

    PERIOD_START_LABEL = "http://www.xbrl.org/2003/role/periodStartLabel"
    """期首ラベル: 期首を表すラベル（例：現金及び現金同等物の期首残高）"""

    PERIOD_END_LABEL = "http://www.xbrl.org/2003/role/periodEndLabel"
    """期末ラベル: 期末を表すラベル（例：現金及び現金同等物の期末残高）"""

    NEGATIVE_LABEL = "http://www.xbrl.org/2003/role/negativeLabel"
    """負値ラベル: 負値のラベル（例：当期純損失（△））"""

    DOCUMENTATION = "http://www.xbrl.org/2003/role/documentation"
    """ドキュメンテーション: 要素に関する説明事項を記載するラベル"""

    # http://info.edinet-fsa.go.jp/jp/fr/gaap/role/
    POSITIVE_OR_NEGATIVE_LABEL = "http://info.edinet-fsa.go.jp/jp/fr/gaap/role/positiveOrNegativeLabel"
    """正値負値ラベル: 複数の期で正値と負値が混在することを表すラベル（例：当期純利益又は当期純損失（△））"""

# 具体的な業種識別子を使う例
class ManufacturingXbrlRole(XbrlRole):
    INDUSTRY_LABEL = "http://info.edinet-fsa.go.jp/jp/fr/gaap/manufacturing/role/label"
    INDUSTRY_VERBOSE_LABEL = "http://info.edinet-fsa.go.jp/jp/fr/gaap/manufacturing/role/verboseLabel"
    INDUSTRY_TOTAL_LABEL = "http://info.edinet-fsa.go.jp/jp/fr/gaap/manufacturing/role/totalLabel"
    INDUSTRY_NEGATIVE_LABEL = "http://info.edinet-fsa.go.jp/jp/fr/gaap/manufacturing/role/negativeLabel"
    INDUSTRY_DOCUMENTATION = "http://info.edinet-fsa.go.jp/jp/fr/gaap/manufacturing/role/documentation"