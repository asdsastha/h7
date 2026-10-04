// LeetCode 146: LRU Cache. https://leetcode.com/problems/lru-cache/
// get/put in O(1). Build: g++ -std=c++20 -Wall -Wextra -O2 -fsanitize=address,undefined lru_cache.cpp -o /tmp/lru && /tmp/lru

#include <cassert>
#include <cstdio>

class LRUCache {
public:
    explicit LRUCache(int capacity) {}

    int get(int key) { return -1; }

    void put(int key, int value) {}

private:
};

// ---------------------------------------------------------------- tests
int main() {
    {   // LeetCode example
        LRUCache c(2);
        c.put(1, 1); c.put(2, 2);
        assert(c.get(1) == 1);
        c.put(3, 3);                 // evicts 2
        assert(c.get(2) == -1);
        c.put(4, 4);                 // evicts 1
        assert(c.get(1) == -1);
        assert(c.get(3) == 3);
        assert(c.get(4) == 4);
    }
    {   // update refreshes recency
        LRUCache c(2);
        c.put(1, 1); c.put(2, 2);
        c.put(1, 10);
        c.put(3, 3);                 // evicts 2, not 1
        assert(c.get(1) == 10);
        assert(c.get(2) == -1);
    }
    {   // capacity 1
        LRUCache c(1);
        c.put(1, 1); c.put(2, 2);
        assert(c.get(1) == -1);
        assert(c.get(2) == 2);
    }
    {   // miss on empty
        LRUCache c(3);
        assert(c.get(42) == -1);
    }
    std::puts("all tests passed");
}
