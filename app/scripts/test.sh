#!/bin/bash

# 引数を受け取る
# 引数がない場合は、デフォルト値を設定
if [ $# -eq 0 ]; then
    echo "No arguments supplied. Using default values."
    # デフォルト値
    TEST_PATH=""
else
    TEST_PATH=tests/$1/
fi

# Step 1: Run pytest with coverage
coverage run -m pytest $TEST_PATH

# Step 2: Generate HTML coverage report
coverage html

# Step 3: Report the coverage summary
coverage report -m

# Step 3: Open the HTML report in the default web browser
# The report is generated in the 'htmlcov' directory
# if [ -f htmlcov/index.html ]; then
    # open htmlcov/index.html  # macOS
    # xdg-open htmlcov/index.html  # Linux
    # start htmlcov/index.html  # Windows
# else
    # echo "Coverage report not found."
# fi
