#!/bin/bash

wget -O chrome.zip https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.68/linux64/chrome-linux64.zip
wget -O chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.68/linux64/chromedriver-linux64.zip

unzip chrome.zip -d chrome
unzip chromedriver.zip -d chromedriver_folder

mv chromedriver_folder/chromedriver-linux64/chromedriver ./chromedriver
chmod +x ./chromedriver
chmod +x ./chrome/chrome-linux64/chrome

export PATH=$PATH:$(pwd)/chrome/chrome-linux64:$(pwd)
python app.py
