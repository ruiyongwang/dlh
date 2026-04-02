# IMA Note Search and Outline Generator
# This script searches IMA notes and generates outline/summary

param(
    [string]$Query = "商事调解",
    [switch]$Outline
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Read credentials
$configDir = "$env:USERPROFILE\.config\ima"
$clientId = Get-Content "$configDir\client_id" -Raw -ErrorAction SilentlyContinue
$apiKey = Get-Content "$configDir\api_key" -Raw -ErrorAction SilentlyContinue

if (-not $clientId) {
    Write-Host "Error: IMA credentials not found"
    exit 1
}

$clientId = $clientId.Trim()
$apiKey = $apiKey.Trim()

# Helper function for API calls
function Invoke-IMAApi {
    param([string]$Path, [hashtable]$Body)
    
    $json = $Body | ConvertTo-Json -Depth 10
    $utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
    
    $headers = @{
        "ima-openapi-clientid" = $clientId
        "ima-openapi-apikey" = $apiKey
    }
    
    try {
        $response = Invoke-RestMethod -Uri "https://ima.qq.com/$Path" `
            -Method Post `
            -Body $utf8Bytes `
            -ContentType "application/json; charset=utf-8" `
            -Headers $headers `
            -TimeoutSec 30
        
        return $response
    } catch {
        return $null
    }
}

# Search notes
$searchResult = Invoke-IMAApi -Path "openapi/note/v1/search_note_book" -Body @{
    search_type = 0
    query_info = @{ title = $Query }
    start = 0
    end = 20
}

if ($searchResult.code -eq 0 -and $searchResult.data.docs) {
    $notes = $searchResult.data.docs
    $totalCount = $searchResult.data.total_hit_num
    Write-Host "Found $totalCount notes matching: $Query"
    Write-Host "================================"
    
    $idx = 1
    foreach ($note in $notes) {
        $title = $note.doc.basic_info.title
        $docId = $note.doc.basic_info.docid
        $summary = $note.doc.basic_info.summary
        $createTime = $note.doc.basic_info.create_time
        
        if ($createTime -match "^\d+$") {
            $createDate = [DateTimeOffset]::FromUnixTimeMilliseconds([long]$createTime).DateTime.ToString("yyyy-MM-dd")
        } else {
            $createDate = $createTime
        }
        
        Write-Host "`n[$idx] $title"
        Write-Host "    ID: $docId | $createDate"
        
        if ($Outline -and $summary) {
            # Try to get full content first
            $contentResult = Invoke-IMAApi -Path "openapi/note/v1/get_doc_content" -Body @{
                doc_id = $docId
                target_content_format = 0
            }
            
            $text = $null
            
            if ($contentResult.code -eq 0 -and $contentResult.data.text) {
                $text = $contentResult.data.text -replace "`r`n", "`n"
            } elseif ($summary) {
                $text = $summary -replace " ", ""
            }
            
            if ($text) {
                # Generate outline
                $lines = $text -split "`n" | Where-Object { $_.Trim() -ne "" }
                $outlineItems = @()
                
                foreach ($line in $lines) {
                    $trimmed = $line.Trim()
                    if ($trimmed.Length -lt 60 -and $trimmed.Length -gt 2 -and (
                        $trimmed -match "^[一二三四五六七八九十\d]" -or
                        $trimmed -match "^第[一二三四五六七八九十\d]" -or
                        $trimmed -match "^[{|[]" -or
                        $trimmed -match "^[*\-]"
                    )) {
                        $outlineItems += $trimmed
                    }
                }
                
                if ($outlineItems.Count -gt 0) {
                    Write-Host "`n    --- Outline ---"
                    $uniqueOutline = $outlineItems | Select-Object -Unique | Select-Object -First 8
                    $oi = 1
                    foreach ($item in $uniqueOutline) {
                        Write-Host "    $oi. $item"
                        $oi++
                    }
                }
                
                # Preview
                if ($text.Length -gt 0) {
                    $preview = $text.Substring(0, [Math]::Min(300, $text.Length))
                    Write-Host "`n    --- Preview ---"
                    $previewLines = ($preview -split "[`n]" | Select-Object -First 3)
                    foreach ($line in $previewLines) {
                        if ($line.Trim()) {
                            $lineText = $line.Substring(0, [Math]::Min(80, $line.Length))
                            Write-Host "    $lineText"
                        }
                    }
                }
            }
        }
        $idx++
    }
} else {
    Write-Host "No notes found: $($Query)"
}
