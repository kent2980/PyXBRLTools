# PyXBRLToolsLogging

PyXBRLToolsLoggingは、PyXBRLToolsのためのロギングユーティリティです。

## 使い方

    ```python
    import logging
    from PyXBRLTools.py_xbrl_tools_logging import PyXBRLToolsLogging

    logger = PyXBRLToolsLogging(log_level=logging.DEBUG)
    logger.set_log_file('py_xbrl_tools.log')

    logger.logger.debug('This is a debug message')
    logger.logger.info('This is an info message')
    logger.logger.warning('This is a warning message')
    logger.logger.error('This is an error message')
    logger.logger.critical('This is a critical message')
    ```

## ライセンス

MIT
