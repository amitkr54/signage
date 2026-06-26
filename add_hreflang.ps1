$files = Get-ChildItem -Path "c:\Users\Admin\Downloads\signage-main (1)\signage-main" -Filter "*.html"

foreach ($file in $files) {
    $content = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)
    
    # Skip if already has hreflang
    if ($content -match "hreflang") {
        continue
    }

    $fileName = $file.Name
    if ($fileName -eq "index.html") {
        $url = "https://signageworks.in/"
    } else {
        $url = "https://signageworks.in/$fileName"
    }

    $hreflangTags = "`n`t<link rel=`"alternate`" hreflang=`"en-in`" href=`"$url`" />`n`t<link rel=`"alternate`" hreflang=`"x-default`" href=`"$url`" />`n</head>"
    
    $content = $content -replace "</head>", $hreflangTags
    [System.IO.File]::WriteAllText($file.FullName, $content, [System.Text.Encoding]::UTF8)
}

Write-Host "Hreflang tags injected into all HTML files!"
