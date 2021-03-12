# CFTC - Analyzer

## Overview

CFTC Analyzer is a tool to get 1 and 3 year z-scores for the major asset classes in the world. It is a indicator to be able to quantify the sentiment on the street. 

| Steps to get it working |
1. Clone the repository on your local device
2. Cd to the directory where the repo is located
3. Create new virtualenv or activate your virtualenv
4. Run: pip install -r requirements.txt in your shell
5. Go to https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm
6. Go to the header "Futures-and-Options Combined Reports", and download the latest 3 (or more) files
7. Rename these zip-files to the corresponding year. For example: dea_com_xls_2021.zip -> 2021.zip
8. Copy these zip-files to the "data" folder inside the repository
9. Current directory to ~/PATH/cftcanalyzer/cftcanalyzer/
10. Run the cftcanalyzer.py file
11. Open metrics.html in your browser
