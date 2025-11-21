#pragma once
#include <iterator>
#include <cstddef>

namespace graph_details {

    template <typename Host, typename RefType, typename PtrType, typename ValueType>
    class NodeDataWalker {
        Host* owner_;
        std::size_t position_;

    public:
        using iterator_category = std::bidirectional_iterator_tag;
        using value_type = ValueType;
        using difference_type = std::ptrdiff_t;
        using pointer = PtrType;
        using reference = RefType;

        NodeDataWalker(Host* g, std::size_t idx) : owner_(g), position_(idx) {}

        reference operator*() const { return owner_->nodes_pool[position_].payload; }
        pointer operator->() const { return &(owner_->nodes_pool[position_].payload); }

        NodeDataWalker& operator++() { ++position_; return *this; }
        NodeDataWalker operator++(int) { auto tmp = *this; ++(*this); return tmp; }
        NodeDataWalker& operator--() { --position_; return *this; }
        NodeDataWalker operator--(int) { auto tmp = *this; --(*this); return tmp; }

        bool operator==(const NodeDataWalker& other) const {
            return position_ == other.position_ && owner_ == other.owner_;
        }
        bool operator!=(const NodeDataWalker& other) const {
            return !(*this == other);
        }

        [[nodiscard]] std::size_t index() const { return position_; }
    };

}