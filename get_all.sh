#!/bin/bash

cd ~/Documents/1-Areas/Recipes/nytcooking-scraper/
mkdir raw_html
cd raw_html
wget -i ../links.txt
for i in *; do mv $i ${i/\?*/.html}; done 
python3 as_md.py
mv md/*.md /Users/dustinknopoff/Library/Mobile\ Documents/com~apple~CloudDocs/MyStuff/Documents/1-Areas/Recipes/Recipes/NYT