# Simple PowerShell Web Server
$port = 8000
$url = "http://localhost:$port/"

# Create HTTP listener
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add($url)
$listener.Start()

Write-Host "Server running at $url" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow

try {
    while ($listener.IsListening) {
        # Wait for request
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response
        
        # Get requested file path
        $localPath = $request.Url.LocalPath
        if ($localPath -eq "/") { $localPath = "/index.html" }
        
        # Remove leading slash and get full path
        $filePath = Join-Path $PWD $localPath.TrimStart('/')
        
        Write-Host "Request: $localPath -> $filePath" -ForegroundColor Cyan
        
        try {
            if (Test-Path $filePath -PathType Leaf) {
                # File exists, serve it
                $content = [System.IO.File]::ReadAllBytes($filePath)
                $response.ContentLength64 = $content.Length
                
                # Set content type
                $extension = [System.IO.Path]::GetExtension($filePath).ToLower()
                switch ($extension) {
                    ".html" { $response.ContentType = "text/html" }
                    ".js" { $response.ContentType = "application/javascript" }
                    ".css" { $response.ContentType = "text/css" }
                    ".json" { $response.ContentType = "application/json" }
                    ".png" { $response.ContentType = "image/png" }
                    ".jpg" { $response.ContentType = "image/jpeg" }
                    default { $response.ContentType = "text/plain" }
                }
                
                $response.OutputStream.Write($content, 0, $content.Length)
                Write-Host "Served: $localPath" -ForegroundColor Green
            } else {
                # File not found
                $response.StatusCode = 404
                $errorMsg = "File not found: $localPath"
                $errorBytes = [System.Text.Encoding]::UTF8.GetBytes($errorMsg)
                $response.ContentLength64 = $errorBytes.Length
                $response.OutputStream.Write($errorBytes, 0, $errorBytes.Length)
                Write-Host "404: $localPath" -ForegroundColor Red
            }
        } catch {
            $response.StatusCode = 500
            $errorMsg = "Server error: $($_.Exception.Message)"
            $errorBytes = [System.Text.Encoding]::UTF8.GetBytes($errorMsg)
            $response.ContentLength64 = $errorBytes.Length
            $response.OutputStream.Write($errorBytes, 0, $errorBytes.Length)
            Write-Host "500: $($_.Exception.Message)" -ForegroundColor Red
        } finally {
            $response.Close()
        }
    }
} finally {
    $listener.Stop()
    Write-Host "Server stopped" -ForegroundColor Yellow
}
