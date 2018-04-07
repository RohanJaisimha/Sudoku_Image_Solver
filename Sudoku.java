import java.io.*;
class Sudoku
{
    //returns the coordinates of an empty space on the grid
    int FindUnassigned(int grid[][])
    {
        int row,col=0;
        for(row=0;row<9;row++)
        {
            for(col=0;col<9;col++)
            {
                if(grid[row][col]==0)
                {
                    return row*10+col;
                }
            }
        }
        return -1;
    }
    
    //returns whether or not a column has num in it already
    boolean CheckCol(int grid[][],int col,int num)
    {
        for(int i=0;i<9;i++)
        {
            if(grid[i][col]==num)
                return false;
        }
        return true;
    }
    
    //returns whether or not a row has num in it already
    boolean CheckRow(int grid[][],int row,int num)
    {
        for(int i=0;i<9;i++)
        {
            if(grid[row][i]==num)
                return false;
        }
        return true;
    }
    
    //returns whether or not a box has num in it already
    boolean CheckBox(int grid[][],int row,int col,int num)
    {
        for(int i=row;i<row+3;i++)
        {
            for(int j=col;j<col+3;j++)
            {
                if(grid[i][j]==num)
                    return false;
            }
        }
        return true;
    }
    boolean CheckSafe(int grid[][],int row,int col,int num)
    {
        if(CheckCol(grid,col,num)==true && CheckRow(grid,row,num)==true && CheckBox(grid,row/3*3,col/3*3,num)==true)
            return true;
        return false;
    }
    
    //workhorse of the program; solves the puzzle using backtracking
    boolean Solve(int grid[][])
    {
        int a=FindUnassigned(grid);
        if(a==-1)
            return true;
        int row=a/10;
        int col=a%10;
        for(int i=1;i<=9;i++)
        {
            if(CheckSafe(grid,row,col,i)==true)
            {
                grid[row][col]=i;
                if(Solve(grid)==true)
                    return true;
                grid[row][col]=0;
            }
        }
        return false;
    } 
    
    //prints the grid in a fancy way
    void PrintGrid(int grid[][])
    {
        System.out.println("The solved grid is:-");
        System.out.println();
        for(int i=0;i<9;i++)
        {
            if(i%3==0)
            {
                System.out.print("+-------+-------+-------+");
                System.out.println();
            }
            for(int j=0;j<9;j++)
            {
                if(j%3==0)
                    System.out.print("| ");
                System.out.print(grid[i][j]+" ");
                if(j==8)
                    System.out.print("| ");
            }
            System.out.println();
        }
        System.out.print("+-------+-------+-------+");
    }       
    public static void main(String args[]) throws IOException
    {
        System.out.print("\f");
        BufferedReader buffy=new BufferedReader(new InputStreamReader(System.in));
        int grid[][]=new int [9][9];
        System.out.println("Enter the grid");
        String grid_in_chars[]=new String[9];
        for(int i=0;i<9;i++)
            grid_in_chars[i]=buffy.readLine();
            
        for(int i=0;i<9;i++)
        {
            int k=0;
            for(int j=0;j<9;j++)
            {
                grid[i][j]=grid_in_chars[i].charAt(k)-48;
                k+=2;
            }
        }       
        Sudoku s1=new Sudoku();
        if(s1.Solve(grid)==true)
            s1.PrintGrid(grid);
        else
            System.out.println("Grid cannot be solved");
    }
}
