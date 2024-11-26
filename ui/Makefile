.PHONY: build zip

build:
	pyinstaller --clean --onefile --windowed --upx-dir "D:\upx" --distpath . -i favicon.ico ui.py

zip:
	zip ui.zip ui.exe favicon.ico cookies.txt
