#pragma once
#include <vector>
#include <iostream>
#include <algorithm>
#include <iterator>

template<typename T>
void BucketSort(T first, T last){
    if (first == last) return;

    size_t n = std::distance(first, last);
    if (n == 0) return;
    using ValueType = typename std::iterator_traits<T>::value_type;
    std::vector<std::vector<ValueType>> buckets (n);
    for(auto it = first; it != last; it++){
        size_t BucketIndex = static_cast<size_t>(*it*n);
        if(BucketIndex >= n) BucketIndex = n-1;
        buckets[BucketIndex].push_back(*it);
    }

    for(auto &bucket:buckets){
        if(!bucket.empty()){
            std::sort(bucket.begin(),bucket.end());
        }
    }

    auto OutIt = first;
    for (const auto& bucket : buckets) {
        for (const auto& val : bucket) {
            *OutIt++ = val;
        }
    }
}

template<typename T>
void BucketSort(std::vector<T> &vec){
    BucketSort(std::begin(vec),std::end(vec));
}

template<typename T,size_t N>
void BucketSort(T (&arr)[N]){
    BucketSort(std::begin(arr),std::end(arr));
}
