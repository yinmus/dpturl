Write-Host "Start installation? [y/n]"
$start = Read-Host
if ($start -ne "y") { exit }

Write-Host "Install dependencies? (Linux only) [y/n]"
$deps = Read-Host
if ($deps -eq "y") {
    Write-Host "=DEBUG= Select distribution:"
    Write-Host "1. Arch/Manjaro"
    Write-Host "2. Debian/Ubuntu"
    $distro_choice = Read-Host "Enter number"

    if ($distro_choice -eq "1") {
        Write-Host "=DEBUG= Arch/Manjaro is not supported directly on Windows."
    } elseif ($distro_choice -eq "2") {
        Write-Host "=DEBUG= Installing for Debian/Ubuntu (via WSL)..."
        wsl sudo apt update
        wsl sudo apt install -y python3 python3-pip python3-requests python3-tqdm
    } else {
        Write-Host "=DEBUG= Invalid choice. Exiting."
        exit
    }
}

Write-Host "Create virtual environment? [y/n]"
$venv = Read-Host
if ($venv -eq "y") {
    python -m venv venv
    venv\Scripts\activate
    pip install --upgrade pip requests tqdm
    Write-Host "=DEBUG= Virtual environment ready."
}

Write-Host "Run script? [y/n]"
$run = Read-Host
if ($run -eq "y") { python dpturl.py -h }
