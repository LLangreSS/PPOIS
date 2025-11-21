#include <UnitTest++.h>
#include <vector>
#include <string>
#include <stdexcept>
#include <sstream>
#include <algorithm>
#include "Graph.h"

TEST(Graph_DefaultConstructor_CreatesEmptyGraph) {
    Graph<int> g;
            CHECK(g.empty());
            CHECK_EQUAL(0, g.nodes_count());
            CHECK_EQUAL(0, g.links_count());
}

TEST(Graph_AppendNode_AddsVertexAndReturnsId) {
    Graph<std::string> g;
    auto id0 = g.append_node("A");
    auto id1 = g.append_node("B");
            CHECK_EQUAL(0, id0);
            CHECK_EQUAL(1, id1);
            CHECK_EQUAL(2, g.nodes_count());
            CHECK_EQUAL("A", g.fetch_value(id0));
            CHECK_EQUAL("B", g.fetch_value(id1));
}

TEST(Graph_Connect_AddsEdge) {
    Graph<int> g;
    auto a = g.append_node(10);
    auto b = g.append_node(20);
    g.connect(a, b);
            CHECK_EQUAL(1, g.links_count());
            CHECK(g.linked(a, b));
            CHECK_EQUAL(1, g.node_degree(a));
            CHECK_EQUAL(1, g.node_degree(b));
}

TEST(Graph_Sever_RemovesEdge) {
    Graph<int> g;
    auto a = g.append_node(1);
    auto b = g.append_node(2);
    g.connect(a, b);
    g.sever(a, b);
            CHECK_EQUAL(0, g.links_count());
            CHECK(!g.linked(a, b));
}

TEST(Graph_EraseNode_RemovesVertexAndEdges) {
    Graph<int> g;
    auto a = g.append_node(1);
    auto b = g.append_node(2);
    auto c = g.append_node(3);
    g.connect(a, b);
    g.connect(a, c);
    g.erase_node(a);
            CHECK_EQUAL(2, g.nodes_count());
            CHECK_EQUAL(0, g.links_count());
            CHECK_EQUAL(2, g.fetch_value(0));
            CHECK_EQUAL(3, g.fetch_value(1));
}

TEST(Graph_MainIterators_BeginEnd) {
    Graph<std::string> g;
    g.append_node("A");
    g.append_node("B");
    g.append_node("C");

    std::vector<std::string> forward, reverse;
    for (auto it = g.begin(); it != g.end(); ++it) {
        forward.push_back(*it);
    }
    for (auto it = g.rbegin(); it != g.rend(); ++it) {
        reverse.push_back(*it);
    }

    std::vector<std::string> expected_fwd = {"A", "B", "C"};
    std::vector<std::string> expected_rev = {"C", "B", "A"};
            CHECK(forward == expected_fwd);
            CHECK(reverse == expected_rev);
}

TEST(Graph_NeighborIterators_ForwardAndReverse) {
    Graph<int> g;
    auto center = g.append_node(0);
    auto a = g.append_node(1);
    auto b = g.append_node(2);
    auto c = g.append_node(3);
    g.connect(center, a);
    g.connect(center, b);
    g.connect(center, c);

    std::vector<Graph<int>::NodeIndex> fwd;
    for (auto it = g.neighbors_begin(center); it != g.neighbors_end(center); ++it) {
        fwd.push_back(*it);
    }

    std::vector<Graph<int>::NodeIndex> rev;
    for (auto it = g.neighbors_rbegin(center); it != g.neighbors_rend(center); ++it) {
        rev.push_back(*it);
    }

    std::vector<Graph<int>::NodeIndex> expected_fwd = {1, 2, 3};
    std::vector<Graph<int>::NodeIndex> expected_rev = {3, 2, 1};
            CHECK(fwd == expected_fwd);
            CHECK(rev == expected_rev);
}

TEST(Graph_IncidentLinkIterators_ForwardAndReverse) {
    Graph<int> g;
    auto v = g.append_node(10);
    auto a = g.append_node(20);
    auto b = g.append_node(30);
    g.connect(v, a);
    g.connect(v, b);

    std::vector<Graph<int>::Link> fwd;
    for (auto it = g.incident_links_begin(v); it != g.incident_links_end(v); ++it) {
        fwd.push_back(*it);
    }
    std::vector<Graph<int>::Link> rev;
    for (auto it = g.incident_links_rbegin(v); it != g.incident_links_rend(v); ++it) {
        rev.push_back(*it);
    }
            CHECK_EQUAL(2, fwd.size());
            CHECK_EQUAL(0, fwd[0].first); CHECK_EQUAL(1, fwd[0].second);
            CHECK_EQUAL(0, fwd[1].first); CHECK_EQUAL(2, fwd[1].second);

            CHECK_EQUAL(2, rev.size());
            CHECK_EQUAL(0, rev[0].first); CHECK_EQUAL(2, rev[0].second);
            CHECK_EQUAL(0, rev[1].first); CHECK_EQUAL(1, rev[1].second);
}

TEST(Graph_GlobalLinkIterator_EraseEdge) {
    Graph<int> g;
    g.append_node(1);
    g.append_node(2);
    g.connect(0, 1);

    auto it = g.links_begin();
    g.erase(it);

            CHECK_EQUAL(0, g.links_count());
            CHECK(!g.linked(0, 1));
}

TEST(Graph_NeighborIterators_Empty) {
    Graph<int> g;
    auto v = g.append_node(1);
            CHECK(g.neighbors_begin(v) == g.neighbors_end(v));
            CHECK(g.neighbors_rbegin(v) == g.neighbors_rend(v));
}

