def makeGrid():
  print("Enter the grid:")
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
  row,col=findUnassignedSpace(grid)
  if(row==-1 and col==-1):
    return True
  for num in range(1,10):
    if(isSafe(grid,row,col,num)):
      grid[row][col]=num
      if(solve(grid)):
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
  print("\nThe solved grid is: ")
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

def isSafe(grid,row,col,num):
  return checkCol(grid,col,num) and checkRow(grid,row,num) and checkBox(grid,row//3*3,col//3*3,num)
             
def main():
  grid=makeGrid()
  if(solve(grid)):
    printGrid(grid)
  else:
    print("Grid is not Solvable")

main()
