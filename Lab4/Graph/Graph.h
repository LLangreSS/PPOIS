#pragma once
#include <iostream>
#include <vector>
#include <algorithm>
#include <stdexcept>
#include <tuple>
#include <iterator>
#include <cstddef>
#include <sstream>

#include "iterators/NodeDataWalker.h"
#include "iterators/NeighborWalker.h"
#include "iterators/IncidentLinkWalker.h"
#include "iterators/GlobalLinkWalker.h"

template <typename T>
class Graph {
public:
    using value_type = T;
    using reference = T&;
    using const_reference = const T&;
    using pointer = T*;
    using const_pointer = const T*;
    using size_type = std::size_t;
    using NodeIndex = size_type;
    using Link = std::pair<NodeIndex, NodeIndex>;

private:
    struct Node {
        T payload;
        std::vector<NodeIndex> adj_pool;
        explicit Node(const T& val) : payload(val) {}
        
        bool operator==(const Node& other) const {
            return payload == other.payload && adj_pool == other.adj_pool;
        }
        bool operator<(const Node& other) const {
            return std::tie(payload, adj_pool) < std::tie(other.payload, other.adj_pool);
        }
    };

    std::vector<Node> nodes_pool;
    size_type links_total = 0;

    void validate_node_id(NodeIndex id) const {
        if (id >= nodes_pool.size()) {
            throw std::out_of_range("Node index is invalid");
        }
    }

    [[nodiscard]] bool link_exists_raw(NodeIndex a, NodeIndex b) const {
        const auto& pool = nodes_pool[a].adj_pool;
        auto pos = std::lower_bound(pool.cbegin(), pool.cend(), b);
        return (pos != pool.cend() && *pos == b);
    }

public:
    Graph() = default;
    ~Graph() = default;
    Graph(const Graph&) = default;
    Graph& operator=(const Graph&) = default;

    bool operator==(const Graph& other) const {
        return std::tie(nodes_pool, links_total) == std::tie(other.nodes_pool, other.links_total);
    }
    bool operator!=(const Graph& other) const { return !(*this == other); }
    bool operator<(const Graph& other) const {
        return std::tie(nodes_pool, links_total) < std::tie(other.nodes_pool, other.links_total);
    }
    bool operator>(const Graph& other) const { return other < *this; }
    bool operator<=(const Graph& other) const { return !(other < *this); }
    bool operator>=(const Graph& other) const { return !(*this < other); }

    [[nodiscard]] bool empty() const  { return nodes_pool.empty(); }
    void clear()  {
        nodes_pool.clear();
        links_total = 0;
    }

    [[nodiscard]] size_type nodes_count() const  { return nodes_pool.size(); }
    [[nodiscard]] size_type links_count() const  { return links_total; }
    [[nodiscard]] bool has_node(NodeIndex id) const  { return id < nodes_pool.size(); }

    const_reference fetch_value(NodeIndex id) const {
        validate_node_id(id);
        return nodes_pool[id].payload;
    }
    reference fetch_value(NodeIndex id) {
        validate_node_id(id);
        return nodes_pool[id].payload;
    }

    NodeIndex append_node(const T& value) {
        nodes_pool.emplace_back(value);
        return nodes_pool.size() - 1;
    }
    NodeIndex append_node(T&& value) {
        nodes_pool.emplace_back(std::move(value));
        return nodes_pool.size() - 1;
    }

    void connect(NodeIndex a, NodeIndex b) {
        validate_node_id(a);
        validate_node_id(b);
        if (a == b) {
            throw std::invalid_argument("Self-links are forbidden");
        }
        if (!link_exists_raw(a, b)) {
            auto& list_a = nodes_pool[a].adj_pool;
            auto& list_b = nodes_pool[b].adj_pool;
            list_a.insert(std::lower_bound(list_a.begin(), list_a.end(), b), b);
            list_b.insert(std::lower_bound(list_b.begin(), list_b.end(), a), a);
            ++links_total;
        }
    }

    void sever(NodeIndex a, NodeIndex b) {
        validate_node_id(a);
        validate_node_id(b);
        if (link_exists_raw(a, b)) {
            auto& list_a = nodes_pool[a].adj_pool;
            auto& list_b = nodes_pool[b].adj_pool;
            list_a.erase(std::lower_bound(list_a.begin(), list_a.end(), b));
            list_b.erase(std::lower_bound(list_b.begin(), list_b.end(), a));
            --links_total;
        }
    }

    void erase_node(NodeIndex id) {
        validate_node_id(id);
        const auto& current_adj = nodes_pool[id].adj_pool;
        for (NodeIndex neighbor : current_adj) {
            auto& its_adj = nodes_pool[neighbor].adj_pool;
            its_adj.erase(std::lower_bound(its_adj.begin(), its_adj.end(), id));
            --links_total;
        }
        nodes_pool.erase(nodes_pool.begin() + static_cast<std::ptrdiff_t>(id));

        for (auto& entry : nodes_pool) {
            for (auto& ref_id : entry.adj_pool) {
                if (ref_id > id) --ref_id;
            }
        }
    }

