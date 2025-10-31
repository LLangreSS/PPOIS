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
SUITE(MachinePostTests) {
    TEST(Step_JumpToZeroIndex) {
        MachinePost m(false);
        m.get_tape().set_cell(0, true);
        Command jump;
        jump.type = CommandType::JUMP;
        jump.jump = 1;
        jump.no_jump = 2;
        m.get_program().add_command(jump);
        m.set_program_index(0);
        m.step();
                CHECK_EQUAL(0, m.get_program_index()); // jump - 1 = 0
    }

    TEST(Step_JumpToNegativeIndex) {
        MachinePost m(false);
        Command jump;
        jump.type = CommandType::JUMP;
        jump.jump = 1;
        jump.no_jump = 0;
        m.get_program().add_command(jump);
        m.set_program_index(0);
        m.step();
                CHECK_EQUAL(-1, m.get_program_index());
    }

    TEST(Step_AfterProgramEnd) {
        MachinePost m(false);
        m.get_program().add_command(Command{CommandType::STOP});
        m.set_program_index(1);
        bool cont = m.step();
                CHECK_EQUAL(false, cont);
    }



    TEST(LoadHeadPosition_NegativeValue) {
        std::istringstream input("-5\n\n!\n");
        MachinePost m(false);
        m.load_from_stream(input);
                CHECK_EQUAL(-5, m.get_pos());
    }

    TEST(LoadTapeState_ZeroValueNotStored) {
        std::istringstream input("0\n10 0\n\n!\n");
        MachinePost m(false);
        m.load_from_stream(input);
                CHECK_EQUAL(false, m.get_tape().get_cell(10));
    }

    TEST(LoadProgram_CommentOrEmptyLineAtEnd) {
        std::istringstream input("0\n\n->\n!\n\n");
        MachinePost m(false);
        m.load_from_stream(input);
                CHECK_EQUAL(2, m.get_program().get_size());
    }

    TEST(LoadProgram_OnlyStop) {
        std::istringstream input("0\n\n!\n");
        MachinePost m(false);
        m.load_from_stream(input);
                CHECK_EQUAL(1, m.get_program().get_size());
                CHECK_EQUAL(static_cast<int>(CommandType::STOP),
                            static_cast<int>(m.get_program().at(0).type));
    }
    TEST(Run_EmptyProgram) {
        MachinePost m(false);
        std::ostringstream oss;
        std::streambuf* old = std::cout.rdbuf(oss.rdbuf());
        m.run();
        std::cout.rdbuf(old);
        std::string out = oss.str();
                CHECK(out.find("Machine stopped normally.") != std::string::npos);
    }
    TEST(Run_LoggingDisabled_NoIntermediateOutput) {
        std::istringstream input("0\n\n1\n!\n");
        MachinePost m(false); // logging = false
        std::ostringstream oss;
        std::streambuf* old = std::cout.rdbuf(oss.rdbuf());
        m.load_from_stream(input);
        m.run();
        std::cout.rdbuf(old);
        std::string out = oss.str();
                CHECK(out.find("Start:") == std::string::npos);
                CHECK(out.find("[1]") == std::string::npos);
                CHECK(out.find("Machine stopped normally.") != std::string::npos);
    }

    TEST(Run_LoggingEnabled_WithSteps) {
        std::istringstream input("0\n\n1\n->\n!\n");
        MachinePost m(true); // logging = true
        std::ostringstream oss;
        std::streambuf* old = std::cout.rdbuf(oss.rdbuf());
        m.load_from_stream(input);
        m.run();
        std::cout.rdbuf(old);
        std::string out = oss.str();
                CHECK(out.find("Start:") != std::string::npos);
                CHECK(out.find("Step 1") != std::string::npos);
                CHECK(out.find("Step 2") != std::string::npos);
    }


    TEST(Reset_PreservesLoggingFlag) {
        MachinePost m(true);
        m.reset();
        std::ostringstream oss;
        std::streambuf* old = std::cout.rdbuf(oss.rdbuf());
        m.run();
        std::cout.rdbuf(old);
                CHECK(oss.str().find("Start:") != std::string::npos);
    }



    TEST(Equality_DifferentTape) {
        MachinePost m1(false), m2(false);
        m1.get_tape().set_cell(0, true);
                CHECK(m1 != m2);
    }

    TEST(Equality_DifferentProgram) {
        MachinePost m1(false), m2(false);
        m1.get_program().add_command(Command{CommandType::STOP});
                CHECK(m1 != m2);
    }
    TEST(Equality_DifferentHeadPos) {
        MachinePost m1(false), m2(false);
        m1.set_pos(1);
                CHECK(m1 != m2);
    }

    TEST(Equality_DifferentProgramIndex) {
        MachinePost m1(false), m2(false);
        m1.set_program_index(1);
                CHECK(m1 != m2);
    }



    TEST(Program_LargeSize) {
        Program p;
        const int N = 1000;
        for (int i = 0; i < N; ++i) {
            p.add_command(Command{CommandType::MOVE_RIGHT});
        }
                CHECK_EQUAL(N, p.get_size());
        for (int i = 0; i < N; ++i) {
                    CHECK_EQUAL(static_cast<int>(CommandType::MOVE_RIGHT),
                                static_cast<int>(p.at(i).type));
        }
    }



    TEST(Run_JumpToStop) {
        std::istringstream input("0\n\n?2 3\n1\n!\n");
        MachinePost m(false);
        m.load_from_stream(input);
        std::ostringstream oss;
        std::streambuf* old = std::cout.rdbuf(oss.rdbuf());
        m.run();
        std::cout.rdbuf(old);
                CHECK(oss.str().find("Machine stopped normally.") != std::string::npos);
    }
    TEST(Step_EmptyProgram) {
        MachinePost m(false);
        bool cont = m.step();
                CHECK_EQUAL(false, cont);
    }

    TEST(Step_ProgramIndexBeyondSize) {
        MachinePost m(false);
        m.set_program_index(100);
        bool cont = m.step();
                CHECK_EQUAL(false, cont);
    }

    TEST(HandleJump_ZeroJumpValues) {
        MachinePost m(false);
        Command cmd;
        cmd.type = CommandType::JUMP;
        cmd.jump = 0;
        cmd.no_jump = 0;
        m.set_program_index(5);
        m.handle_jump(cmd);
                CHECK_EQUAL(-1, m.get_program_index());

    }

    TEST(LoadProgram_EmptyLineHandling) {
        std::istringstream input("0\n\n->\n\n1\n\n!\n\n");
        MachinePost m(false);
        m.load_from_stream(input);
                CHECK_EQUAL(3, m.get_program().get_size());
    }

    TEST(LoadTapeState_SingleLine) {
        std::istringstream input("0\n5 1\n\n!\n");
        MachinePost m(false);
        m.load_from_stream(input);
                CHECK_EQUAL(true, m.get_tape().get_cell(5));
                CHECK_EQUAL(false, m.get_tape().get_cell(0));
    }

    TEST(LoadTapeState_MultipleSpaces) {
        std::istringstream input("0\n  -3   0  \n\n!\n");
        MachinePost m(false);
        m.load_from_stream(input);
                CHECK_EQUAL(false, m.get_tape().get_cell(-3));
    }

    TEST(ParseCommand_JumpWithExtraSpaces) {
        MachinePost m(false);
        Command cmd = m.parse_command("?  5   3  ");
                CHECK_EQUAL(static_cast<int>(CommandType::JUMP), static_cast<int>(cmd.type));
                CHECK_EQUAL(5, cmd.jump);
                CHECK_EQUAL(3, cmd.no_jump);
    }

    TEST(Run_LoggingEnabled_PrintsStartAndEnd) {
        std::istringstream input("0\n0 1\n\n1\n!\n");
        MachinePost m(true); // logging = true
        std::ostringstream oss;
        std::streambuf* old = std::cout.rdbuf(oss.rdbuf());
        m.load_from_stream(input);
        m.run();
        std::cout.rdbuf(old);

        std::string out = oss.str();
                CHECK(out.find("Start:") != std::string::npos);
                CHECK(out.find("Machine stopped normally.") != std::string::npos);
                CHECK(out.find("[1]") != std::string::npos);
    }

    TEST(Reset_AfterRun) {
        std::istringstream input("0\n\n1\n!\n");
        MachinePost m(false);
        m.load_from_stream(input);
        m.run();
        m.reset();
                CHECK_EQUAL(0, m.get_pos());
                CHECK_EQUAL(0, m.get_program_index());
                CHECK_EQUAL(0, m.get_program().get_size());
                CHECK_EQUAL(false, m.get_tape().read_cell());
    }

    TEST(EqualityOperator_DifferentLogging) {
        MachinePost m1(true), m2(false);
                CHECK(m1 != m2);
    }

    TEST(SelfAssignment_MachinePost) {
        MachinePost m1(false);
        m1.get_tape().set_cell(10, true);
        m1.get_program().add_command(Command{CommandType::STOP});
        m1.set_pos(5);
        m1.set_program_index(0);

        m1 = m1;

                CHECK_EQUAL(5, m1.get_pos());
                CHECK_EQUAL(true, m1.get_tape().get_cell(10));
                CHECK_EQUAL(1, m1.get_program().get_size());
    }

    TEST(ConstructorAndLogging) {
        MachinePost m(true);
                CHECK_EQUAL(0, m.get_pos());
                CHECK_EQUAL(0, m.get_program_index());
                CHECK(m.get_tape().get_cell(0) == false);
    }

    TEST(CopyAndAssignment) {
        MachinePost m1(false);
        m1.get_tape().set_cell(5, true);
        m1.get_program().add_command(Command{CommandType::MARK});
        MachinePost m2(m1);
                CHECK(m1 == m2);

        MachinePost m3(true);
        m3 = m1;
                CHECK(m1 == m3);
                CHECK_EQUAL(false, m3.get_tape().get_cell(6));
                CHECK_EQUAL(1, m3.get_program().get_size());
    }

    TEST(ParseCommand_ValidCommands) {
        MachinePost m(false);
        Command cmd;

        cmd = m.parse_command("->");
                CHECK_EQUAL(static_cast<int>(CommandType::MOVE_RIGHT), static_cast<int>(cmd.type));

        cmd = m.parse_command("<-");
                CHECK_EQUAL(static_cast<int>(CommandType::MOVE_LEFT), static_cast<int>(cmd.type));

        cmd = m.parse_command("1");
                CHECK_EQUAL(static_cast<int>(CommandType::MARK), static_cast<int>(cmd.type));

        cmd = m.parse_command("0");
                CHECK_EQUAL(static_cast<int>(CommandType::ERASE), static_cast<int>(cmd.type));

        cmd = m.parse_command("!");
                CHECK_EQUAL(static_cast<int>(CommandType::STOP), static_cast<int>(cmd.type));

        cmd = m.parse_command("?5 3");
                CHECK_EQUAL(static_cast<int>(CommandType::JUMP), static_cast<int>(cmd.type));
                CHECK_EQUAL(5, cmd.jump);
                CHECK_EQUAL(3, cmd.no_jump);
    }

    TEST(ParseCommand_InvalidCommand) {
        MachinePost m(false);
                CHECK_THROW(m.parse_command("xyz"), std::invalid_argument);
                CHECK_THROW(m.parse_command("?"), std::runtime_error);
                CHECK_THROW(m.parse_command("?a b"), std::runtime_error);
    }

    TEST(LoadFromStream_ValidInput) {
        std::istringstream input("2\n-1 1\n0 0\n1 1\n\n->\n1\n!\n");
        MachinePost m(false);
        m.load_from_stream(input);

                CHECK_EQUAL(2, m.get_pos());
                CHECK_EQUAL(true, m.get_tape().get_cell(-1));
                CHECK_EQUAL(false, m.get_tape().get_cell(0));
                CHECK_EQUAL(true, m.get_tape().get_cell(1));
                CHECK_EQUAL(3, m.get_program().get_size());
                CHECK_EQUAL(static_cast<int>(CommandType::MOVE_RIGHT), static_cast<int>(m.get_program().at(0).type));
                CHECK_EQUAL(static_cast<int>(CommandType::MARK), static_cast<int>(m.get_program().at(1).type));
                CHECK_EQUAL(static_cast<int>(CommandType::STOP), static_cast<int>(m.get_program().at(2).type));
    }

    TEST(LoadFromStream_MissingHeadPosition) {
        std::istringstream input("");
        MachinePost m(false);
                CHECK_THROW(m.load_from_stream(input), std::runtime_error);
    }

    TEST(LoadFromStream_InvalidTapeFormat) {
        std::istringstream input("0\nabc\n");
        MachinePost m(false);
                CHECK_THROW(m.load_from_stream(input), std::runtime_error);
    }

    TEST(Step_MoveRight) {
        MachinePost m(false);
        m.get_program().add_command(Command{CommandType::MOVE_RIGHT});
                CHECK_EQUAL(0, m.get_pos());
                CHECK_EQUAL(0, m.get_program_index());
        bool cont = m.step();
                CHECK_EQUAL(true, cont);
                CHECK_EQUAL(1, m.get_pos());
                CHECK_EQUAL(1, m.get_program_index());
    }

    TEST(Step_MoveLeft) {
        MachinePost m(false);
        m.get_program().add_command(Command{CommandType::MOVE_LEFT});
        m.step();
                CHECK_EQUAL(-1, m.get_pos());
                CHECK_EQUAL(1, m.get_program_index());
    }

    TEST(Step_MarkAndErase) {
        MachinePost m(false);
        m.get_program().add_command(Command{CommandType::MARK});
        m.step();
                CHECK_EQUAL(true, m.get_tape().get_cell(0));

        m.reset();
        m.get_program().add_command(Command{CommandType::ERASE});
        m.step();
                CHECK_EQUAL(false, m.get_tape().get_cell(0)); // already false, but safe
    }

    TEST(Step_Stop) {
        MachinePost m(false);
        m.get_program().add_command(Command{CommandType::STOP});
        bool cont = m.step();
                CHECK_EQUAL(false, cont);
                CHECK_EQUAL(0, m.get_program_index());
    }

    TEST(Step_Jump_True) {
        MachinePost m(false);
        m.get_tape().set_cell(0, true);
        Command jumpCmd;
        jumpCmd.type = CommandType::JUMP;
        jumpCmd.jump = 3;
        jumpCmd.no_jump = 5;
        m.get_program().add_command(Command{CommandType::MOVE_RIGHT});
        m.get_program().add_command(Command{CommandType::MOVE_RIGHT});
        m.get_program().add_command(Command{CommandType::MOVE_RIGHT});
        m.get_program().add_command(jumpCmd);
        m.get_program().add_command(Command{CommandType::STOP});

        m.set_program_index(3);
        m.step();
                CHECK_EQUAL(2, m.get_program_index());
    }

    TEST(Step_Jump_False) {
        MachinePost m(false);

        Command jumpCmd;
        jumpCmd.type = CommandType::JUMP;
        jumpCmd.jump = 10;
        jumpCmd.no_jump = 2;
        m.get_program().add_command(Command{CommandType::ERASE});
        m.get_program().add_command(Command{CommandType::MARK});
        m.get_program().add_command(jumpCmd);

        m.set_program_index(2);
        m.step();
                CHECK_EQUAL(1, m.get_program_index());
    }

    TEST(Run_SimpleProgram) {

        std::istringstream input("0\n\n1\n!\n");
        MachinePost m(false);
        m.load_from_stream(input);
        m.run();

                CHECK_EQUAL(true, m.get_tape().get_cell(0));
    }

    TEST(Run_MaxStepsLimit) {
        std::istringstream input("0\n\n?1 1\n");
        MachinePost m(false);
        m.load_from_stream(input);

        std::ostringstream oss;
        std::streambuf* old = std::cout.rdbuf(oss.rdbuf());
        m.run();
        std::cout.rdbuf(old);

        std::string output = oss.str();
                CHECK(output.find("too many steps") != std::string::npos);
    }

    TEST(Reset_ClearsState) {
        MachinePost m(false);
        m.get_tape().set_cell(10, true);
        m.get_program().add_command(Command{CommandType::STOP});
        m.set_pos(42);
        m.set_program_index(99);

        m.reset();

                CHECK_EQUAL(0, m.get_pos());
                CHECK_EQUAL(0, m.get_program_index());
                CHECK_EQUAL(0, m.get_program().get_size());
                CHECK_EQUAL(false, m.get_tape().get_cell(10));
    }

    TEST(LogState_OutputFormat) {
        MachinePost m(true);
        m.get_tape().set_cell(-1, true);
        m.get_tape().set_cell(0, false);
        m.get_tape().set_cell(1, true);
        m.set_pos(0);

        std::ostringstream oss;
        std::streambuf* old = std::cout.rdbuf(oss.rdbuf());
        m.log_state();
        std::cout.rdbuf(old);

        std::string output = oss.str();
                CHECK(output.find("[0]") != std::string::npos);
                CHECK(output.find("(head on 0)") != std::string::npos);
    }
}
