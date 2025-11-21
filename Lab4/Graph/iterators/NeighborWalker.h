#pragma once
#include <iterator>
#include <vector>
#include <cstddef>

namespace graph_details {

    class NeighborWalker {
        const std::vector<std::size_t>* ref_list_;
        std::size_t cursor_;

    public:
        using iterator_category = std::bidirectional_iterator_tag;
        using value_type = std::size_t;
        using difference_type = std::ptrdiff_t;
        using pointer = const std::size_t*;
        using reference = const std::size_t&;

        NeighborWalker(const std::vector<std::size_t>* list, std::size_t idx)
                : ref_list_(list), cursor_(idx) {}

        value_type operator*() const { return (*ref_list_)[cursor_]; }

        NeighborWalker& operator++() { ++cursor_; return *this; }
        NeighborWalker operator++(int) { auto tmp = *this; ++(*this); return tmp; }
        NeighborWalker& operator--() { --cursor_; return *this; }
        NeighborWalker operator--(int) { auto tmp = *this; --(*this); return tmp; }

        bool operator==(const NeighborWalker& other) const {
            return cursor_ == other.cursor_ && ref_list_ == other.ref_list_;
        }
        bool operator!=(const NeighborWalker& other) const {
            return !(*this == other);
        }
    };

}