#pragma once
#include <vector>
#include <iterator>
#include <utility>

template<typename RandomIt>
void SelectionSort(RandomIt first, RandomIt last) {
    if (first == last) return;
    for (auto it = first; it != last; ++it) {
        auto MinIt = it;
        for (auto jt = std::next(it); jt != last; ++jt) {
            if (*jt < *MinIt) {
                MinIt = jt;
            }
        }
        if (MinIt != it) {
            using std::swap;
            swap(*MinIt, *it);
        }
    }
}

template<typename T>
void SelectionSort(std::vector<T>& vec) {
    SelectionSort(vec.begin(), vec.end());
}

template<typename T, size_t N>
void SelectionSort(T (&arr)[N]) {
    SelectionSort(std::begin(arr), std::end(arr));
}