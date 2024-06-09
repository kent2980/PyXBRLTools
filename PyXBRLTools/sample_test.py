from xbrl_manager.xbrl_download_manager import XBRLDownloadManager
from xbrl_manager.xbrl_path_manager import XbrlPathManager

if __name__ == '__main__':
    xbrl_dir_path = '/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData'
    xbrl_save_dir = '/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir'
    xbrl_path_manager = XbrlPathManager(xbrl_dir_path)

    xbrl_schema_paths = xbrl_path_manager.xsd_path
    for xbrl_schema_path in xbrl_schema_paths:
        xbrl_download_manager = XBRLDownloadManager(xbrl_schema_path['file_path'], xbrl_save_dir)
        local_path = xbrl_download_manager.get_xbrl_files()
        for path in local_path:
            print(path)
        print("****************************")
