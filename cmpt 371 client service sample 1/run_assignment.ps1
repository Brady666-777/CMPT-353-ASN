# CMPT 371 Network Programming Assignment - PowerShell Test Script
# This script runs all the network tests for the assignment

Write-Host "CMPT 371 - Client-Server Communication Assignment" -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Green

$pythonExe = "C:/Users/wohai/AppData/Local/Microsoft/WindowsApps/python3.11.exe"

Write-Host "`nRunning comprehensive network tests..." -ForegroundColor Yellow

# Run the main test suite
& $pythonExe "run_tests.py"

Write-Host "`n`nTest completed!" -ForegroundColor Green
Write-Host "For individual component testing:" -ForegroundColor Cyan
Write-Host "  - TCP Server: $pythonExe tcp_server.py" -ForegroundColor White
Write-Host "  - TCP Client: $pythonExe tcp_client.py" -ForegroundColor White  
Write-Host "  - UDP Server: $pythonExe udp_server.py" -ForegroundColor White
Write-Host "  - UDP Client: $pythonExe udp_client.py" -ForegroundColor White
Write-Host "  - Demo Mode:  $pythonExe demo.py" -ForegroundColor White

Read-Host "`nPress Enter to exit"
