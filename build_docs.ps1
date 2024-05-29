# Array of supported languages
$languages = @("en", "zh_CN")

$defaultLang = "en"

# Build directory
$build_dir = "_build"

# run sphinx-build gettext
sphinx-build -b gettext docs/ "$build_dir/gettext"

foreach ($lang in $languages) {
    if ($lang -eq $defaultLang) {
        continue
    }
    # create intl
    sphinx-intl update -p "$build_dir/gettext" -l $lang
}
# confirm prompt
Read-Host -Prompt "Press any key to continue"

# Clean previous builds
Remove-Item -Recurse -Force "$build_dir/*"

# Build each language
foreach ($lang in $languages) {
    Write-Host "Building documentation for language: $lang"
    sphinx-build -b html -D language=$lang docs/ "$build_dir/html/$lang"
}

Write-Host "All documentation builds are complete."