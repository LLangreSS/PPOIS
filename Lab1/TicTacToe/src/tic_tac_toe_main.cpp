#include "tic_tac_toe.h"
#include <iostream>
int main()
{
    TicTacToe game(3);
    while(true)
    {
        std::cout<<"The current move is: "<<game.get_current_player()<<"\n";
        char currentPlayer=game.get_current_player();
        std::cin>>game;
        if (std::cin.fail()) {
            std::cin.clear();
            std::cin.ignore(10000, '\n');

            std::cout<<"No valid move\n";
            continue;
        }
        std::cout<<"\n"<<game;
        if (game.check_win(currentPlayer)) {
            std::cout << "The winner is: "<<currentPlayer<<"\n";
            break;
        }
        else if (game.is_draw()) {
            std::cout << "Draw!\n";
            break;
        }
    }
}