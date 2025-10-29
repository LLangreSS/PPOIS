#include "UnitTest++.h"
#include "../src/tic_tac_toe.h"
#include <sstream>
#include <stdexcept>
int main()
{
    return UnitTest::RunAllTests();
}
TEST(CreationAndBasicProperties) {
    TicTacToe game(3);

    CHECK_EQUAL(3, game.get_size());
    CHECK_EQUAL('X', game.get_current_player());

    TicTacToe game2(2);

    CHECK_EQUAL(2, game2.get_size());
    CHECK_THROW(TicTacToe game3(1), std::invalid_argument);
    CHECK_THROW(TicTacToe game4(0), std::invalid_argument);
    CHECK_THROW(TicTacToe game5(-1), std::invalid_argument);
}
TEST(CopyConstructorAndAssignment) {
    TicTacToe game1(3);
    game1[0][0] = 'X';
    game1[1][1] = 'O';

    TicTacToe game2(game1);
            CHECK_EQUAL(3, game2.get_size());
            CHECK(game1 == game2);

    TicTacToe game3(4);
    game3 = game1;

            CHECK(game1 == game3);
    game3 = game3;
            CHECK(game1 == game3);

    TicTacToe game4(3);
            CHECK(game1 != game4);
}
TEST(OperatorAccess) {
    TicTacToe game(3);

    game[0][0] = 'X';
    CHECK_EQUAL('X', game[0][0]);
    CHECK_EQUAL('-', game[1][1]);


    const TicTacToe& const_game = game;
    CHECK_EQUAL('X', const_game[0][0]);

    CHECK_THROW(game[-1][0], std::out_of_range);
    CHECK_THROW(game[3][0], std::out_of_range);

    CHECK_THROW(const_game[-1][0], std::out_of_range);
    CHECK_THROW(const_game[3][0], std::out_of_range);
}
TEST(CanPlaceMethod) {
    TicTacToe game(3);


            CHECK(game.can_place(0, 0));
            CHECK(game.can_place(1, 1));
            CHECK(game.can_place(2, 2));


    game[0][0] = 'X';
            CHECK(!game.can_place(0, 0));


            CHECK(!game.can_place(-1, 0));
            CHECK(!game.can_place(0, -1));
            CHECK(!game.can_place(3, 0));
            CHECK(!game.can_place(0, 3));
}
TEST(CheckLineMethod) {
    TicTacToe game(3);


    game[0][0] = 'X'; game[0][1] = 'X'; game[0][2] = 'X';
            CHECK(game.check_line(0, 0, 0, 1, 'X'));
            CHECK(!game.check_line(0, 0, 0, 1, 'O'));


    TicTacToe game2(3);
    game2[0][1] = 'O'; game2[1][1] = 'O'; game2[2][1] = 'O';
            CHECK(game2.check_line(0, 1, 1, 0, 'O'));


    TicTacToe game3(3);
    game3[0][0] = 'X'; game3[1][1] = 'X'; game3[2][2] = 'X';
            CHECK(game3.check_line(0, 0, 1, 1, 'X'));


    TicTacToe game4(3);
    game4[0][2] = 'O'; game4[1][1] = 'O'; game4[2][0] = 'O';
            CHECK(game4.check_line(0, 2, 1, -1, 'O'));
}
TEST(HorizontalWin) {

    TicTacToe game(3);
    game[0][0] = 'X'; game[0][1] = 'X'; game[0][2] = 'X';
            CHECK(game.check_win('X'));
            CHECK(!game.check_win('O'));


    TicTacToe game2(3);
    game2[1][0] = 'O'; game2[1][1] = 'O'; game2[1][2] = 'O';
            CHECK(game2.check_win('O'));


    TicTacToe game3(3);
    game3[2][0] = 'X'; game3[2][1] = 'X'; game3[2][2] = 'X';
            CHECK(game3.check_win('X'));
}
TEST(VerticalWin) {

    TicTacToe game(3);
    game[0][0] = 'X'; game[1][0] = 'X'; game[2][0] = 'X';
            CHECK(game.check_win('X'));


    TicTacToe game2(3);
    game2[0][1] = 'O'; game2[1][1] = 'O'; game2[2][1] = 'O';
            CHECK(game2.check_win('O'));


    TicTacToe game3(3);
    game3[0][2] = 'X'; game3[1][2] = 'X'; game3[2][2] = 'X';
            CHECK(game3.check_win('X'));
}
TEST(DiagonalWin) {

    TicTacToe game(3);
    game[0][0] = 'X'; game[1][1] = 'X'; game[2][2] = 'X';
            CHECK(game.check_win('X'));


    TicTacToe game2(3);
    game2[0][2] = 'O'; game2[1][1] = 'O'; game2[2][0] = 'O';
            CHECK(game2.check_win('O'));
}
TEST(NoWin) {
    TicTacToe game(3);

            CHECK(!game.check_win('X'));
            CHECK(!game.check_win('O'));


    game[0][0] = 'X'; game[1][1] = 'O';
            CHECK(!game.check_win('X'));
            CHECK(!game.check_win('O'));
}
TEST(IsDraw) {

    TicTacToe game(2);
    game[0][0] = 'X'; game[0][1] = '-';
    game[1][0] = 'O'; game[1][1] = 'X';
    CHECK(!game.is_draw());
    CHECK(game.check_win('X'));
    CHECK(!game.check_win('O'));


    TicTacToe game2(2);
    game2[0][0] = 'X';
            CHECK(!game2.is_draw());


    TicTacToe game3(2);
    game3[0][0] = 'X'; game3[0][1] = 'X';
    game3[1][0] = 'O'; game3[1][1] = '-';
            CHECK(!game3.is_draw());
}
TEST(OutputStreamOperator) {
    TicTacToe game(2);
    game[0][0] = 'X';
    game[1][1] = 'O';

    std::stringstream ss;
    ss << game;

    std::string output = ss.str();
    CHECK(output.find('X') != std::string::npos);
    CHECK(output.find('O') != std::string::npos);
    CHECK(output.find('-') != std::string::npos);
}
TEST(InputStreamOperator) {
    TicTacToe game(3);


    std::stringstream ss1("1 1");
    ss1 >> game;
            CHECK_EQUAL('O', game.get_current_player());
            CHECK_EQUAL('X', game[1][1]);


    std::stringstream ss2("1 1");
    ss2 >> game;
            CHECK(ss2.fail());


    std::stringstream ss3("5 5");
    ss3 >> game;
            CHECK(ss3.fail());
}
TEST(GameFlow) {
    TicTacToe game(3);


            CHECK_EQUAL('X', game.get_current_player());


    std::stringstream ss1("0 0");
    ss1 >> game;
            CHECK_EQUAL('O', game.get_current_player());
            CHECK_EQUAL('X', game[0][0]);


    std::stringstream ss2("0 1");
    ss2 >> game;
            CHECK_EQUAL('X', game.get_current_player());
            CHECK_EQUAL('O', game[0][1]);


    std::stringstream ss3("0 0");
    ss3 >> game;
            CHECK(ss3.fail());
            CHECK_EQUAL('X', game.get_current_player());
}
TEST(WinScenarios) {

    TicTacToe game(3);
    game[0][0] = 'X'; game[0][1] = 'X';

    std::stringstream ss("0 2");
    ss >> game;
            CHECK(game.check_win('X'));
            CHECK(!game.is_draw());


    TicTacToe game2(3);
    game2[0][1] = 'O'; game2[1][1] = 'O'; game2[2][1] = 'O';
            CHECK(game2.check_win('O'));
}
TEST(DifferentSizes) {

    TicTacToe game4(4);
            CHECK_EQUAL(4, game4.get_size());


    game4[2][0] = 'X'; game4[2][1] = 'X';
    game4[2][2] = 'X'; game4[2][3] = 'X';
            CHECK(game4.check_win('X'));


    TicTacToe game5(5);
            CHECK_EQUAL(5, game5.get_size());


    for(int i = 0; i < 5; i++) {
        game5[i][i] = 'O';
    }
            CHECK(game5.check_win('O'));
}
TEST(EdgeCases) {

    TicTacToe game(2);
            CHECK_EQUAL(2, game.get_size());


    game[0][0] = 'X'; game[0][1] = 'X';
            CHECK(game.check_win('X'));


    TicTacToe game2(2);
    game2[0][0] = 'X'; game2[0][1] = 'O';
    game2[1][0] = 'O'; game2[1][1] = '-';
    CHECK(!game2.is_draw());
}
TEST(MultipleOperations) {
    TicTacToe game(3);


    game[0][0] = 'X';
            CHECK(!game.can_place(0, 0));
            CHECK(game.can_place(0, 1));

    const TicTacToe game_copy = game;
            CHECK(game == game_copy);

    game[0][1] = 'O';
            CHECK(game != game_copy);
}
TEST(CurrentPlayerAfterWin) {
    TicTacToe game(3);


    game[0][0] = 'X'; game[0][1] = 'X';
    game[1][0] = 'O'; game[1][1] = 'O';


    std::stringstream ss("0 2");
    char player_before = game.get_current_player();
    ss >> game;


            CHECK(game.check_win('X'));
}
TEST(FullGameSimulation) {
    TicTacToe game(3);


    std::vector<std::pair<int, int>> moves = {
            {0,0}, {0,1}, {0,2}, {1,1}, {1,0}, {1,2}, {2,1}, {2,0}, {2,2}
    };

    for(const auto& move : moves) {
        if(!game.is_draw() && !game.check_win('X') && !game.check_win('O')) {
            std::stringstream ss;
            ss << move.first << " " << move.second;
            ss >> game;
        }
    }

            CHECK(game.is_draw());
}
TEST(TestEmptyBoardNoWin) {
    TicTacToe game(3);
            CHECK(!game.check_win('X'));
            CHECK(!game.check_win('O'));
            CHECK(!game.is_draw());
}
TEST(TestSingleMoveNoWin) {
    TicTacToe game(3);
    game[1][1] = 'X';
            CHECK(!game.check_win('X'));
            CHECK(!game.check_win('O'));
}
TEST(TestTwoMovesNoWin) {
    TicTacToe game(3);
    game[0][0] = 'X';
    game[1][1] = 'O';
            CHECK(!game.check_win('X'));
            CHECK(!game.check_win('O'));
}
TEST(TestAlmostWinHorizontal) {
    TicTacToe game(3);
    game[0][0] = 'X';
    game[0][1] = 'X';

    CHECK(!game.check_win('X'));
}
TEST(TestAlmostWinVertical) {
    TicTacToe game(3);
    game[0][1] = 'O';
    game[1][1] = 'O';

    CHECK(!game.check_win('O'));
}
TEST(TestAlmostWinDiagonal) {
    TicTacToe game(3);
    game[0][0] = 'X';
    game[1][1] = 'X';

    CHECK(!game.check_win('X'));
}
TEST(TestWinPreventsDraw) {
    TicTacToe game(3);
    game[0][0] = 'X'; game[0][1] = 'X'; game[0][2] = 'X';
            CHECK(!game.is_draw());
}
TEST(TestEmptyCellsPreventDraw) {
    TicTacToe game(3);
    game[0][0] = 'X';
            CHECK(!game.is_draw());
}
TEST(TestCanPlaceOnEmpty) {
    TicTacToe game(3);
            CHECK(game.can_place(0, 0));
            CHECK(game.can_place(2, 2));
            CHECK(game.can_place(1, 1));
}
TEST(TestCannotPlaceOnOccupied) {
    TicTacToe game(3);
    game[1][1] = 'X';
            CHECK(!game.can_place(1, 1));
}
TEST(TestCannotPlaceOutOfBounds) {
    TicTacToe game(3);
            CHECK(!game.can_place(-1, 0));
            CHECK(!game.can_place(3, 0));
            CHECK(!game.can_place(0, -1));
            CHECK(!game.can_place(0, 3));
}
TEST(TestPlayerSwitchAfterMove) {
    TicTacToe game(3);
    std::stringstream ss("0 0");
    ss >> game;
            CHECK_EQUAL('O', game.get_current_player());
}
TEST(TestNoPlayerSwitchAfterInvalidMove) {
    TicTacToe game(3);
    std::stringstream ss("0 0");
    ss >> game; // Valid move
    char player_after_first = game.get_current_player();

    std::stringstream ss2("0 0");
    ss2 >> game;
    CHECK_EQUAL(player_after_first, game.get_current_player());
}
TEST(TestInputFailureOnInvalidMove) {
    TicTacToe game(3);
    std::stringstream ss("0 0");
    ss >> game; // Valid move

    std::stringstream ss2("0 0");
            CHECK(!(ss2 >> game));
}
TEST(TestEqualitySameBoard) {
    TicTacToe game1(3);
    TicTacToe game2(3);
            CHECK(game1 == game2);
}
TEST(TestInequalityDifferentSize) {
    TicTacToe game1(3);
    TicTacToe game2(4);
            CHECK(game1 != game2);
}
TEST(TestInequalityDifferentContent) {
    TicTacToe game1(3);
    TicTacToe game2(3);
    game2[0][0] = 'X';
            CHECK(game1 != game2);
}