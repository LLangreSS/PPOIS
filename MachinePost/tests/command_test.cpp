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
SUITE(CommandTests) {
    TEST(ConstructorFromCommandType) {
        Command c1(CommandType::MOVE_RIGHT);
                CHECK_EQUAL(static_cast<int>(CommandType::MOVE_RIGHT), static_cast<int>(c1.type));
                CHECK_EQUAL(0, c1.jump);
                CHECK_EQUAL(0, c1.no_jump);

        Command c2(CommandType::JUMP);
                CHECK_EQUAL(static_cast<int>(CommandType::JUMP), static_cast<int>(c2.type));
    }
    TEST(DefaultConstructor) {
        Command c;
                CHECK_EQUAL(static_cast<int>(CommandType::NONE), static_cast<int>(c.type));
                CHECK_EQUAL(0, c.jump);
                CHECK_EQUAL(0, c.no_jump);
    }

    TEST(CopyConstructor) {
        Command c1;
        c1.type = CommandType::JUMP;
        c1.jump = 5;
        c1.no_jump = 3;
        Command c2(c1);
                CHECK_EQUAL(static_cast<int>(c2.type), static_cast<int>(c1.type));
                CHECK_EQUAL(5, c2.jump);
                CHECK_EQUAL(3, c2.no_jump);
    }

    TEST(AssignmentOperator) {
        Command c1, c2;
        c1.type = CommandType::MARK;
        c2 = c1;
                CHECK_EQUAL(static_cast<int>(CommandType::MARK), static_cast<int>(c2.type));
    }

    TEST(EqualityOperators) {
        Command c1, c2;
        c1.type = CommandType::ERASE;
        c2.type = CommandType::ERASE;
                CHECK(c1 == c2);
        c2.type = CommandType::MARK;
                CHECK(c1 != c2);
    }
}
