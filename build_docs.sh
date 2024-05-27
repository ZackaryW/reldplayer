#!/bin/bash

# Array of supported languages
languages=("en" "zh_CN")

# Build directory
build_dir="_build"

# Clean previous builds
rm -rf $build_dir/*

# Build each language
for lang in "${languages[@]}"
do
    echo "Building documentation for language: $lang"
    sphinx-build -b html -D language=$lang docs/ $build_dir/html/$lang
done

echo "All documentation builds are complete."