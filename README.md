# AFL-Tracing

AFL-Tracing is the extension module of AFL that can work together with Symbolic Execution

### Installation

Install  some tools

```sh
$ sudo apt install python virtualenv git python-dev
```
Activate the virtual environment

```sh
$ mkdir afl-tracing
$ cd ~/afl-tracing
$ virtualenv venv
$ source venv/bin/activate
```

Install AFL
```sh
$ git clone https://github.com/mirrorer/afl
$ cd afl
$ make && sudo make install
```

Install Angr & Driller modules 
```sh
$ pip install git+https://github.com/angr/cle
$ pip install git+https://github.com/angr/angr
$ pip install git+https://github.com/angr/tracer
$ pip install git+https://github.com/shellphish/driller
```
### Running the Example Program
Usage : python run.py [binary] [fuzzer_input_dir] [fuzzer_output_dir]
```sh
$ gcc foo.c -o foo
$ mkdir test
$ echo 'start' > test/input/seed
$ python run.py ./foo test/input test/output
```
License
----

MIT

