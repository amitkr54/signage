$files = Get-ChildItem -Path "c:\Users\Admin\Downloads\signage-main (1)\signage-main" -Filter "*.html"

$fbPixel = @"
<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '416473172091484');
fbq('track', 'PageView');
</script>
<!-- End Meta Pixel Code -->
</head>
"@

foreach ($file in $files) {
    $content = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)
    $modified = $false

    # 1. Inject FB Pixel if missing
    if ($content -notmatch "fbevents\.js") {
        $content = $content -replace "</head>", $fbPixel
        $modified = $true
    }

    # 2. Inject Facebook Link in footer if missing
    if ($content -notmatch "facebook\.com/signageworks") {
        $footerText = "All Rights Reserved"
        $newFooterText = 'All Rights Reserved | <a href="https://www.facebook.com/signageworks" target="_blank" rel="noopener" style="color:inherit; text-decoration:none;">Facebook</a>'
        $content = $content.Replace($footerText, $newFooterText)
        $modified = $true
    }

    if ($modified) {
        [System.IO.File]::WriteAllText($file.FullName, $content, [System.Text.Encoding]::UTF8)
    }
}

Write-Host "Facebook Pixel and Facebook Page Link injected into all HTML files!"
