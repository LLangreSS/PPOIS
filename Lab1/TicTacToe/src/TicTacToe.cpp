#include "tic_tac_toe.h"
#include <iostream>

TicTacToe::TicTacToe(int size)
{
    if(size <= 1) throw std::invalid_argument("Size must be positive");
    this->size=size;
    this->board=std::vector<std::vector<char>>(size, std::vector<char>(size, '-'));
    this->current_player='X';
};
TicTacToe::TicTacToe(const TicTacToe &other)
{
    this->board=other.board;
    this->size=other.size;
    this->current_player=other.current_player;
}

TicTacToe &TicTacToe::operator=(const TicTacToe &other)
{
    if (this!=&other)
    {
        this->size=other.size;
        this->board=other.board;
        this->current_player=other.current_player;
    }
    return *this;
}

bool TicTacToe::operator==(const TicTacToe &other) const
{
    if(this->size!=other.size) return false;
    return (this->board==other.board);
}
bool TicTacToe::operator!=(const TicTacToe &other) const
{
    return !(*this==other);
}

std::vector<char> &TicTacToe::operator[](int i)
{
    if (i<0 || i>=size) throw std::out_of_range("Index out of range\n");
    return board[i];
}
const std::vector<char> &TicTacToe::operator[](int i) const
{
    if (i<0 || i>=size) throw std::out_of_range("Index out of range\n");
    return board[i];
}

char TicTacToe::get_current_player() const
{
    return current_player;
}

int TicTacToe::get_size() const
{
    return size;
}

bool TicTacToe::can_place(int i,int j) const
{
    return (i>=0 && i<size && j>=0 && j<size && board[i][j]=='-');
}
bool TicTacToe::check_line(int start_i, int start_j, int di, int dj, char player) const
{
    int i = start_i;
    int j = start_j;

    for(int step=0;step<size;step++)
    {
        if(board[i][j]!=player) return false;
        i+=di;
        j+=dj;
    }
    return true;
}
bool TicTacToe::check_win(char player) const
{
    for(int i = 0; i < size; i++)
    {
        if(check_line(i, 0, 0, 1, player)) return true;
    }
    for(int j = 0; j < size; j++)
    {
        if(check_line(0, j, 1, 0, player)) return true;
    }
    return check_line(0, 0, 1, 1, player) ||
           check_line(0, size-1, 1, -1, player);
}
bool TicTacToe::is_draw() const
{
    if(check_win(current_player)) return false;
    for(int i=0;i<size;i++)
    {
        for(int j=0;j<size;j++)
        {
         if(board[i][j]=='-') return false;
        }
    }
    return true;
}

std::ostream &operator<<(std::ostream &os,const TicTacToe &game)
{
    for(int i=0;i<game.size;i++)
    {
        for(int j=0;j<game.size;j++)
        {
            os<<game.board[i][j]<<"\t";
        }
        os<<"\n";
    }
    return os;
}
std::istream &operator>>(std::istream &is,TicTacToe &game)
{
     int i,j;
     is>>i>>j;
    if(!game.can_place(i,j))
    {
        is.setstate(std::ios::failbit);
        return is;
    }
     game.board[i][j]=game.current_player;
    if(!game.check_win(game.current_player) && !game.is_draw())
    {
        game.current_player = (game.current_player == 'X') ? 'O' : 'X';
    }
     return is;
}



