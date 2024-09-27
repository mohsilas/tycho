<div align="center"><h1>Tycho</h1></div>

<br>
<div align="center">
  <img/ src="https://github.com/user-attachments/assets/b7ca8b8b-7840-4b1d-aa40-c081e15d3af2" height="25">&nbsp;&nbsp;
  <img/ src="https://github.com/user-attachments/assets/3cd1ab55-deda-4cdd-a21e-951d91bf3231" height="25">&nbsp;&nbsp;
  <img/ src="https://github.com/user-attachments/assets/c93b9d1f-920b-4191-99da-acc38466f8c2" height="25">&nbsp;&nbsp;
  <img/ src="https://github.com/user-attachments/assets/aaac5885-8d01-4b17-a778-e67a6d98d74b" height="25">
</div>
<br>

Tycho is a simple versioned backup script. once initialized inside a project's dir, it keeps versions of the project inside a .tyc folder.

## 🎠 Setup and Usage

* clone
```
git clone https://github.com/mohsilas/tycho
```

* create alias (python3 /../.py or python/../.py):
```
alias tycho="python3 /../tycho.py"
```

* commands

| command | function                                                             |
|---------|----------------------------------------------------------------------|
| init    | creates .tyc folder and log.json (backup tracker) |
| push    | asks from commit msg, then copies the current project files into .tyc/n (n is backup number)  |
| log     | show current backup versions in the .tyco dir                               |
| ignore  | add a file name to be ignored when backing up  (rules inside .tyc/log.json              |
| help    | show help                                                            |
