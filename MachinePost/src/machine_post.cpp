#include "machine_post.h"
MachinePost::MachinePost(bool log): head_pos(0),logging(log),program_index(0){}
MachinePost::MachinePost(const MachinePost &other) {
    this->head_pos=other.head_pos;
    this->tape=other.tape;
    this->program_index=other.program_index;
    this->prog=other.prog;
    this->logging=other.logging;
}

MachinePost &MachinePost::operator=(const MachinePost &other) {
    if (this!=&other) {
        this->head_pos=other.head_pos;
        this->tape=other.tape;
        this->program_index=other.program_index;
        this->prog=other.prog;
        this->logging=other.logging;
    }
    return *this;
}

bool MachinePost::operator==(const MachinePost &other) const {
    return (this->head_pos==other.head_pos &&
    this->tape==other.tape &&
    this->program_index==other.program_index &&
    this->prog==other.prog &&
    this->logging==other.logging);
}
bool MachinePost::operator!=(const MachinePost &other) const {
    return !(*this==other);
}

void MachinePost::load_head_position(std::istream& f) {
    std::string line;
    if (!std::getline(f, line)) {
        throw std::runtime_error("Missing head position in file");
    }
    head_pos = std::stoi(line);
}
void MachinePost::load_tape_state(std::istream& f) {
    std::string line;
    while (std::getline(f, line) && !line.empty()) {
        std::istringstream is(line);
        int pos, val;
        if (!(is >> pos >> val)) {
            throw std::runtime_error("Invalid tape cell format: " + line);
        }
        tape.set_cell(pos, static_cast<bool>(val));
    }
}
void MachinePost::load_program(std::istream& f) {
    std::string line;
    while (std::getline(f, line)) {
        if (line.empty()) continue;
        prog.add_command(parse_command(line));
    }
}
void MachinePost::load_from_stream(std::istream &is){
    load_head_position(is);
    load_tape_state(is);
    load_program(is);
}
void MachinePost::load(const std::string& filename) {
    if (filename == "-"){
        load_from_stream(std::cin);
    }
    else {
        std::ifstream f(filename);
        if (!f.is_open()) {
            throw std::runtime_error("Cannot open file: " + filename);
        }
        load_from_stream(f);
    }
}

Command MachinePost::parse_command(const std::string& line) {
    Command cmd;
    if (line == "<-") {
        cmd.type = CommandType::MOVE_LEFT;
    } else if (line == "->") {
        cmd.type = CommandType::MOVE_RIGHT;
    } else if (line == "!") {
        cmd.type = CommandType::STOP;
    } else if (line == "1") {
        cmd.type = CommandType::MARK;
    } else if (line == "0") {
        cmd.type = CommandType::ERASE;
    } else if (line[0] == '?') {
        cmd.type = CommandType::JUMP;
        std::istringstream is(line.substr(1));
        if (!(is >> cmd.jump >> cmd.no_jump)) {
            throw std::runtime_error("Invalid jump command: " + line);
        }
    } else {
        throw std::invalid_argument("Unknown command: " + line);
    }
    return cmd;
}

bool MachinePost::step(){
    if (program_index >= prog.get_size()) return false;

    const Command& cmd = prog.at(program_index);

    bool continue_execution = true;
    switch (cmd.type) {
        case CommandType::MOVE_RIGHT: handle_move_right(); break;
        case CommandType::MOVE_LEFT:  handle_move_left(); break;
        case CommandType::MARK:       handle_mark(); break;
        case CommandType::ERASE:      handle_erase(); break;
        case CommandType::STOP:       continue_execution = false; break;
        case CommandType::JUMP:       handle_jump(cmd); break;
    }

    if (logging && continue_execution) {
        log_state();
    }
    return continue_execution;
}

void MachinePost::handle_move_right() {
    head_pos++;
    program_index++;
}
void MachinePost::handle_move_left() {
    head_pos--;
    program_index++;
}
void MachinePost::handle_mark() {
    tape.set_cell(head_pos, true);
    program_index++;
}
void MachinePost::handle_erase() {
    tape.set_cell(head_pos, false);
    program_index++;
}
void MachinePost::handle_jump(const Command& cmd) {
    bool value = tape.read_cell();
    program_index = value ? (cmd.jump - 1) : (cmd.no_jump - 1);
}

void MachinePost::log_state() const {
    std::cout << "--- Step " << program_index << " ---\n";
    tape.print(head_pos);
    std::cout << "\n";
}
void MachinePost::run() {
    const int max_steps = 10000;
    if (logging) {
        std::cout << "Start:\n";
        tape.print(head_pos);
        std::cout << "\n";
    }
    int steps = 0;
    while (step() && steps < max_steps) {
        steps++;
    }
    if (steps >= max_steps) {
        std::cout << "Execution stopped: too many steps (>=" << max_steps << ")\n";
    } else {
        std::cout << "Machine stopped normally.\n";
        if (logging) tape.print(head_pos);
    }
}
void MachinePost::reset() {
    tape = Tape();
    head_pos = 0;
    program_index = 0;
    prog = Program();
}
