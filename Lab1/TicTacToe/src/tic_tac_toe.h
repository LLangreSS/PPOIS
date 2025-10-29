#ifndef TIC_TAC_TOE_H
#define TIC_TAC_TOE_H
#include <vector>
#include <iosfwd>
class TicTacToe
{
private:
    char current_player;
    std::vector<std::vector<char>> board;
    int size;
public:

    TicTacToe(int size);
    TicTacToe(const TicTacToe &other);

    TicTacToe &operator=(const TicTacToe &other);

    std::vector<char> &operator[](int i);
    const std::vector<char> &operator[](int i) const;

    bool operator==(const TicTacToe &other) const;
    bool operator!=(const TicTacToe &other) const;

    bool can_place(int i,int j) const;

    bool check_win(char player) const;
    bool is_draw() const;
    bool check_line(int start_i, int start_j, int di, int dj, char player) const;

    friend std::ostream &operator <<(std::ostream &os,const TicTacToe &game);
    friend std::istream &operator >>(std::istream &is,TicTacToe &game);

    char get_current_player() const;

    int get_size() const;
};
#endif //TIC_TAC_TOE_H