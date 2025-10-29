#include "machine_post.h"
Program::Program() {}
Program::Program(const Program &other) {
   this->commands=other.commands;
}

Program &Program::operator=(const Program &other) {
    if (this!=&other) {
        this->commands=other.commands;
    }
    return *this;
}

bool Program::operator==(const Program &other) const {
    return (this->commands==other.commands);
}
bool Program::operator!=(const Program &other) const {
    return !(*this==other);
}

void Program::add_command(Command cmd) {
    commands.push_back(cmd);
}
void Program::remove_command(int index) {
    if (index < 0 || index >= static_cast<int>(commands.size())) {
        throw std::out_of_range("Program::remove_command: index out of range");
    }
    commands.erase(commands.begin() + index);
}
void Program::set_command(int index, const Command& cmd) {
    if (index < 0 || index >= static_cast<int>(commands.size())) {
        throw std::out_of_range("Program::set_command: index out of range");
    }
    commands[index] = cmd;
}

Command& Program::at(int i) {
    if (i < 0 || i >= static_cast<int>(commands.size())) {
        throw std::out_of_range("Program::at: index out of range");
    }
    return commands[i];
}
const Command& Program::at(int i) const {
    if (i < 0 || i >= static_cast<int>(commands.size())) {
        throw std::out_of_range("Program::at: index out of range");
    }
    return commands[i];
}

int Program::get_size() {
    return commands.size();
}