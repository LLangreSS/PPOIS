#include "machine_post.h"
Command::Command(CommandType t):jump(0),no_jump(0),type(t){}
Command::Command():jump(0),no_jump(0),type(CommandType::NONE) {}
Command::Command(const Command &other) {
   this->no_jump=other.no_jump;
   this->jump=other.jump;
   this->type=other.type;
}

Command &Command::operator=(const Command &other) {
    if (this!=&other)
    {
        this->no_jump=other.no_jump;
        this->jump=other.jump;
        this->type=other.type;
    }
    return *this;
};

bool Command::operator==(const Command &other) const {
    return (this->no_jump==other.no_jump &&
    this->jump==other.jump &&
    this->type==other.type);
}
bool Command::operator!=(const Command &other) const {
    return !(*this==other);
}