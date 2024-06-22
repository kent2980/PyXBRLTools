import zipfile
from pathlib import Path

if __name__ == "__main__":

    zip_dir = Path("/Users/user/Documents/tdnet/tdnet")
    # 再起的にzipファイルのリストを取得
    zip_files = [p for p in zip_dir.glob("**/*.zip") if p.is_file()]
    # zipファイルの中身のファイル名に"edjp"が含まれるファイルを取得
    doc_name = "edus"
    edjp_files = []
    for zip_file in zip_files:
        with zipfile.ZipFile(zip_file) as z:
            for name in z.namelist():
                if doc_name in name:
                    edjp_files.append(zip_file)
                    break

    # edjp_filesの最初のファイルを/Users/user/Vscode/python/PyXBRLTools/PyXBRLTools/tests/data/xbrl_zipにコピー
    if len(edjp_files) > 0:
        edjp_file = edjp_files[3]
        copy_path = Path("/Users/user/Vscode/python/PyXBRLTools/PyXBRLTools/tests/data/xbrl_zip")
        copy_path.mkdir(parents=True, exist_ok=True)
        edjp_file_name = edjp_file.name
        copy_path = copy_path / f'{doc_name}.zip'
        with open(copy_path, "wb") as f:
            with open(edjp_file, "rb") as f2:
                f.write(f2.read())
        print(f"copy_path: {copy_path}")
    else:
        print("No files found.")
