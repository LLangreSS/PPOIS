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
SUITE(ProgramExhaustiveTests) {

    static Command make_simple_command(CommandType type) {
        Command cmd;
        cmd.type = type;
        return cmd;
    }

    static Command make_jump_command(int jump_target, int no_jump_target) {
        Command cmd;
        cmd.type = CommandType::JUMP;
        cmd.jump = jump_target;
        cmd.no_jump = no_jump_target;
        return cmd;
    }

    TEST(DefaultConstructor) {
        Program p;
                CHECK_EQUAL(0, p.get_size());
    }

    TEST(CopyConstructor_Empty) {
        Program p1;
        Program p2(p1);
                CHECK_EQUAL(0, p2.get_size());
    }

    TEST(CopyConstructor_NonEmpty) {
        Program p1;
        p1.add_command(make_simple_command(CommandType::MARK));
        p1.add_command(make_simple_command(CommandType::STOP));
        Program p2(p1);
                CHECK_EQUAL(2, p2.get_size());
                CHECK_EQUAL(static_cast<int>(p1.at(0).type), static_cast<int>(p2.at(0).type));
                CHECK_EQUAL(static_cast<int>(p1.at(1).type), static_cast<int>(p2.at(1).type));
    }

    TEST(AssignmentOperator_EmptyToNonEmpty) {
        Program p1;
        p1.add_command(make_simple_command(CommandType::MOVE_RIGHT));
        Program p2;
        p2 = p1;
                CHECK_EQUAL(1, p2.get_size());
                CHECK_EQUAL(static_cast<int>(CommandType::MOVE_RIGHT), static_cast<int>(p2.at(0).type));
    }

    TEST(AssignmentOperator_SelfAssignment) {
        Program p;
        p.add_command(make_simple_command(CommandType::ERASE));
        p = p; // критическая ветка: if (this != &other)
                CHECK_EQUAL(1, p.get_size());
                CHECK_EQUAL(static_cast<int>(CommandType::ERASE), static_cast<int>(p.at(0).type));
    }

    // --- Операторы сравнения ---
    TEST(Equality_BothEmpty) {
        Program p1, p2;
                CHECK(p1 == p2);
    }

    TEST(Equality_IdenticalSimpleCommands) {
        Program p1, p2;
        p1.add_command(make_simple_command(CommandType::MOVE_LEFT));
        p2.add_command(make_simple_command(CommandType::MOVE_LEFT));
                CHECK(p1 == p2);
    }

    TEST(Equality_DifferentSimpleCommands) {
        Program p1, p2;
        p1.add_command(make_simple_command(CommandType::MARK));
        p2.add_command(make_simple_command(CommandType::ERASE));
                CHECK(p1 != p2);
    }

    TEST(Equality_JumpCommands_SameParams) {
        Program p1, p2;
        auto cmd = make_jump_command(5, 3);
        p1.add_command(cmd);
        p2.add_command(cmd);
                CHECK(p1 == p2);
    }

    TEST(Equality_JumpCommands_DifferentJump) {
        Program p1, p2;
        p1.add_command(make_jump_command(5, 3));
        p2.add_command(make_jump_command(6, 3));
                CHECK(p1 != p2);
    }

    TEST(Equality_JumpCommands_DifferentNoJump) {
        Program p1, p2;
        p1.add_command(make_jump_command(5, 3));
        p2.add_command(make_jump_command(5, 4));
                CHECK(p1 != p2);
    }

    TEST(Equality_DifferentSizes) {
        Program p1, p2;
        p1.add_command(make_simple_command(CommandType::STOP));
                CHECK(p1 != p2);
    }

    // --- add_command ---
    TEST(AddCommand_IncrementsSize) {
        Program p;
        p.add_command(make_simple_command(CommandType::MOVE_RIGHT));
                CHECK_EQUAL(1, p.get_size());
        p.add_command(make_simple_command(CommandType::STOP));
                CHECK_EQUAL(2, p.get_size());
    }

    // --- remove_command ---
    TEST(RemoveCommand_First) {
        Program p;
        p.add_command(make_simple_command(CommandType::MARK));
        p.add_command(make_simple_command(CommandType::MARK));
        p.remove_command(0);
                CHECK_EQUAL(1, p.get_size());
                CHECK_EQUAL(static_cast<int>(CommandType::MARK), static_cast<int>(p.at(0).type));
    }

    TEST(RemoveCommand_Last) {
        Program p;
        p.add_command(make_simple_command(CommandType::MARK));
        p.add_command(make_simple_command(CommandType::STOP));
        p.remove_command(1);
                CHECK_EQUAL(1, p.get_size());
                CHECK_EQUAL(static_cast<int>(CommandType::MARK), static_cast<int>(p.at(0).type));
    }

    TEST(RemoveCommand_SingleElement) {
        Program p;
        p.add_command(make_simple_command(CommandType::STOP));
        p.remove_command(0);
                CHECK_EQUAL(0, p.get_size());
    }

    TEST(RemoveCommand_Empty_Throws) {
        Program p;
                CHECK_THROW(p.remove_command(0), std::out_of_range);
    }

    TEST(RemoveCommand_NegativeIndex_Throws) {
        Program p;
        p.add_command(make_simple_command(CommandType::MARK));
                CHECK_THROW(p.remove_command(-1), std::out_of_range);
    }

    TEST(RemoveCommand_IndexTooLarge_Throws) {
        Program p;
        p.add_command(make_simple_command(CommandType::ERASE));
                CHECK_THROW(p.remove_command(1), std::out_of_range);
    }

    // --- set_command ---
    TEST(SetCommand_ValidIndex) {
        Program p;
        p.add_command(make_simple_command(CommandType::MOVE_LEFT));
        p.set_command(0, make_simple_command(CommandType::STOP));
                CHECK_EQUAL(static_cast<int>(CommandType::STOP), static_cast<int>(p.at(0).type));
    }

    TEST(SetCommand_PreservesOtherElements) {
        Program p;
        p.add_command(make_simple_command(CommandType::MOVE_LEFT));
        p.add_command(make_simple_command(CommandType::MOVE_RIGHT));
        p.add_command(make_simple_command(CommandType::STOP));
        p.set_command(1, make_simple_command(CommandType::JUMP));
                CHECK_EQUAL(static_cast<int>(CommandType::MOVE_LEFT), static_cast<int>(p.at(0).type));
                CHECK_EQUAL(static_cast<int>(CommandType::JUMP), static_cast<int>(p.at(1).type));
                CHECK_EQUAL(static_cast<int>(CommandType::STOP), static_cast<int>(p.at(2).type));
    }

    TEST(SetCommand_Empty_Throws) {
        Program p;
                CHECK_THROW(p.set_command(0, make_simple_command(CommandType::MARK)), std::out_of_range);
    }

    TEST(SetCommand_NegativeIndex_Throws) {
        Program p;
        p.add_command(make_simple_command(CommandType::STOP));
                CHECK_THROW(p.set_command(-1, make_simple_command(CommandType::ERASE)), std::out_of_range);
    }

    TEST(SetCommand_IndexTooLarge_Throws) {
        Program p;
        p.add_command(make_simple_command(CommandType::MOVE_RIGHT));
                CHECK_THROW(p.set_command(1, make_simple_command(CommandType::JUMP)), std::out_of_range);
    }

    // --- at() ---
    TEST(At_Mutable_Valid) {
        Program p;
        p.add_command(make_simple_command(CommandType::MARK));
        Command& c = p.at(0);
        c.type = CommandType::ERASE;
                CHECK_EQUAL(static_cast<int>(CommandType::ERASE), static_cast<int>(p.at(0).type));
    }

    TEST(At_Const_Valid) {
        Program p;
        p.add_command(make_simple_command(CommandType::STOP));
        const Program& cp = p;
        const Command& c = cp.at(0);
                CHECK_EQUAL(static_cast<int>(CommandType::STOP), static_cast<int>(c.type));
    }

    TEST(At_Empty_Throws) {
        Program p;
                CHECK_THROW(p.at(0), std::out_of_range);
        const Program& cp = p;
                CHECK_THROW(cp.at(0), std::out_of_range);
    }

    TEST(At_NegativeIndex_Throws) {
        Program p;
        p.add_command(make_simple_command(CommandType::MOVE_LEFT));
                CHECK_THROW(p.at(-1), std::out_of_range);
        const Program& cp = p;
                CHECK_THROW(cp.at(-1), std::out_of_range);
    }

    TEST(At_IndexTooLarge_Throws) {
        Program p;
        p.add_command(make_simple_command(CommandType::JUMP));
                CHECK_THROW(p.at(1), std::out_of_range);
        const Program& cp = p;
                CHECK_THROW(cp.at(1), std::out_of_range);
    }

    // --- get_size ---
    TEST(GetSize_ConsistentAfterOperations) {
        Program p;
                CHECK_EQUAL(0, p.get_size());

        p.add_command(make_simple_command(CommandType::MARK));
                CHECK_EQUAL(1, p.get_size());

        p.add_command(make_simple_command(CommandType::STOP));
                CHECK_EQUAL(2, p.get_size());

        p.remove_command(0);
                CHECK_EQUAL(1, p.get_size());

        p.set_command(0, make_simple_command(CommandType::ERASE));
                CHECK_EQUAL(1, p.get_size());
    }

    // --- Смешанные сценарии ---
    TEST(Program_ComplexSequence) {
        Program p;
        p.add_command(make_simple_command(CommandType::MOVE_RIGHT));
        p.add_command(make_jump_command(4, 2));
        p.add_command(make_simple_command(CommandType::MARK));
        p.add_command(make_simple_command(CommandType::STOP));

                CHECK_EQUAL(4, p.get_size());
                CHECK_EQUAL(static_cast<int>(CommandType::JUMP), static_cast<int>(p.at(1).type));
                CHECK_EQUAL(4, p.at(1).jump);
                CHECK_EQUAL(2, p.at(1).no_jump);

        p.remove_command(2); // удаляем MARK
                CHECK_EQUAL(3, p.get_size());
                CHECK_EQUAL(static_cast<int>(CommandType::STOP), static_cast<int>(p.at(2).type));

        p.set_command(0, make_simple_command(CommandType::MOVE_LEFT));
                CHECK_EQUAL(static_cast<int>(CommandType::MOVE_LEFT), static_cast<int>(p.at(0).type));
    }
}
