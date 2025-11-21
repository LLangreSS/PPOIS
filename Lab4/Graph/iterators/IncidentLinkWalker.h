#pragma once
#include <iterator>
#include <vector>
#include <utility>
#include <cstddef>

namespace graph_details {

    class IncidentLinkWalker {
        std::size_t source_;
        const std::vector<std::size_t>* adj_ref_;
        std::size_t step_;

    public:
        using iterator_category = std::bidirectional_iterator_tag;
        using value_type = std::pair<std::size_t, std::size_t>;
        using difference_type = std::ptrdiff_t;
        using pointer = void;
        using reference = value_type;

        IncidentLinkWalker(std::size_t src, const std::vector<std::size_t>* adj, std::size_t i)
                : source_(src), adj_ref_(adj), step_(i) {}

        reference operator*() const {
            return value_type{source_, (*adj_ref_)[step_]};
        }

        IncidentLinkWalker& operator++() {
            ++step_;
            return *this;
        }
        IncidentLinkWalker operator++(int) {
            IncidentLinkWalker tmp = *this;
            ++(*this);
            return tmp;
        }
        IncidentLinkWalker& operator--() {
            --step_;
            return *this;
        }
        IncidentLinkWalker operator--(int) {
            IncidentLinkWalker tmp = *this;
            --(*this);
            return tmp;
        }

        bool operator==(const IncidentLinkWalker& other) const {
            return step_ == other.step_ && adj_ref_ == other.adj_ref_;
        }
        bool operator!=(const IncidentLinkWalker& other) const {
            return !(*this == other);
        }
    };

}