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

    explicit TicTacToe(int size=3);
    TicTacToe(const TicTacToe &other);

    TicTacToe &operator=(const TicTacToe &other);

    std::vector<char> &operator[](int i);
    const std::vector<char> &operator[](int i) const;

    bool operator==(const TicTacToe &other) const;
    bool operator!=(const TicTacToe &other) const;

    [[nodiscard]] bool can_place(int i,int j) const;
    bool make_move(int i,int j);
    [[nodiscard]] bool check_win(char player) const;
    [[nodiscard]] bool is_draw() const;
    [[nodiscard]] bool check_line(int start_i, int start_j, int di, int dj, char player) const;
    [[nodiscard]] bool is_game_over() const;
    [[nodiscard]] char get_winner()const;

    friend std::ostream &operator <<(std::ostream &os,const TicTacToe &game);
    friend std::istream &operator >>(std::istream &is,TicTacToe &game);

    [[nodiscard]] char get_current_player() const;
    [[nodiscard]] int get_size() const;

    void reset();
};
#endif //TIC_TAC_TOE_H