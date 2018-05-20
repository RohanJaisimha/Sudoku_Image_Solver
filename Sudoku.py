def makeGrid():
  print("Enter the grid:\n")
  grid=[]
  for i in range(9):
    grid.append([int(j) for j in input().split()])
  return grid

def findUnassignedSpace(grid):
  for i in range(len(grid)):
    for j in range(len(grid)):
      if(grid[i][j]==0):
        return i,j
  return -1,-1

def solve(grid):
  row,col=findUnassignedSpace()
  if(row==-1 and col==-1):
    return True
  for num in range(1,10):
    if(isSafe(row,col,num)):
      grid[row][col]=num
      if(solve()):
        return True
      grid[row][col]=0
  return False

def checkCol(grid,col,num):
  for i in range(len(grid)):
    if(grid[i][col]==num):
      return False
  return True

def checkRow(grid,row,num):
  for i in range(len(grid)):
    if(grid[row][i]==num):
      return False
  return True

def checkBox(grid,row,col,num):
  for i in range(row,row+3):
    for j in range(col,col+3):
      if(grid[i][j]==num):
        return False
  return True

def printGrid(grid):
  for i in range(len(grid)):
    if(i%3==0):
      print("+-------+-------+-------+")
    for j in range(len(grid)):
      if(j%3==0):
        print("|",end=" ")
      print(grid[i][j],end=" ")
      if(j==8):
        print("|")
  print("+-------+-------+-------+")

def isSafe(row,col,num):
  return checkCol(col,num) and checkRow(row,num) and checkBox(row//3*3,col//3*3,num)
             
def main():
  grid=makeGrid()
  if(solve(grid)):
    printGrid()
  else:
    print("Grid is not Solvable")

main()
  
