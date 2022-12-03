# Advent of Code

## Requirements

- GHC >= 8.0.2
- NASM >= 2.13.02
- Python >= 3.9

## Usage

Look at the headers of the request from e.g. your browser and grab the session
identifier from the `cookie` header (it looks like `Cookie: session=...`).
Invoke `./aoc token` on it with

~~~ console
$ ./aoc token <session>
~~~

This will store the token (in plain text) in `.token` within the current
working directory.

You can now automatically pull the input data for each day with the command

~~~ console
$ ./aoc pull <year> <day>
~~~

Before you can run the code you need to invoke `./aoc init` to create a
virtual environment for the Python code, with the `aoctk` package installed.
After this step you can run the code for a specific day with

~~~ console
$ ./aoc run <year> <day>
~~~
