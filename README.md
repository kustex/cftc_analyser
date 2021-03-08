# CFTC - Analyzer

## Overview

CFTC Analyzer is a tool to get 1 and 3 year z-scores for the major asset classes in the world. It is a indicator to be able to quantify the sentiment on the street. 

| Steps to get it working |
|---|---|
1. Download the repository
2. Go to https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm
3. Go to the header "Futures-and-Options Combined Reports", and download the latest 3 (or more) files.
4. Rename these zip-files to the corresponding year. For example: dea_com_xls_2021.zip -> 2021.zip
5. Copy these zip-files to the "data" folder inside the repository. 
6. Current directory to ~/PATH/cftcanalyzer/cftcanalyzer/
7. Run the cftcanalyzer.py file
8. Open metrics.html in your browser
