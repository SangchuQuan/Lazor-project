# Lazor-project
This is the lazor project for EN 540.635 Software Carpentry
The goal of this project is to use python automatically solve the lazor game in ios or android, and output a txt file to show the solution.

## How to use
1. Download this 'laser.py' file and make sure that all bff files in the same folder.
2. Deside which puzzle you want to solve and run the python file to enter the file name of puzzle
3. You will get a txt file showing the solution automatically.

## Idea of our project:
Firstly, we need to read the bff files and extract the information we need. Our code will read bff files and creat a list to represent the layout of blocks. 
It will also store the information of lasers and other points for later use. Then it will calculate all possible arrangements of given blocks in given grid.
After that, the code will combine every information and simulate whether laser can pass all target points in one arrangement. When meeting the right arrangement, it will
recognize it and output a solution txt file.

##### Author: Honglin Shi hshi24@jh.edu, Sangchu Quan squan4@jh.edu
