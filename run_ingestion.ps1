$chapters = 1..15
$raw_dir = "c:\Users\himkar vashistha\Desktop\RAG_system_NCERT\data\raw\pdfs"
New-Item -ItemType Directory -Force -Path $raw_dir | Out-Null

foreach ($ch in $chapters) {
    $ch_str = "{0:D2}" -f $ch
    $url = "https://ncert.nic.in/textbook/pdf/iesc1$ch_str.pdf"
    $file_path = Join-Path $raw_dir "iesc1$ch_str.pdf"
    
    if (-not (Test-Path $file_path)) {
        try {
            Invoke-WebRequest -Uri $url -OutFile $file_path -UseBasicParsing -ErrorAction Stop
            Write-Host "Downloaded Chapter $ch"
        } catch {
            Write-Host "Failed to download Chapter $ch"
        }
    } else {
        Write-Host "Chapter $ch already exists"
    }
}

cd "c:\Users\himkar vashistha\Desktop\RAG_system_NCERT"
& .\venv\Scripts\pip.exe install langchain-chroma
& .\venv\Scripts\python.exe src/ingestion/ingest_pipeline.py
