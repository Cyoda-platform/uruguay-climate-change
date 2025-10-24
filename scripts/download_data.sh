#!/bin/bash

# Script to download climate data for Uruguay
# Customize this script based on your data sources

echo "Downloading climate data for Uruguay..."

# Create data directories if they don't exist
mkdir -p data/raw
mkdir -p data/external

# Example: Download data from a public API or repository
# Uncomment and modify the following lines based on your data source

# Example using wget:
# wget -O data/raw/climate_data.csv "https://example.com/uruguay_climate_data.csv"

# Example using curl:
# curl -o data/raw/temperature_data.json "https://api.example.com/temperature?country=uruguay"

# Example for multiple files:
# for year in {2000..2023}; do
#     wget -O "data/raw/climate_${year}.csv" "https://example.com/data/${year}.csv"
# done

echo "Data download complete!"
echo "Downloaded files are located in data/raw/"
