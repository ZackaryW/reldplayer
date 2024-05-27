# Array of supported languages
$languages = @("en", "zh_CN")

# Build directory
$build_dir = "_build"

# Clean previous builds
Remove-Item -Recurse -Force "$build_dir/*"

# Build each language
foreach ($lang in $languages) {
    Write-Host "Building documentation for language: $lang"
    sphinx-build -b html -D language=$lang docs/ "$build_dir/html/$lang"
}

Write-Host "All documentation builds are complete."