#!/bin/bash

# Array of supported languages
languages=("en" "zh_CN")

defaultLang="en"

# Build directory
build_dir="_build"

# Run sphinx-build gettext
sphinx-build -b gettext docs/ "$build_dir/gettext"

for lang in "${languages[@]}"; do
    if [ "$lang" == "$defaultLang" ]; then
        continue
    fi
    # Create intl
    sphinx-intl update -p "$build_dir/gettext" -l $lang
done

# Confirm prompt
read -p "Press any key to continue"

# Clean previous builds
rm -rf "$build_dir/*"

# Build each language
for lang in "${languages[@]}"; do
    echo "Building documentation for language: $lang"
    sphinx-build -b html -D language=$lang docs/ "$build_dir/html/$lang"
done

echo "All documentation builds are complete."
