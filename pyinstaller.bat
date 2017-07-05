pyinstaller.exe --onedir --noconsole ^
    --add-data="./networkdetective/resources;./networkdetective/resources" ^
    --icon="./networkdetective/resources/app_icon.ico" ^
    --name="NetworkDetective" ^
    ./networkdetective/main.py
