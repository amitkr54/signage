$files = Get-ChildItem -Path "c:\Users\Admin\Downloads\signage-main (1)\signage-main" -Filter "*.html"

foreach ($file in $files) {
    $content = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)
    
    # Fix hreflang casing
    if ($content -match "hreflang=`"en-in`"") {
        $content = $content -replace "hreflang=`"en-in`"", "hreflang=`"en-IN`""
    }

    # Fix index.html title
    if ($file.Name -eq "index.html") {
        $content = $content -replace "<title>Signage Company in Delhi NCR, Gurgaon, LED Sign board Manufacturers</title>", "<title>Signage Company in Delhi NCR | Sign &amp; Display Solutions</title>"
    }

    [System.IO.File]::WriteAllText($file.FullName, $content, [System.Text.Encoding]::UTF8)
}

Write-Host "Fixed hreflang casing and title length!"
