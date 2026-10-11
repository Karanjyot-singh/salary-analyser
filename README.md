# Salary Analyser

The salary analyser is a group project created by my fellow classmate and me.

## How to run

1. Download the files.
2. Open the command line terminal.
3. Go to the folder with the files:
```
   cd location name
```
4. Create the virtual environment:
```
   python -m venv venv
```
5. Activate it:
```
   venv\Scripts\activate
```
6. Install the packages:
```
   pip install streamlit numpy pandas
```
7. Run the app:
```
   streamlit run frontend.py
```
8. The analyser opens in the web browser.

## Cautions

- Download `analyser.py`, `db.py` and `frontend.py` and put them in the same folder.
- When Streamlit starts for the first time, it asks for an email. Ignore it and press Enter.
- To stop the analyser, press `Ctrl + C`.
- If you get a PowerShell error, run this and try again:
```
  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
