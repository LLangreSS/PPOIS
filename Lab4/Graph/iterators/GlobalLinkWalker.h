#pragma once
#include <iterator>
#include <vector>
#include <utility>
#include <cstddef>

namespace graph_details {

    template <typename GraphType>
    class GlobalLinkWalker {
        std::vector<typename GraphType::Link> cached_links_;
        std::size_t current_index_;

    public:
        using iterator_category = std::bidirectional_iterator_tag;
        using value_type = typename GraphType::Link;
        using difference_type = std::ptrdiff_t;
        using pointer = const value_type*;
        using reference = const value_type&;

        explicit GlobalLinkWalker(const GraphType* g) : current_index_(0) {
            if (!g) return;
            auto n = g->nodes_count();
            for (std::size_t u = 0; u < n; ++u) {
                for (std::size_t v = u + 1; v < n; ++v) {
                    if (g->linked(u, v)) {
                        cached_links_.emplace_back(u, v);
                    }
                }
            }
        }

        GlobalLinkWalker(const GraphType* g, bool end_tag) {
            if (!g) return;
            auto n = g->nodes_count();
            for (std::size_t u = 0; u < n; ++u) {
                for (std::size_t v = u + 1; v < n; ++v) {
                    if (g->linked(u, v)) {
                        cached_links_.emplace_back(u, v);
                    }
                }
            }
            current_index_ = cached_links_.size();
        }

        reference operator*() const {
            return cached_links_[current_index_];
        }
        pointer operator->() const {
            return &cached_links_[current_index_];
        }

        GlobalLinkWalker& operator++() {
            ++current_index_;
            return *this;
        }
        GlobalLinkWalker operator++(int) {
            auto tmp = *this;
            ++(*this);
            return tmp;
        }
        GlobalLinkWalker& operator--() {
            --current_index_;
            return *this;
        }
        GlobalLinkWalker operator--(int) {
            auto tmp = *this;
            --(*this);
            return tmp;
        }

        bool operator==(const GlobalLinkWalker& other) const {
            return current_index_ == other.current_index_;
        }
        bool operator!=(const GlobalLinkWalker& other) const {
            return !(*this == other);
        }
    };

}