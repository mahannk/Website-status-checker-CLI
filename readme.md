# Website Status Checker

## Getting started

Build a multithreads Python script with `concurrent.futures` for website status code checker

***Prerequisites***

```code
$ pip install -r requirements.txt
```

***Running the script***

```code
$ python status_check -i <inputFile.xlsx> -o [outputFile.xlsx] -t [read timeout]
```

### Bash Command Line Arguments:

```code
-i <input file.xlsx> - name of the input file (mandatory)
-o [output file.xlsx] – name of the output file (optional)
-t [time] – read timeout applied to creating a TCP request to the HTTP server [optional]
```

