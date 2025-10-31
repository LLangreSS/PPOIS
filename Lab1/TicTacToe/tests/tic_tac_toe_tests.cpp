#include "../../unittest-cpp/UnitTest++/UnitTest++.h"
#include "../src/tic_tac_toe.h"
#include <sstream>
#include <stdexcept>
int main()
{
    return UnitTest::RunAllTests();
}
SUITE(TicTacToeTests) {
    TEST(ConstructorInvalidSize) {
        CHECK_THROW(TicTacToe game(0), std::invalid_argument);
        CHECK_THROW(TicTacToe game(-1), std::invalid_argument);
        CHECK_THROW(TicTacToe game(1), std::invalid_argument);
    }

    TEST(ConstructorInitialState) {
        TicTacToe game(3);
                CHECK_EQUAL('X', game.get_current_player());
                CHECK_EQUAL(3, game.get_size());
        for (int i = 0; i < 3; ++i) {
            for (int j = 0; j < 3; ++j) {
                        CHECK_EQUAL('-', game[i][j]);
            }
        }
    }

    TEST(CopyConstructor) {
        TicTacToe game1(3);
        game1.make_move(0, 0);
        game1.make_move(1, 1);
        TicTacToe game2(game1);
                CHECK(game1 == game2);
                CHECK_EQUAL(game1.get_current_player(), game2.get_current_player());
    }

    TEST(AssignmentOperator) {
        TicTacToe game1(3);
        game1.make_move(0, 0);
        TicTacToe game2(4);
        game2 = game1;
                CHECK(game1 == game2);
                CHECK_EQUAL(3, game2.get_size());
    }

    TEST(SelfAssignment) {
        TicTacToe game(3);
        game.make_move(1, 1);
        game = game;
                CHECK_EQUAL('O', game.get_current_player());
                CHECK_EQUAL('X', game[1][1]);
    }

    TEST(EqualityOperator) {
        TicTacToe game1(3);
        TicTacToe game2(3);
                CHECK(game1 == game2);
        game1.make_move(0, 0);
                CHECK(game1 != game2);
    }

    TEST(InequalityOperator) {
        TicTacToe game1(3);
        TicTacToe game2(4);
                CHECK(game1 != game2);
    }

    TEST(OperatorAccessInvalid) {
        TicTacToe game(3);
                CHECK_THROW(game[-1], std::out_of_range);
                CHECK_THROW(game[3], std::out_of_range);
                CHECK_THROW(game[100], std::out_of_range);
    }

    TEST(CanPlaceValid) {
        TicTacToe game(3);
                CHECK(game.can_place(0, 0));
                CHECK(game.can_place(2, 2));
                CHECK(game.can_place(1, 1));
    }

    TEST(CanPlaceInvalid) {
        TicTacToe game(3);
                CHECK(!game.can_place(-1, 0));
                CHECK(!game.can_place(0, -1));
                CHECK(!game.can_place(3, 0));
                CHECK(!game.can_place(0, 3));
    }

    TEST(CanPlaceOccupied) {
        TicTacToe game(3);
        game.make_move(1, 1);
                CHECK(!game.can_place(1, 1));
    }

    TEST(MakeMoveValid) {
        TicTacToe game(3);
                CHECK(game.make_move(0, 0));
                CHECK_EQUAL('X', game[0][0]);
                CHECK_EQUAL('O', game.get_current_player());
    }

    TEST(MakeMoveInvalidPosition) {
        TicTacToe game(3);
                CHECK(!game.make_move(-1, 0));
                CHECK(!game.make_move(0, -1));
                CHECK(!game.make_move(3, 0));
                CHECK(!game.make_move(0, 3));
    }

    TEST(MakeMoveOccupied) {
        TicTacToe game(3);
        game.make_move(0, 0);
                CHECK(!game.make_move(0, 0));
    }

    TEST(MakeMoveAfterGameOver) {
        TicTacToe game(3);
        game.make_move(0, 0);
        game.make_move(1, 0);
        game.make_move(0, 1);
        game.make_move(1, 1);
        game.make_move(0, 2);
                CHECK(!game.make_move(2, 2));
    }

    TEST(CheckLineHorizontal) {
        TicTacToe game(3);
        game.make_move(0, 0);
        game.make_move(1, 0);
        game.make_move(0, 1);
        game.make_move(1, 1);
        game.make_move(0, 2);
                CHECK(game.check_win('X'));
    }

    TEST(CheckLineVertical) {
        TicTacToe game(3);
        game.make_move(0, 0);
        game.make_move(0, 1);
        game.make_move(1, 0);
        game.make_move(1, 1);
        game.make_move(2, 0);
                CHECK(game.check_win('X'));
    }

    TEST(CheckLineDiagonal) {
        TicTacToe game(3);
        game.make_move(0, 0);
        game.make_move(0, 1);
        game.make_move(1, 1);
        game.make_move(0, 2);
        game.make_move(2, 2);
                CHECK(game.check_win('X'));
    }

    TEST(CheckLineAntiDiagonal) {
        TicTacToe game(3);
        game.make_move(0, 2);
        game.make_move(0, 0);
        game.make_move(1, 1);
        game.make_move(0, 1);
        game.make_move(2, 0);
                CHECK(game.check_win('X'));
    }

    TEST(CheckLineNoWin) {
        TicTacToe game(3);
        game.make_move(0, 0);
        game.make_move(1, 1);
                CHECK(!game.check_win('X'));
                CHECK(!game.check_win('O'));
    }

    TEST(IsDrawTrue) {
        TicTacToe game(3);
        game.make_move(0, 0);
        game.make_move(0, 1);
        game.make_move(0, 2);
        game.make_move(1, 0);
        game.make_move(1, 2);
        game.make_move(1, 1);
        game.make_move(2, 0);
        game.make_move(2, 2);
        game.make_move(2, 1);
                CHECK(game.is_draw());
    }

    TEST(IsDrawFalseWithWin) {
        TicTacToe game(3);
        game.make_move(0, 0);
        game.make_move(1, 0);
        game.make_move(0, 1);
        game.make_move(1, 1);
        game.make_move(0, 2);
                CHECK(!game.is_draw());
    }

    TEST(IsDrawFalseWithEmpty) {
        TicTacToe game(3);
        game.make_move(0, 0);
                CHECK(!game.is_draw());
    }

    TEST(IsGameOverWin) {
        TicTacToe game(3);
        game.make_move(0, 0);
        game.make_move(1, 0);
        game.make_move(0, 1);
        game.make_move(1, 1);
        game.make_move(0, 2);
                CHECK(game.is_game_over());
    }

    TEST(IsGameOverDraw) {
        TicTacToe game(3);
        std::vector<std::pair<int, int>> moves = {
                {0,0}, {0,1}, {0,2},
                {1,0}, {1,2}, {1,1},
                {2,0}, {2,2}, {2,1}
        };
        for (auto move : moves) {
            game.make_move(move.first, move.second);
        }
                CHECK(game.is_game_over());
    }

    TEST(IsGameOverFalse) {
        TicTacToe game(3);
                CHECK(!game.is_game_over());
        game.make_move(0, 0);
                CHECK(!game.is_game_over());
    }

    TEST(GetWinnerX) {
        TicTacToe game(3);
        game.make_move(0, 0);
        game.make_move(1, 0);
        game.make_move(0, 1);
        game.make_move(1, 1);
        game.make_move(0, 2);
                CHECK_EQUAL('X', game.get_winner());
    }

    TEST(GetWinnerO) {
        TicTacToe game(3);
        game.make_move(0, 0);
        game.make_move(1, 0);
        game.make_move(0, 1);
        game.make_move(1, 1);
        game.make_move(2, 2);
        game.make_move(1, 2);
                CHECK_EQUAL('O', game.get_winner());
    }

    TEST(GetWinnerDraw) {
        TicTacToe game(3);
        std::vector<std::pair<int, int>> moves = {
                {0,0}, {0,1}, {0,2},
                {1,0}, {1,2}, {1,1},
                {2,0}, {2,2}, {2,1}
        };
        for (auto move : moves) {
            game.make_move(move.first, move.second);
        }
                CHECK_EQUAL('-', game.get_winner());
    }

    TEST(GetWinnerInProgress) {
        TicTacToe game(3);
                CHECK_EQUAL(' ', game.get_winner());
        game.make_move(0, 0);
                CHECK_EQUAL(' ', game.get_winner());
    }

    TEST(OutputStreamOperator) {
        TicTacToe game(3);
        game.make_move(0, 0);
        game.make_move(1, 1);
        std::ostringstream oss;
        oss << game;
        std::string output = oss.str();
                CHECK(output.find('X') != std::string::npos);
                CHECK(output.find('O') != std::string::npos);
                CHECK(output.find('-') != std::string::npos);
    }

    TEST(InputStreamOperatorInvalid) {
        TicTacToe game(3);
        std::istringstream iss("5 5");
        iss >> game;
                CHECK(iss.fail());
                CHECK_EQUAL('X', game.get_current_player());
    }

    TEST(ResetGame) {
        TicTacToe game(3);
        game.make_move(0, 0);
        game.make_move(1, 1);
        game.reset();
                CHECK_EQUAL('X', game.get_current_player());
        for (int i = 0; i < 3; ++i) {
            for (int j = 0; j < 3; ++j) {
                        CHECK_EQUAL('-', game[i][j]);
            }
        }
    }

    TEST(LargeBoardWin) {
        TicTacToe game(5);
        for (int i = 0; i < 5; ++i) {
            game.make_move(i, i);
            if (i < 4) {
                game.make_move(i, i + 1);
            }
        }
                CHECK(game.check_win('X'));
    }

    TEST(PlayerSwitchAfterMove) {
        TicTacToe game(3);
                CHECK_EQUAL('X', game.get_current_player());
        game.make_move(0, 0);
                CHECK_EQUAL('O', game.get_current_player());
        game.make_move(1, 1);
                CHECK_EQUAL('X', game.get_current_player());
    }

    TEST(NoPlayerSwitchAfterWin) {
        TicTacToe game(3);
        game.make_move(0, 0);
        game.make_move(1, 0);
        game.make_move(0, 1);
        game.make_move(1, 1);
        game.make_move(0, 2);
                CHECK_EQUAL('X', game.get_current_player());
    }

    TEST(MultipleMovesSequence) {
        TicTacToe game(3);
                CHECK(game.make_move(0, 0));
                CHECK(game.make_move(1, 1));
                CHECK(game.make_move(2, 2));
                CHECK_EQUAL('X', game[0][0]);
                CHECK_EQUAL('O', game[1][1]);
                CHECK_EQUAL('X', game[2][2]);
    }

    TEST(GetSize) {
        TicTacToe game3(3);
        TicTacToe game5(5);
                CHECK_EQUAL(3, game3.get_size());
                CHECK_EQUAL(5, game5.get_size());
    }
}
