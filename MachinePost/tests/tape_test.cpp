#include "UnitTest++.h"
#include "../src/machine_post.h"
#include <sstream>
#include <fstream>
#include <string>
#include <cstdio>
int main()
{
    return UnitTest::RunAllTests();
}
SUITE(TapeTests) {
    TEST(WriteCell_FalseErases) {
        Tape t;
        t.set_cell(5, true);
        t.write_cell(false);
                CHECK_EQUAL(true, t.get_cell(5));

        t.set_position(5);
        t.write_cell(false);
                CHECK_EQUAL(false, t.get_cell(5));
    }

    TEST(Print_SingleCellAtZero) {
        std::ostringstream oss;
        std::streambuf* old = std::cout.rdbuf(oss.rdbuf());
        Tape t;
        t.set_cell(0, true);
        t.print(0);
        std::cout.rdbuf(old);
        std::string out = oss.str();
                CHECK(out.find("[1]") != std::string::npos);
    }

    TEST(Print_NegativePositions) {
        std::ostringstream oss;
        std::streambuf* old = std::cout.rdbuf(oss.rdbuf());
        Tape t;
        t.set_cell(-2, true);
        t.set_cell(-1, false);
        t.print(-1);
        std::cout.rdbuf(old);
        std::string out = oss.str();
                CHECK(out.find("[0]") != std::string::npos);
                CHECK(out.find("1") != std::string::npos);
    }

    TEST(Print_HeadOutsideCellRange) {
        std::ostringstream oss;
        std::streambuf* old = std::cout.rdbuf(oss.rdbuf());
        Tape t;
        t.set_cell(10, true);
        t.print(0); // головка в 0, ячейки только в 10
        std::cout.rdbuf(old);
        std::string out = oss.str();
        // Должно напечатать [0] для позиции 0 и 1 для позиции 10
                CHECK(out.find("[0]") != std::string::npos);
                CHECK(out.find("1") != std::string::npos);
    }

    TEST(DefaultConstructor) {
        Tape t;
                CHECK_EQUAL(0, t.get_position());
                CHECK_EQUAL(false, t.read_cell());
    }

    TEST(CopyConstructor) {
        Tape t1;
        t1.set_cell(5, true);
        t1.set_position(5);
        Tape t2(t1);
                CHECK_EQUAL(true, t2.get_cell(5));
                CHECK_EQUAL(5, t2.get_position());
    }

    TEST(AssignmentOperator) {
        Tape t1;
        t1.set_cell(-3, true);
        t1.set_position(-3);
        Tape t2;
        t2 = t1;
                CHECK_EQUAL(true, t2.get_cell(-3));
                CHECK_EQUAL(-3, t2.get_position());
    }

    TEST(EqualityOperators) {
        Tape t1, t2;
        t1.set_cell(10, true);
        t2.set_cell(10, true);
                CHECK(t1 == t2);
        t2.set_cell(11, true);
                CHECK(t1 != t2);
    }

    TEST(MoveLeftRight) {
        Tape t;
        t.move_right();
                CHECK_EQUAL(1, t.get_position());
        t.move_left();
                CHECK_EQUAL(0, t.get_position());
    }

    TEST(SetGetPosition) {
        Tape t;
        t.set_position(42);
                CHECK_EQUAL(42, t.get_position());
    }

    TEST(WriteReadCell) {
        Tape t;
        t.write_cell(true);
                CHECK_EQUAL(true, t.read_cell());
        t.move_right();
                CHECK_EQUAL(false, t.read_cell());
    }

    TEST(SetGetCell) {
        Tape t;
        t.set_cell(100, true);
                CHECK_EQUAL(true, t.get_cell(100));
                CHECK_EQUAL(false, t.get_cell(101));
    }

    TEST(EraseCell) {
        Tape t;
        t.set_cell(5, true);
        t.set_cell(5, false);
                CHECK_EQUAL(false, t.get_cell(5));
    }

    TEST(PrintEmptyTape) {
        std::ostringstream oss;
        std::streambuf* old = std::cout.rdbuf(oss.rdbuf());
        Tape t;
        t.print(0);
        std::cout.rdbuf(old);
                CHECK(oss.str().find("[ ]") != std::string::npos);
    }

    TEST(PrintNonEmptyTape) {
        std::ostringstream oss;
        std::streambuf* old = std::cout.rdbuf(oss.rdbuf());
        Tape t;
        t.set_cell(-1, true);
        t.set_cell(0, false);
        t.set_cell(1, true);
        t.print(0);
        std::cout.rdbuf(old);
        std::string output = oss.str();
                CHECK(output.find("[0]") != std::string::npos);
                CHECK(output.find("1") != std::string::npos);
    }
}
