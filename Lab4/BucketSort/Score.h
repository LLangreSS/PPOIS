#pragma once
#include <iostream>

class Score {
public:
    explicit Score(double value = 0.0) : value_(value) {
    }

    bool operator<(const Score& other) const {
        return value_ < other.value_;
    }

    bool operator>(const Score& other) const {
        return value_ > other.value_;
    }

    bool operator<=(const Score& other) const {
        return value_ <= other.value_;
    }

    bool operator>=(const Score& other) const {
        return value_ >= other.value_;
    }

    bool operator==(const Score& other) const {
        return value_ == other.value_;
    }

    bool operator!=(const Score& other) const {
        return !(*this == other);
    }

    double operator*(size_t multiplier) const {
        return value_ * static_cast<double>(multiplier);
    }

private:
    double value_;
};