#!/bin/bash

apt-get update
apt-get install -y unzip wget

wget -O chrome.zip https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.68/linux64/chrome-linux64.zip
wget -O chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.68/linux64/chromedriver-linux64.zip

unzip chrome.zip -d chrome
unzip chromedriver.zip -d chromedriver_folder

chmod +x ./chromedriver_folder/chromedriver-linux64/chromedriver
chmod +x ./chrome/chrome-linux64/chrome

mv ./chromedriver_folder/chromedriver-linux64/chromedriver ./chromedriver

python app.py
