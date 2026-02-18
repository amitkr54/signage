$path = "c:\Users\Admin\Downloads\signage-main\signage-main\door-nameplate-signage.html"
$content = Get-Content -Raw -Path $path
$svg = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#6b21a8" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 8px;"><polyline points="20 6 9 17 4 12"></polyline></svg>'
# This regex matches the entire img tag and its content
$old = '(?s)<img[^>]*?src="\.\./\.\./s\.w\.org/images/core/emoji/16\.0\.1/svg/2714\.svg"[^>]*?>'
$newContent = $content -replace $old, $svg
[System.IO.File]::WriteAllText($path, $newContent)
