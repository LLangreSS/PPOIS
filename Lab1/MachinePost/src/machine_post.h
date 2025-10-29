#ifndef MACHINE_POST_H
#define MACHINE_POST_H
#include <map>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
class Tape
{
private:
    std::map<int,bool> cells;
    int position;
public:
    Tape();
    Tape(const Tape &other);

    Tape &operator=(const Tape &other);

    bool operator==(const Tape &other) const;
    bool operator!=(const Tape &other) const;

    void move_right();
    void move_left();

    void set_position(int pos);
    int get_position() const;

    void write_cell(bool value);
    bool read_cell() const;
    void set_cell(int pos,bool value);
    bool get_cell(int pos) const;

    void print(int pos) const;
};
enum class CommandType
{
    MOVE_RIGHT,
    MOVE_LEFT,
    ERASE,
    MARK,
    JUMP,
    STOP,
    NONE
};
class Command
{
public:
    CommandType type;
    int no_jump=0;
    int jump=0;

    Command(CommandType t);
    Command();
    Command(const Command &other);

    Command &operator=(const Command &other);

    bool operator==(const Command  &other) const;
    bool operator!=(const Command  &other) const;
};
class Program
{
private:
    std::vector<Command> commands;
public:

    Program();
    Program(const Program &other);

    Program &operator=(const Program &other);

    bool operator==(const Program &other) const;
    bool operator!=(const Program &other) const;

    void add_command(Command cmd);
    void remove_command(int index);
    void set_command(int index,const Command &cmd);

    Command &at(int i);
    const Command& at(int i)const;

    int get_size();
};
class MachinePost
{
private:
    Tape tape;
    int head_pos;
    int program_index;
    Program prog;
    bool logging;
public:

    explicit MachinePost(bool log);
    MachinePost(const MachinePost &other);

    MachinePost &operator=(const MachinePost &other);

    bool operator==(const MachinePost &other) const;
    bool operator!=(const MachinePost &other) const;

    void load_head_position(std::istream& f);
    void load_tape_state(std::istream& f);
    void load_program(std::istream& f);
    void load(const std::string &filename);
    void load_from_stream(std::istream &is);

    Command parse_command(const std::string& line);

    bool step();

    void handle_move_left();
    void handle_move_right();
    void handle_mark();
    void handle_erase();
    void handle_jump(const Command &cmd);

    void log_state() const;
    void run();

    void reset();

    int get_pos() const {return head_pos;}
    int get_program_index() const {return program_index;}
    void set_pos(int value){head_pos=value;}
    void set_program_index(int value) {program_index=value;}

    Tape& get_tape() { return tape; }
    Program& get_program() {return prog;}
};

#endif //MACHINE_POST_H