    [[nodiscard]] size_type node_degree(NodeIndex id) const {
        validate_node_id(id);
        return nodes_pool[id].adj_pool.size();
    }

    [[nodiscard]] bool linked(NodeIndex a, NodeIndex b) const {
        if (a >= nodes_pool.size() || b >= nodes_pool.size()) return false;
        return link_exists_raw(a, b);
    }

    template <typename Host, typename RefType, typename PtrType, typename ValueType>
    friend class graph_details::NodeDataWalker;

    friend class graph_details::NeighborWalker;
    friend class graph_details::IncidentLinkWalker;
    template <typename GraphType>
    friend class graph_details::GlobalLinkWalker;

    using iterator = graph_details::NodeDataWalker<Graph, T&, T*, T>;
    using const_iterator = graph_details::NodeDataWalker<const Graph, const T&, const T*, T>;
    using reverse_iterator = std::reverse_iterator<iterator>;
    using const_reverse_iterator = std::reverse_iterator<const_iterator>;

    iterator begin() { return iterator(this, 0); }
    iterator end() { return iterator(this, nodes_pool.size()); }
    const_iterator begin() const { return const_iterator(this, 0); }
    const_iterator end() const { return const_iterator(this, nodes_pool.size()); }
    const_iterator cbegin() const { return begin(); }
    const_iterator cend() const { return end(); }
    reverse_iterator rbegin() { return reverse_iterator(end()); }
    reverse_iterator rend() { return reverse_iterator(begin()); }
    const_reverse_iterator rbegin() const { return const_reverse_iterator(end()); }
    const_reverse_iterator rend() const { return const_reverse_iterator(begin()); }
    const_reverse_iterator crbegin() const { return rbegin(); }
    const_reverse_iterator crend() const { return rend(); }

    iterator erase(iterator pos) {
        NodeIndex id = pos.index();
        erase_node(id);
        return iterator(this, id);
    }

    using neighbor_iterator = graph_details::NeighborWalker;
    using const_neighbor_iterator = neighbor_iterator;
    using reverse_neighbor_iterator = std::reverse_iterator<neighbor_iterator>;

    neighbor_iterator neighbors_begin(NodeIndex v) const {
        validate_node_id(v);
        return neighbor_iterator(&nodes_pool[v].adj_pool, 0);
    }
    neighbor_iterator neighbors_end(NodeIndex v) const {
        validate_node_id(v);
        return neighbor_iterator(&nodes_pool[v].adj_pool, nodes_pool[v].adj_pool.size());
    }
    reverse_neighbor_iterator neighbors_rbegin(NodeIndex v) const {
        return reverse_neighbor_iterator(neighbors_end(v));
    }
    reverse_neighbor_iterator neighbors_rend(NodeIndex v) const {
        return reverse_neighbor_iterator(neighbors_begin(v));
    }

    using incident_link_iterator = graph_details::IncidentLinkWalker;
    using const_incident_link_iterator = incident_link_iterator;
    using reverse_incident_link_iterator = std::reverse_iterator<incident_link_iterator>;

    incident_link_iterator incident_links_begin(NodeIndex v) const {
        validate_node_id(v);
        return incident_link_iterator(v, &nodes_pool[v].adj_pool, 0);
    }
    incident_link_iterator incident_links_end(NodeIndex v) const {
        validate_node_id(v);
        return incident_link_iterator(v, &nodes_pool[v].adj_pool, nodes_pool[v].adj_pool.size());
    }
    [[nodiscard]] reverse_incident_link_iterator incident_links_rbegin(NodeIndex v) const {
        return reverse_incident_link_iterator(incident_links_end(v));
    }
    [[nodiscard]] reverse_incident_link_iterator incident_links_rend(NodeIndex v) const {
        return reverse_incident_link_iterator(incident_links_begin(v));
    }

    using global_link_iterator = graph_details::GlobalLinkWalker<const Graph>;
    using const_global_link_iterator = global_link_iterator;
    using reverse_global_link_iterator = std::reverse_iterator<global_link_iterator>;

    global_link_iterator links_begin() const {
        return global_link_iterator(this);
    }
    global_link_iterator links_end() const {
        return global_link_iterator(this, true);
    }
    reverse_global_link_iterator links_rbegin() const {
        return reverse_global_link_iterator(links_end());
    }
    reverse_global_link_iterator links_rend() const {
        return reverse_global_link_iterator(links_begin());
    }

    void erase(global_link_iterator it) {
        Link edge = *it;
        sever(edge.first, edge.second);
    }

    friend std::ostream& operator<<(std::ostream& os, const Graph& g) {
        os << "Graph(nodes=" << g.nodes_count()
           << ", links=" << g.links_count() << ")[";

        bool first = true;
        std::for_each(g.cbegin(), g.cend(), [&os, &first](const T& val) {
            if (!first) os << ", ";
            os << val;
            first = false;
        });
        os << "]";
        return os;
    }
};