#pragma once
#include <iostream>
#include <string>
class Student {
public:
    std::string name;
    int score;

    Student(const std::string& n, int s) : name(n), score(s) {}

    bool operator<(const Student& other) const {
        return score < other.score;
    }

    friend std::ostream& operator<<(std::ostream& os, const Student& s) {
        os << s.name << " (" << s.score << ")";
        return os;
    }
};
