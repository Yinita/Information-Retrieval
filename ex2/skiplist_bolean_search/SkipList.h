#pragma once
#include <iostream>
#include <list>
#include <set>
#include <vector>
#include <ctime>
#include <cstdlib>
#include <cmath>

#define LAYER 2


class SkipList {
public:
    SkipList();
    void insert(int value);
    void renew();
    static SkipList boolean_and(const SkipList& lhs, const SkipList& rhs);
    static SkipList boolean_and_ORI(const SkipList& lhs, const SkipList& rhs);
    static SkipList boolean_and_OPT(const SkipList& lhs, const SkipList& rhs);
    static SkipList boolean_or(const SkipList& lhs, const SkipList& rhs);
    void print(int mod);
    std::set<int> turn_into_set();
    int size;

private:
    struct Node {
        int value;
        std::vector<Node*> forward;
        Node(int value, int level = LAYER);
    };

    int levels;
    Node* head;
};