@echo off
setlocal
python -m pip install -r requirements.txt
pyinstaller --noconfirm --onefile --name plc-monitor --windowed src/main.py
echo Ejecutable generado en dist\plc-monitor.exe
