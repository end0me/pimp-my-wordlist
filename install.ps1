# Windows PowerShell installation script for PMWL (Pimp My Wordlist)

# Function to display colored text
function Write-ColorText {
    param (
        [string]$Text,
        [string]$Color
    )
    
    Write-Host $Text -ForegroundColor $Color
}

function Show-Banner {
    Clear-Host
    Write-Host ""
    Write-ColorText "██████╗ ██╗███╗   ███╗██████╗     ███╗   ███╗██╗   ██╗    ██╗    ██╗ ██████╗ ██████╗ ██████╗ ██╗     ██╗███████╗████████╗" "Cyan"
    Write-ColorText "██╔══██╗██║████╗ ████║██╔══██╗    ████╗ ████║╚██╗ ██╔╝    ██║    ██║██╔═══██╗██╔══██╗██╔══██╗██║     ██║██╔════╝╚══██╔══╝" "Cyan"
    Write-ColorText "██████╔╝██║██╔████╔██║██████╔╝    ██╔████╔██║ ╚████╔╝     ██║ █╗ ██║██║   ██║██████╔╝██║  ██║██║     ██║███████╗   ██║   " "Cyan"
    Write-ColorText "██╔═══╝ ██║██║╚██╔╝██║██╔═══╝     ██║╚██╔╝██║  ╚██╔╝      ██║███╗██║██║   ██║██╔══██╗██║  ██║██║     ██║╚════██║   ██║   " "Cyan"
    Write-ColorText "██║     ██║██║ ╚═╝ ██║██║         ██║ ╚═╝ ██║   ██║       ╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝███████╗██║███████║   ██║   " "Cyan"
    Write-ColorText "╚═╝     ╚═╝╚═╝     ╚═╝╚═╝         ╚═╝     ╚═╝   ╚═╝        ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝╚══════╝   ╚═╝   " "Cyan"
    Write-Host ""
    Write-ColorText "                           [ Wordlist Generator for Penetration Testing ]" "Yellow"
    Write-Host ""
    Write-Host "-----------------------------------------------------------------------------------------"
    Write-Host ""
}

# Display banner
Show-Banner

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-ColorText "This script should be run as Administrator for the best experience." "Yellow"
    $runAsAdmin = Read-Host "Do you want to restart this script as Administrator? (Y/n)"
    if ($runAsAdmin -eq "" -or $runAsAdmin -eq "Y" -or $runAsAdmin -eq "y") {
        Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
        exit
    }
}

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    
    if ($pythonVersion -match "Python (\d+)\.(\d+)\.(\d+)") {
        $major = [int]$Matches[1]
        $minor = [int]$Matches[2]
        
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 6)) {
            Write-ColorText "Python 3.6 or higher is required. You have $pythonVersion" "Red"
            
            $installPython = Read-Host "Do you want to open the Python download page? (Y/n)"
            if ($installPython -eq "" -or $installPython -eq "Y" -or $installPython -eq "y") {
                Start-Process "https://www.python.org/downloads/"
            }
            exit 1
        }
        
        Write-ColorText "Python $pythonVersion detected." "Green"
    } else {
        throw "Python not installed"
    }
} catch {
    Write-ColorText "Python 3.6 or higher is not installed." "Red"
    
    $installPython = Read-Host "Do you want to open the Python download page? (Y/n)"
    if ($installPython -eq "" -or $installPython -eq "Y" -or $installPython -eq "y") {
        Start-Process "https://www.python.org/downloads/"
    }
    exit 1
}

# Check if pip is available
try {
    pip --version | Out-Null
    Write-ColorText "pip is installed." "Green"
} catch {
    Write-ColorText "pip is not installed or not in PATH." "Red"
    Write-ColorText "Please reinstall Python and make sure to check 'Add Python to PATH' during installation." "Yellow"
    exit 1
}

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Ask if user wants to install in virtual environment
$useVenv = Read-Host "Do you want to install in a virtual environment? (recommended) [Y/n]"
if ($useVenv -eq "" -or $useVenv -eq "Y" -or $useVenv -eq "y") {
    # Create and activate virtual environment
    Write-Host "Creating virtual environment..."
    
    # Check if venv module is available
    try {
        python -c "import venv" 2>&1 | Out-Null
    } catch {
        Write-ColorText "Python venv module not found. Make sure you have the full Python installation." "Red"
        exit 1
    }
    
    # Create virtual environment
    python -m venv "$scriptDir\venv"
    
    # Create activation script
    $activateScript = "$scriptDir\run.bat"
    "@echo off`r`n" | Out-File -FilePath $activateScript -Encoding ascii
    "call `"%~dp0venv\Scripts\activate.bat`"`r`n" | Out-File -FilePath $activateScript -Append -Encoding ascii
    "pmwl`r`n" | Out-File -FilePath $activateScript -Append -Encoding ascii
    "if %ERRORLEVEL% NEQ 0 pause`r`n" | Out-File -FilePath $activateScript -Append -Encoding ascii
    
    Write-ColorText "Virtual environment created." "Green"
    
    # Activate the virtual environment and install
    Write-Host "Installing Pimp My Wordlist in virtual environment..."
    & "$scriptDir\venv\Scripts\python.exe" -m pip install --upgrade pip
    & "$scriptDir\venv\Scripts\pip.exe" install -e "$scriptDir" --install-option="--platform=windows"
    & "$scriptDir\venv\Scripts\pip.exe" install pywin32 winshell
    
    # Create desktop shortcut
    $createShortcut = Read-Host "Do you want to create a desktop shortcut? (Y/n)"
    if ($createShortcut -eq "" -or $createShortcut -eq "Y" -or $createShortcut -eq "y") {
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\PMWL.lnk")
        $Shortcut.TargetPath = "$scriptDir\run.bat"
        $Shortcut.WorkingDirectory = $scriptDir
        $Shortcut.Description = "Custom wordlist generator for penetration testing"
        $Shortcut.IconLocation = "powershell.exe,0"
        $Shortcut.Save()
        
        Write-ColorText "Desktop shortcut created." "Green"
    }
    
    # Create Start Menu shortcut
    $createStartMenu = Read-Host "Do you want to create a Start Menu shortcut? (Y/n)"
    if ($createStartMenu -eq "" -or $createStartMenu -eq "Y" -or $createStartMenu -eq "y") {
        $startMenuPath = [System.IO.Path]::Combine($env:APPDATA, "Microsoft\Windows\Start Menu\Programs")
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut("$startMenuPath\PMWL.lnk")
        $Shortcut.TargetPath = "$scriptDir\run.bat"
        $Shortcut.WorkingDirectory = $scriptDir
        $Shortcut.Description = "Custom wordlist generator for penetration testing"
        $Shortcut.IconLocation = "powershell.exe,0"
        $Shortcut.Save()
        
        Write-ColorText "Start Menu shortcut created." "Green"
    }
    
    Write-ColorText "Installation complete! Run using the run.bat script or the created shortcuts." "Green"
} else {
    # Install globally
    Write-Host "Installing Pimp My Wordlist globally..."
    pip install -e "$scriptDir" --install-option="--platform=windows"
    pip install pywin32 winshell
    
    Write-ColorText "Installation complete! Run using: pimp-my-wordlist" "Green"
}

Write-Host ""
Write-ColorText "Thank you for installing Pimp My Wordlist!" "Yellow"
