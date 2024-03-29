# Tic Tac Toe Game

This is a **tic tac toe** game made using **Python** with **PyGame** for the game structure and **Prolog** to define the behavior of the actor that plays the game along with the user.

## Dependencies
- *PyGame >= 2.1.2*
- *PySwip >= 0.2.10*
- *SwiProlog >= 8.4.2*

## Installing Dependencies

On Linux, the dependencies can be installed with the following commands:

```bash
sudo apt update
sudo apt install swi-prolog python3-pygame python3-pip
```

Some python libraries should also be installed before running the software, it is recommended that you install and configure [anaconda](https://docs.conda.io/projects/miniconda/en/latest/),
and create a virtual environment to install the following dependencies inside:

```
conda install -c conda-forge libstdcxx-ng
pip install git+https://github.com/yuce/pyswip@master#egg=pyswi
pip install pygame
```

If `pip install git+https://github.com/yuce/pyswip@master#egg=pyswi` did not work you can try using `pip install pyswip` instead.

## Executing the Program

After installing the dependencies (inside the conda env) execute the program with:

```bash
python3 main.py
```
### Basic Debugging

For basic debugging there exists two basic debug levels:

1. Describes each action suggested at each move of the player

```bash
DEBUG=1 python3 main.py
```

2. Describes eventual exceptions that occurred during the execution of the program (it also includes 1)

```bash
DEBUG=2 python3 main.py
```

## References
- Russell, Stuart, et, Norvig, Peter, "***Artificial Intelligence A Modern Approach***", 4th Edition
- Lalanda, Philippe, “***Two complementary patterns to build multi-expert systems***”, Thomson-CSF Corporate Research Laboratory
- [6. Search: Games, Minimax, and Alpha-Beta](https://www.youtube.com/watch?v=STjW3eH0Cik) by MIT OpenCourseWare on YouTube
- [Coding Tic Tac Toe in Python with Pygame](https://www.youtube.com/watch?v=q_Nzuyvf3tw) by Coder Space on YouTube
- Pilgrim, A. Robert, "***TIC-TAC-TOE: Introducing Expert Systems to Middle School Students***", Dept. of Computer Science and Information Systems, Murray State University
