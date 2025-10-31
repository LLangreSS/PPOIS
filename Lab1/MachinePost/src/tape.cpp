#include "machine_post.h"
Tape::Tape() : position(0){}
Tape::Tape(const Tape &other) {
    this->cells=other.cells;
    this->position=other.position;
}

Tape &Tape::operator=(const Tape &other) {
    if (this!=&other)
    {
        this->position=other.position;
        this->cells=other.cells;
    }
    return *this;
}

bool Tape::operator==(const Tape &other) const {
    return (this->position==other.position && this->cells==other.cells);
}
bool Tape::operator!=(const Tape &other) const {
    return !(*this==other);
}

void Tape::move_left() {
    position--;
}
void Tape::move_right() {
    position++;
}

void Tape::set_position(int pos) {
    position=pos;
}
int Tape::get_position() const {
    return position;
}

bool Tape::read_cell() const {
    auto current_cell=cells.find(position);
    return (current_cell!=cells.end())?current_cell->second:0;
}
void Tape::write_cell(bool value) {
    if (value) cells[position]=value;
    else cells.erase(position);
}
void Tape::set_cell(int pos, bool value) {
    if (value) cells[pos]=value;
    else cells.erase(pos);
}
bool Tape::get_cell(int pos) const {
    auto it=cells.find(pos);
    return (it!=cells.end())?it->second:0;
}

void Tape::print(int pos) const {
    if (cells.empty()) {
        std::cout << "[ ] (head on " << pos << ")\n";
        return;
    }
    int minP = std::min(cells.begin()->first, pos);
    int maxP = std::max(cells.rbegin()->first, pos);
    for (int i = minP; i <= maxP; i++) {
        if (i == pos) std::cout << '[' << (get_cell(i) ? '1' : '0') << ']';
        else std::cout << ' ' << (get_cell(i) ? '1' : '0') << ' ';
    }
    std::cout << " (head on " << pos << ")\n";
}