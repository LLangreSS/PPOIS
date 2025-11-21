#include "BucketSort.h"
#include "Score.h"
#include <UnitTest++.h>
#include <vector>
#include <array>
#include <algorithm>
#include <random>
#include <iostream>

template<typename ForwardIt>
bool IsSorted(ForwardIt first, ForwardIt last) {
    return std::is_sorted(first, last);
}

SUITE(BucketSortTest) {

    TEST(Float_ValueEqualToOne) {
        std::vector<float> v = {0.2f, 1.0f, 0.5f};
        BucketSort(v);
                CHECK(std::is_sorted(v.begin(), v.end()));
    }

    TEST(Float_ValueGreaterThanOne) {
        std::vector<float> v = {0.1f, 1.5f, 0.3f};
        BucketSort(v);
                CHECK(std::is_sorted(v.begin(), v.end()));
    }

    TEST(Float_AllOnes) {
        std::vector<float> v = {1.0f, 1.0f, 1.0f};
        BucketSort(v);
                CHECK(std::is_sorted(v.begin(), v.end()));
    }

    TEST(Score_ValueEqualToOne) {
        std::vector<Score> v = {Score(0.4), Score(1.0), Score(0.2)};
        BucketSort(v);
                CHECK(std::is_sorted(v.begin(), v.end()));
    }

    TEST(Float_EmptyVector) {
        std::vector<float> v;
        BucketSort(v);
                CHECK(v.empty());
    }

    TEST(Float_SingleElement) {
        std::vector<float> v = {0.5f};
        BucketSort(v);
                CHECK_EQUAL(1, v.size());
                CHECK_EQUAL(0.5f, v[0]);
    }

    TEST(Float_AlreadySorted) {
        std::vector<float> v = {0.1f, 0.2f, 0.3f, 0.4f, 0.5f};
        std::vector<float> expected = v;
        BucketSort(v);
                CHECK_ARRAY_EQUAL(expected.data(), v.data(), v.size());
                CHECK(IsSorted(v.begin(), v.end()));
    }

    TEST(Float_ReverseSorted) {
        std::vector<float> v = {0.9f, 0.7f, 0.5f, 0.3f, 0.1f};
        BucketSort(v);
                CHECK(IsSorted(v.begin(), v.end()));
    }

    TEST(Float_RandomOrder) {
        std::vector<float> v = {0.42f, 0.32f, 0.33f, 0.52f, 0.37f, 0.47f, 0.51f};
        BucketSort(v);
                CHECK(IsSorted(v.begin(), v.end()));
    }

    TEST(Float_Duplicates) {
        std::vector<float> v = {0.5f, 0.3f, 0.5f, 0.1f, 0.3f, 0.5f};
        BucketSort(v);
                CHECK(IsSorted(v.begin(), v.end()));
    }

    TEST(Float_CArray) {
        float arr[] = {0.89f, 0.23f, 0.67f, 0.12f, 0.91f, 0.05f};
        const size_t n = sizeof(arr) / sizeof(arr[0]);
        std::vector<float> expected(arr, arr + n);
        std::sort(expected.begin(), expected.end());

        BucketSort(arr);

        CHECK_ARRAY_EQUAL(expected.data(), arr, n);
    }

    TEST(Double_RandomOrder) {
        std::vector<double> v = {0.42, 0.32, 0.33, 0.52, 0.37, 0.47, 0.51};
        BucketSort(v);
                CHECK(IsSorted(v.begin(), v.end()));
    }

    TEST(Score_EmptyVector) {
        std::vector<Score> v;
        BucketSort(v);
                CHECK(v.empty());
    }


    TEST(Score_RandomOrder) {
        std::vector<Score> v = {Score(0.42), Score(0.32), Score(0.33), Score(0.52), Score(0.37)};
        BucketSort(v);
                CHECK(is_sorted(v.begin(), v.end()));
    }

    TEST(Score_Duplicates) {
        std::vector<Score> v = {Score(0.5), Score(0.3), Score(0.5), Score(0.1)};
        BucketSort(v);
                CHECK(is_sorted(v.begin(), v.end()));
    }

    TEST(Float_EdgeValues) {
        std::vector<float> v = {0.0f, 0.999999f, 0.000001f, 0.5f};
        BucketSort(v);
                CHECK(is_sorted(v.begin(), v.end()));
    }
    TEST(CArray_WithOnePointZero) {
        float arr[] = {0.9f, 1.0f, 0.1f};
        BucketSort(arr);
                CHECK(std::is_sorted(std::begin(arr), std::end(arr)));
    }

    TEST(IteratorVersion_WithEdgeValues) {
        std::vector<float> v = {1.0f, 0.0f, 0.999999f, 1.2f};
        BucketSort(v.begin(), v.end());
                CHECK(std::is_sorted(v.begin(), v.end()));
    }

    TEST(Score_WithOnePointZero) {
        std::vector<Score> v = {Score(1.0), Score(0.99), Score(0.0)};
        BucketSort(v);
                CHECK(is_sorted(v.begin(), v.end()));
    }
}

int main() {
    return UnitTest::RunAllTests();
}