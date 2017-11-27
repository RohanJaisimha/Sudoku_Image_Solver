#include<iostream>
using namespace std;
int FindUnassigned(int grid[][9])
{
	for(int row=0;row<9;row++)
		for(int col=0;col<9;col++)
			if(grid[row][col]==0)
				return row*10+col;
	return -1;
}
bool CheckBox(int grid[][9],int row,int col,int num)
{
	for(int i=row;i<row+3;i++)
		for(int j=col;j<col+3;j++)
			if(grid[i][j]==num)
				return false;
	return true;
}
bool CheckCol(int grid[][9],int col,int num)
{
	for(int i=0;i<9;i++)
		if(grid[i][col]==num)
			return false;
	return true;
}
bool CheckRow(int grid[][9],int row,int num)
{
	for(int i=0;i<9;i++)
		if(grid[row][i]==num)
			return false;
	return true;
}
bool CheckSafe(int grid[][9],int row,int col,int num)
{
	return (CheckBox(grid,row/3*3,col/3*3,num) && CheckCol(grid,col,num) && CheckRow(grid,row,num));
}
bool Solve(int grid[][9])
{
	int UnassignedCoordinates=FindUnassigned(grid);
	if(UnassignedCoordinates==-1)
		return true;
	int row=UnassignedCoordinates/10,col=UnassignedCoordinates%10;
	for(int i=1;i<=9;i++)
	{
		if(CheckSafe(grid,row,col,i))
		{
			grid[row][col]=i;
			if(Solve(grid))
				return true;
			grid[row][col]=0;
		}
	}
	return false;
}
void PrintGrid(int grid[][9])
{
	cout<<"\nThe solved grid is:\n\n";
	for(int i=0;i<9;i++)
	{
		if(i%3==0)
			cout<<"+-------+-------+-------+\n";
		for(int j=0;j<9;j++)
		{
			if(j%3==0)
				cout<<"| ";
			cout<<grid[i][j]<<" ";
			if(j==8)
				cout<<"| ";
		}
		cout<<"\n";
	}
	cout<<"+-------+-------+-------+\n";
}
int main()
{
	int grid[9][9];
	re_enter:
		cout<<"Enter the grid(Blank Spaces ====> '0')\n";
		for(int i=0;i<9;i++)
		{
			for(int j=0;j<9;j++)
			{
				cin>>grid[i][j];
				if(grid[i][j]<0 || grid[i][j]>9)
				{
					cout<<"Error:Invalid number\n";
					goto re_enter;
				}
			}
		}	
	if(Solve(grid)==false)
	{
		cout<<"Error:Grid  is unsolvable\n";
		return 0;
	}
	PrintGrid(grid);
	return 0;
}	
