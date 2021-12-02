# Advent of Code

## Requirements

- GHC >= 8.0.2
- NASM >= 2.13.02
- Python >= 3.9

## How to get input data

Look at the headers of the request from e.g. your browser and grab the session
identifier from the `cookie` header (it looks like `Cookie: session=...`).
Export the variable `AOC_SESSION_ID` with the value you just grabbed and then
run

~~~ console
./aoc <year> <day>
~~~

to download the input for the specific day. This creates a sub-folder
`<year>/<day>`, with the `input.txt` file in it and a sample Python script
named `code.py`.