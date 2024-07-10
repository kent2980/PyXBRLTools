import psycopg2


class PostgreSqlConnector:
    """PostgreSQL database コネクター"""

    def __init__(self, host, port, database, user, password):
        """コンストラクタ

        Args:
        host (str): ホスト名
        port (int): ポート番号
        database (str): データベース名
        user (str): ユーザー名
        password (str): パスワード

        Returns:
        PostgreSqlConnector: PostgreSQL database コネクター
        """
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        """データベースに接続

        Examples:
        >>> connector.connect()
        """
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
            )
            print("Connected to PostgreSQL database!")
        except (Exception, psycopg2.Error) as error:
            print(
                "Error while connecting to PostgreSQL database:",
                error,
            )

    def disconnect(self):
        """データベースから切断

        Examples:
        >>> connector.disconnect()
        """
        if self.connection:
            self.connection.close()
            print("Disconnected from PostgreSQL database.")

    def edit_table(self, table_name, column_name, new_value, condition):
        """テーブルのデータを更新

        Args:
        table_name (str): テーブル名
        column_name (str): カラム名
        new_value (str): 新しい値
        condition (str): 更新条件
        """
        try:
            cursor = self.connection.cursor()
            query = f"UPDATE {table_name}\
                    SET {column_name} = %s WHERE {condition}"
            cursor.execute(query, (new_value,))
            self.connection.commit()
            print("Table updated successfully!")
        except (Exception, psycopg2.Error) as error:
            print("Error while updating table:", error)
            self.connection.rollback()
        finally:
            if cursor:
                cursor.close()

    # 新規テーブルを作成する関数を追加
    def create_table(self, table_name, columns):
        """テーブルを作成

        Args:
        table_name (str): テーブル名
        columns (str): カラム
        """
        try:
            cursor = self.connection.cursor()
            query = f"CREATE TABLE {table_name} ({columns})"
            cursor.execute(query)
            self.connection.commit()
            print("Table created successfully!")
        except (Exception, psycopg2.Error) as error:
            print("Error while creating table:", error)
            self.connection.rollback()
        finally:
            if cursor:
                cursor.close()

    # テーブルに新規データを追加する関数を追加
    def add_data(self, table_name, columns, values):
        """テーブルにデータを追加

        Args:
        table_name (str): テーブル名
        columns (str): カラム
        values (str): 値

        Examples:
        >>> connector.add_data("your_table", "id, name", "1, 'John'")
        output: Data added successfully!
        """
        try:
            cursor = self.connection.cursor()
            query = (
                f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            )
            cursor.execute(query)
            self.connection.commit()
            print("Data added successfully!")
        except (Exception, psycopg2.Error) as error:
            print("Error while adding data:", error)
            self.connection.rollback()
        finally:
            if cursor:
                cursor.close()

    # データフレームからデータを追加する関数を追加
    def add_data_from_df(self, table_name, df):
        """データフレームからデータを追加

        Args:
        table_name (str): テーブル名
        df (pandas.DataFrame): データフレーム

        Examples:
        >>> connector.add_data_from_df("your_table", df)
        output: Data added successfully!
        """
        try:
            cursor = self.connection.cursor()
            for _, row in df.iterrows():
                query = f"INSERT INTO {table_name} ({', '.join(df.columns)})\
                    VALUES ({', '.join(['%s']*len(df.columns))})"
                cursor.execute(query, tuple(row))
            self.connection.commit()
            print("Data added successfully!")
        except (Exception, psycopg2.Error) as error:
            print("Error while adding data:", error)
            self.connection.rollback()
        finally:
            if cursor:
                cursor.close()

    # データフレームと同じデータ構造と型のテーブルを作成する関数を追加
    def create_table_from_df(self, table_name, df):
        """データフレームと同じデータ構造と型のテーブルを作成してデータを追加

        Args:
            table_name (str): テーブル名
            df (pandas.DataFrame): データフレーム

        Examples:
            >>> connector.create_table_from_df("your_table", df)
            output: Table created successfully!
        """
        try:
            cursor = self.connection.cursor()

            # Pandas dtype から PostgreSQL dtype へのマッピング
            dtype_mapping = {
                "int64": "BIGINT",
                "float64": "DOUBLE PRECISION",
                "bool": "BOOLEAN",
                # 'object' 通常は string を意味する
                "object": "TEXT",
                # 他の pandas dtype に対する変換もここに追加
                "string": "TEXT",
            }

            columns = ", ".join(
                [
                    (
                        f"{col} {dtype_mapping[str(df.dtypes[col])]}"
                        if str(df.dtypes[col]) in dtype_mapping
                        else f"{col} TEXT"
                    )  # マッピングがない場合はデフォルトで TEXT とする
                    for col in df.columns
                ]
            )

            query = f"CREATE TABLE {table_name} ({columns})"
            cursor.execute(query)
            self.connection.commit()
            print("Table created successfully!")
            self.add_data_from_df(table_name, df)
        except (Exception, psycopg2.Error) as error:
            print("Error while creating table:", error)
            self.connection.rollback()
        finally:
            if cursor:
                cursor.close()

    # 既存のテーブルに外部キー制約を追加する関数を追加
    def add_foreign_key(
        self, table_name, column_name, ref_table, ref_column
    ):
        """テーブルに外部キー制約を追加

        Args:
        table_name (str): テーブル名
        column_name (str): カラム名
        ref_table (str): 参照テーブル名
        ref_column (str): 参照カラム名

        """
        try:
            cursor = self.connection.cursor()
            query = f"ALTER TABLE {table_name} \
                ADD FOREIGN KEY ({column_name}) \
                    REFERENCES {ref_table}({ref_column})"
            cursor.execute(query)
            self.connection.commit()
            print("Foreign key added successfully!")
        except (Exception, psycopg2.Error) as error:
            print("Error while adding foreign key:", error)
            self.connection.rollback()
        finally:
            if cursor:
                cursor.close()

    def set_unique_key(self, table_name, column_names: list[str]):
        """テーブルに一意制約を追加

        Args:
        table_name (str): テーブル名
        column_names (list[str]): カラム名のリスト
        """
        try:
            cursor = self.connection.cursor()
            query = f"ALTER TABLE {table_name} \
                ADD UNIQUE ({', '.join(column_names)})"
            cursor.execute(query)
            self.connection.commit()
            print("Unique key added successfully!")
        except (Exception, psycopg2.Error) as error:
            print("Error while adding unique key:", error)
            self.connection.rollback()
        finally:
            if cursor:
                cursor.close()

    # テーブルが存在するか確認する関数を追加
    def is_exist_table(self, table_name):
        """テーブルが存在するか確認

        Args:
        table_name (str): テーブル名

        Returns:
        bool: テーブルが存在する場合は True、存在しない場合は False

        Examples:
        >>> connector.is_exist_table("your_table")
        """
        try:
            cursor = self.connection.cursor()
            query = f"SELECT EXISTS \
                (SELECT 1 FROM information_schema.tables \
                WHERE table_name = '{table_name}')"
            cursor.execute(query)
            return cursor.fetchone()[0]
        except (Exception, psycopg2.Error) as error:
            print("Error while checking table existence:", error)
        finally:
            if cursor:
                cursor.close()

    # データフレームからテーブルにデータを挿入する関数を追加、重複するデータがある場合は挿入しない
    def add_data_from_df_ignore_duplicate(self, table_name, df):
        """データフレームからデータを追加（重複するデータがある場合は挿入しない）

        Args:
        table_name (str): テーブル名
        df (pandas.DataFrame): データフレーム

        Examples:
        >>> connector.add_data_from_df_ignore_duplicate("your_table", df)
        output: Data added successfully!
        """
        try:
            cursor = self.connection.cursor()
            for _, row in df.iterrows():
                query = f"INSERT INTO {table_name} ({', '.join(df.columns)}) \
                    VALUES ({', '.join(['%s']*len(df.columns))}) \
                        ON CONFLICT DO NOTHING"
                cursor.execute(query, tuple(row))
            self.connection.commit()
            print("Data added successfully!")
        except (Exception, psycopg2.Error) as error:
            print("Error while adding data:", error)
            self.connection.rollback()
        finally:
            if cursor:
                cursor.close()
