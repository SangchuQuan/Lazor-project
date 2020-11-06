# Lazor-project
This is the lazor project for EN 540.635 Software Carpentry
The goal of this project is to use python automatically solve the lazor game in ios or android, and output a txt file to show the solution.

## How to use
1. Download this 'laser.py' file and make sure that all bff files in the same folder.
2. Deside which puzzle you want to solve and manually change the filename in the "if __name__ == '__main__'" part
3. Run the python file and you will get a txt fill showing the solution

## Idea of our project:
Firstly, we need to read the bff files and extract the information we need. Our code will read bff files and creat a list to represent the layout of blocks. 
It will also store the information of lasers and other points for later use. Then it will calculate all possible arrangements of given blocks in given grid.
After that, the code will combine every information and simulate whether laser can pass all target points in one arrangement. When meeting the right arrangement, it will
recognize it and output a solution txt file.

##### Author: Honglin Shi, Sangchu Quan
