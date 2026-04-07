Add-Type -AssemblyName System.Drawing

function New-RoundedRectPath {
    param(
        [float]$X,
        [float]$Y,
        [float]$Width,
        [float]$Height,
        [float]$Radius
    )

    $path = New-Object System.Drawing.Drawing2D.GraphicsPath
    $d = $Radius * 2
    $path.AddArc($X, $Y, $d, $d, 180, 90)
    $path.AddArc($X + $Width - $d, $Y, $d, $d, 270, 90)
    $path.AddArc($X + $Width - $d, $Y + $Height - $d, $d, $d, 0, 90)
    $path.AddArc($X, $Y + $Height - $d, $d, $d, 90, 90)
    $path.CloseFigure()
    return $path
}

$width = 1280
$height = 640
$outputDir = Join-Path $PSScriptRoot "..\assets"
$outputPath = Join-Path $outputDir "social-preview-7deer.png"

if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

$bitmap = New-Object System.Drawing.Bitmap $width, $height
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit

$rect = New-Object System.Drawing.Rectangle 0, 0, $width, $height
$bgTop = [System.Drawing.Color]::FromArgb(255, 8, 16, 31)
$bgBottom = [System.Drawing.Color]::FromArgb(255, 26, 51, 89)
$gradient = New-Object System.Drawing.Drawing2D.LinearGradientBrush $rect, $bgTop, $bgBottom, 30
$graphics.FillRectangle($gradient, $rect)

$overlayBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(18, 255, 255, 255))
$linePen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(52, 128, 204, 255), 2)

for ($i = 0; $i -lt 8; $i++) {
    $x = 70 + ($i * 140)
    $y = 70 + (($i % 2) * 28)
    $graphics.FillEllipse($overlayBrush, $x, $y, 140, 140)
}

for ($i = 0; $i -lt 6; $i++) {
    $x1 = 170 + ($i * 150)
    $x2 = $x1 + 120
    $graphics.DrawLine($linePen, $x1, 110, $x2, 470)
}

$cardPath = New-RoundedRectPath -X 72 -Y 72 -Width 1136 -Height 496 -Radius 28
$cardBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(42, 5, 13, 28))
$cardPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(110, 112, 192, 255), 2)
$graphics.FillPath($cardBrush, $cardPath)
$graphics.DrawPath($cardPen, $cardPath)

$titleFont = New-Object System.Drawing.Font("Segoe UI", 42, [System.Drawing.FontStyle]::Bold)
$subtitleFont = New-Object System.Drawing.Font("Segoe UI", 20, [System.Drawing.FontStyle]::Regular)
$chipFont = New-Object System.Drawing.Font("Segoe UI", 16, [System.Drawing.FontStyle]::Bold)
$bodyFont = New-Object System.Drawing.Font("Segoe UI", 18, [System.Drawing.FontStyle]::Regular)
$smallFont = New-Object System.Drawing.Font("Segoe UI", 16, [System.Drawing.FontStyle]::Regular)

$whiteBrush = [System.Drawing.Brushes]::White
$accentBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255, 127, 214, 255))
$mutedBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255, 196, 221, 240))
$chipBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(48, 92, 165, 255))
$panelBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(72, 8, 18, 36))
$footerBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255, 173, 214, 255))

$graphics.DrawString("7Deer Skills", $titleFont, $whiteBrush, 112, 128)
$graphics.DrawString("Reusable skills for SEO automation, content pipelines, and AI agent workflows", $subtitleFont, $mutedBrush, 112, 200)

$chips = @("SEO automation", "content pipelines", "AI agents", "Next.js", "Python")
$chipX = 112
$chipY = 264
foreach ($chip in $chips) {
    $size = $graphics.MeasureString($chip, $chipFont)
    $chipWidth = [math]::Ceiling($size.Width + 32)
    $chipPath = New-RoundedRectPath -X $chipX -Y $chipY -Width $chipWidth -Height 40 -Radius 18
    $graphics.FillPath($chipBrush, $chipPath)
    $graphics.DrawString($chip, $chipFont, $whiteBrush, $chipX + 16, $chipY + 8)
    $chipPath.Dispose()
    $chipX += $chipWidth + 12
}

$items = @(
    "Google Trends -> SEO pages",
    "Game codes JSON -> Next.js page",
    "SKILL.md + scripts + templates"
)
$itemY = 352
foreach ($item in $items) {
    $graphics.FillEllipse($accentBrush, 120, $itemY + 8, 10, 10)
    $graphics.DrawString($item, $bodyFont, $whiteBrush, 144, $itemY)
    $itemY += 54
}

$panelPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(130, 102, 178, 255), 1.5)
$panelTitleFont = $chipFont
$panels = @(
    @{ X = 860; Y = 132; W = 250; H = 88; Title = "INPUT"; Text = "keywords, source data, workflow needs" },
    @{ X = 910; Y = 246; W = 220; H = 88; Title = "SKILL"; Text = "docs, scripts, references, templates" },
    @{ X = 860; Y = 360; W = 250; H = 88; Title = "OUTPUT"; Text = "pages, automation flows, reusable systems" }
)
foreach ($panel in $panels) {
    $path = New-RoundedRectPath -X $panel.X -Y $panel.Y -Width $panel.W -Height $panel.H -Radius 20
    $graphics.FillPath($panelBrush, $path)
    $graphics.DrawPath($panelPen, $path)
    $graphics.DrawString($panel.Title, $panelTitleFont, $accentBrush, $panel.X + 18, $panel.Y + 14)
    $graphics.DrawString($panel.Text, $smallFont, $whiteBrush, $panel.X + 18, $panel.Y + 44)
    $path.Dispose()
}

$arrowPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(190, 127, 214, 255), 3)
$arrowPen.EndCap = [System.Drawing.Drawing2D.LineCap]::ArrowAnchor
$graphics.DrawLine($arrowPen, 984, 220, 1024, 244)
$graphics.DrawLine($arrowPen, 1024, 334, 984, 358)

$graphics.DrawString("Open source repository", $bodyFont, $footerBrush, 112, 518)
$graphics.DrawString("github.com/kennyzir/7deer_skills", $bodyFont, $mutedBrush, 332, 518)

$bitmap.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)

$gradient.Dispose()
$overlayBrush.Dispose()
$linePen.Dispose()
$cardBrush.Dispose()
$cardPen.Dispose()
$titleFont.Dispose()
$subtitleFont.Dispose()
$chipFont.Dispose()
$bodyFont.Dispose()
$smallFont.Dispose()
$accentBrush.Dispose()
$mutedBrush.Dispose()
$chipBrush.Dispose()
$panelBrush.Dispose()
$panelPen.Dispose()
$footerBrush.Dispose()
$arrowPen.Dispose()
$cardPath.Dispose()
$graphics.Dispose()
$bitmap.Dispose()

Write-Output $outputPath
