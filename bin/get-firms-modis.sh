#!/bin/env bash
cd ~/data/fire
# NRT download token:
token=bXN0cmFobDpiV2xyYTI4dWMzUnlZV2hzWlc1a2IzSm1aa0JtYldrdVptaz06MTYyNjc3MzA4MDowNWNkYzJiNGYwZjk1ODY2ZTViMzVkOTBkZGFlOTZhZWVhZjM0MmVh
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=7 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/FIRMS/modis-c6.1/Europe" --header "Authorization: Bearer $token" -P .
