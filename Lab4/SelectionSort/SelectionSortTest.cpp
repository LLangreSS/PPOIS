#include <UnitTest++.h>
#include <vector>
#include <string>
#include <iostream>
#include <utility>
#include "SelectionSort.h"
#include "Student.h"

SUITE(SelectionSortTest) {
    TEST (SelectionSort_EmptyVector) {
        std::vector<int> vec;
        SelectionSort(vec);
                CHECK_EQUAL(0, vec.size());
    }

    TEST (SelectionSort_SingleElementVector) {
        std::vector<int> vec = {42};
        SelectionSort(vec);
                CHECK_EQUAL(42, vec[0]);
    }

    TEST (SelectionSort_IntVector) {
        std::vector<int> vec = {5, 2, 8, 1, 9};
        SelectionSort(vec);
        std::vector<int> expected = {1, 2, 5, 8, 9};
                CHECK_ARRAY_EQUAL(expected.data(), vec.data(), vec.size());
    }

    TEST (SelectionSort_CStyleArray) {
        double arr[] = {3.14, 1.41, 2.71, 0.57};
        SelectionSort(arr);
        double expected[] = {0.57, 1.41, 2.71, 3.14};
        for (size_t i = 0; i < 4; ++i) {
                    CHECK_CLOSE(expected[i], arr[i], 1e-6);
        }
    }

    TEST (SelectionSort_StudentArray) {
        Student students[] = {
                Student("Alice", 88),
                Student("Bob", 95),
                Student("Charlie", 76),
                Student("Diana", 92)
        };
        SelectionSort(students);

                CHECK_EQUAL("Charlie", students[0].name);
                CHECK_EQUAL(76, students[0].score);

                CHECK_EQUAL("Alice", students[1].name);
                CHECK_EQUAL(88, students[1].score);

                CHECK_EQUAL("Diana", students[2].name);
                CHECK_EQUAL(92, students[2].score);

                CHECK_EQUAL("Bob", students[3].name);
                CHECK_EQUAL(95, students[3].score);
    }

    TEST (SelectionSort_StudentVector) {
        std::vector<Student> vec = {
                Student("Eve", 82),
                Student("Frank", 79),
                Student("Grace", 90)
        };
        SelectionSort(vec);

                CHECK_EQUAL("Frank", vec[0].name);
                CHECK_EQUAL(79, vec[0].score);

                CHECK_EQUAL("Eve", vec[1].name);
                CHECK_EQUAL(82, vec[1].score);

                CHECK_EQUAL("Grace", vec[2].name);
                CHECK_EQUAL(90, vec[2].score);
    }

    TEST (SelectionSort_Duplicates) {
        std::vector<int> vec = {3, 1, 4, 1, 5, 9, 2, 6, 5};
        SelectionSort(vec);
        std::vector<int> expected = {1, 1, 2, 3, 4, 5, 5, 6, 9};
                CHECK_ARRAY_EQUAL(expected.data(), vec.data(), vec.size());
    }

    TEST (SelectionSort_StringVector) {
        std::vector<std::string> vec = {"banana", "apple", "cherry"};
        SelectionSort(vec);
        std::vector<std::string> expected = {"apple", "banana", "cherry"};
                CHECK_ARRAY_EQUAL(expected.data(), vec.data(), vec.size());
    }
}
TEST(SelectionSort_EmptyCArray) {
    double arr[1];
    SelectionSort(arr, arr);
}

int main() {
    return UnitTest::RunAllTests();
}