TEST(Graph_GlobalLinkIterators_EmptyGraph) {
    Graph<int> g;
            CHECK(g.links_begin() == g.links_end());
            CHECK(g.links_rbegin() == g.links_rend());
}

TEST(Graph_GlobalLinkIterators_NoEdges) {
    Graph<int> g;
    g.append_node(1);
    g.append_node(2);
            CHECK(g.links_begin() == g.links_end());
            CHECK(g.links_rbegin() == g.links_rend());
}


TEST(Graph_Comparison_Operators) {
    Graph<std::string> g1, g2;
    g1.append_node("A");
    g2.append_node("A");
            CHECK(g1 == g2);

    g2.append_node("B");
            CHECK(g1 != g2);
            CHECK(g1 < g2);
}

TEST(Graph_OStreamOperator) {
    Graph<std::string> g;
    g.append_node("X");
    g.append_node("Y");
    g.connect(0, 1);

    std::ostringstream oss;
    oss << g;
    std::string s = oss.str();

            CHECK(s.find("nodes=2") != std::string::npos);
            CHECK(s.find("links=1") != std::string::npos);
            CHECK(s.find("X") != std::string::npos);
            CHECK(s.find("Y") != std::string::npos);
}

TEST(Graph_Connect_ThrowsOnSelfLoop) {
    Graph<int> g;
    auto a = g.append_node(1);
            CHECK_THROW(g.connect(a, a), std::invalid_argument);
}

TEST(Graph_FetchValue_ThrowsOnInvalidId) {
    Graph<int> g;
            CHECK_THROW(g.fetch_value(0), std::out_of_range);
    g.append_node(1);
            CHECK_THROW(g.fetch_value(1), std::out_of_range);
}

TEST(Graph_ReverseIterators_WorkWithStdReverse) {
    Graph<int> g;
    g.append_node(10);
    g.append_node(20);
    g.append_node(30);

    std::vector<int> vals;
    for (auto it = g.rbegin(); it != g.rend(); ++it) {
        vals.push_back(*it);
    }
    std::vector<int> expected = {30, 20, 10};
            CHECK(vals == expected);
}
TEST(Graph_Sever_NothingIfEdgeNotExists) {
    Graph<int> g;
    auto a = g.append_node(1);
    auto b = g.append_node(2);
    g.sever(a, b);
            CHECK_EQUAL(0, g.links_count());
}
TEST(Graph_Linked_CoversAllBounds) {
    Graph<int> g;
    g.append_node(1);
            CHECK(!g.linked(0, 1));
            CHECK(!g.linked(1, 0));
            CHECK(!g.linked(1, 1));
            CHECK(!g.linked(100, 200));
}
TEST(Graph_Connect_DuplicateInt) {
    Graph<int> g;
    auto a = g.append_node(1);
    auto b = g.append_node(2);
    g.connect(a, b);
    g.connect(a, b);
            CHECK_EQUAL(1, g.links_count());
}

TEST(Graph_Connect_DuplicateString) {
    Graph<std::string> g;
    auto a = g.append_node("A");
    auto b = g.append_node("B");
    g.connect(a, b);
    g.connect(b, a);
            CHECK_EQUAL(1, g.links_count());
}
TEST(Graph_ValidateNode_String_Throws) {
    Graph<std::string> g;
    g.append_node("A");
            CHECK_EQUAL("A", g.fetch_value(0));
            CHECK_THROW(g.fetch_value(1), std::out_of_range);
}
TEST(Graph_EraseNode_CoversAllBranches) {
    Graph<int> g;
    auto a = g.append_node(1);
    auto b = g.append_node(2);
    auto c = g.append_node(3);
    g.connect(a, b);
    g.connect(b, c);

    g.erase_node(b);
            CHECK_EQUAL(2, g.nodes_count());
            CHECK_EQUAL(0, g.links_count());
}
TEST(Graph_NodeEquality_DifferentAdjacency) {
    Graph<std::string> g1, g2;
    auto a1 = g1.append_node("X");
    auto b1 = g1.append_node("Y");
    g1.connect(a1, b1);

    auto a2 = g2.append_node("X");
    auto b2 = g2.append_node("Y");

            CHECK(g1 != g2);
}
TEST(Graph_Connect_DuplicateStringEdge) {
    Graph<std::string> g;
    auto a = g.append_node("A");
    auto b = g.append_node("B");
    g.connect(a, b);
            CHECK_EQUAL(1, g.links_count());

    g.connect(a, b);
            CHECK_EQUAL(1, g.links_count());
    g.connect(b, a);
            CHECK_EQUAL(1, g.links_count());
}
TEST(Graph_EraseNode_CoversAllBranchesInEraseNode) {
    Graph<int> g;

    g.append_node(0);
    g.append_node(1);
    g.append_node(2);
    g.append_node(3);
    g.append_node(4);

    g.connect(0, 1);
    g.connect(1, 2);
    g.connect(2, 3);

    g.erase_node(2);

            CHECK_EQUAL(4, g.nodes_count());
            CHECK_EQUAL(1, g.links_count());
            CHECK(g.linked(0, 1));
            CHECK(!g.linked(1, 2));

    g.erase_node(3);
            CHECK_EQUAL(3, g.nodes_count());
            CHECK_EQUAL(1, g.links_count());
}
int main() {
    return UnitTest::RunAllTests();
}