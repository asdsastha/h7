"""LeetCode 146: LRU Cache. https://leetcode.com/problems/lru-cache/

Design a cache with a fixed capacity:
  get(key) -> value, or -1 if the key is missing; marks the key as most recently used
  put(key, value) inserts or updates the key; if over capacity, evicts the least recently used key
Both operations must run in O(1) time.

Run: pytest lru_cache.py -q
"""
from __future__ import annotations

import logging
from enum import Enum

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class Cache:

    class STATUS(Enum):
        SUCCESS = 0
        FAILURE = -1
        ERROR_CACHE_FULL = -2
        ERROR_CACHE_EMPTY = -3
        
    def __init__(self, capacity: int):
        self._capacity = capacity
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def data(self):
        data = {}
        current = self.head
        while current.next is not self.tail:
            current = current.next
            data[current.key] = current.value
        return data
    
    def capacity(self) -> int:
        return self._capacity

    def is_full(self) -> bool:
        return len(self.data()) >= self._capacity

    def is_empty(self) -> bool:
        return len(self.data()) == 0

    def size(self) -> int:
        return len(self.data())

    def clear(self) -> None:
        self.head.next = self.tail
        self.tail.prev = self.head
        return Cache.STATUS.SUCCESS

    def _is_present(self, key: int) -> bool:
        data = self.data()
        return key in data
    
    def _remove(self, node: Node) -> None:
        if self.is_empty():
            return Cache.STATUS.ERROR_CACHE_EMPTY
        pnode = node.prev
        nnode = node.next
        pnode.next = nnode
        nnode.prev = pnode
        return Cache.STATUS.SUCCESS

    def _append(self, node: Node) -> Cache.STATUS:
        if self.is_full():
            return Cache.STATUS.ERROR_CACHE_FULL        
        pnode = self.tail.prev
        node.prev = pnode
        pnode.next = node
        node.next = self.tail 
        self.tail.prev = node
        return Cache.STATUS.SUCCESS
    
    def _get_node(self, key: int) -> Node:
        current = self.head.next
        while current is not self.tail:
            if current.key == key:
                return current
            current = current.next
        return None

class LRUCache(Cache):
    def __init__(self, capacity: int):
        super().__init__(capacity)
        
    def _touch(self, node: Node):
        self._remove(node)
        self._append(node)

    def get(self, key: int) -> int:
        value = -1
        if self._is_present(key):
            node = self._get_node(key)
            self._touch(node)
            value = node.value
        return value

    def put(self, key: int, value: int) -> None:
        if self._is_present(key):
            node = self._get_node(key)
            node.value = value
            self._touch(node)
        else:
            node = Node(key, value)
            status = self._append(node)
            if status == Cache.STATUS.ERROR_CACHE_FULL:
                self._remove(self.head.next)
                self._append(node)


# ---------------------------------------------------------------- tests
def test_leetcode_example():
    logger.info("Running test_leetcode_example")
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    logger.info("State after initial puts: %s", c.data())
    assert c.get(1) == 1
    c.put(3, 3)            # evicts 2
    logger.info("State after put(3, 3): %s", c.data())
    assert c.get(2) == -1
    c.put(4, 4)            # evicts 1
    logger.info("State after put(4, 4): %s", c.data())
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4
    logger.info("test_leetcode_example passed")


def test_update_refreshes_recency():
    logger.info("Running test_update_refreshes_recency")
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    logger.info("State after initial puts: %s", c.data())
    c.put(1, 10)           # update moves 1 to the most recently used slot
    logger.info("State after updating key 1: %s", c.data())
    c.put(3, 3)            # evicts 2, not 1
    logger.info("State after put(3, 3): %s", c.data())
    assert c.get(1) == 10
    assert c.get(2) == -1
    logger.info("test_update_refreshes_recency passed")


def test_capacity_one():
    logger.info("Running test_capacity_one")
    c = LRUCache(1)
    c.put(1, 1)
    logger.info("State after put(1, 1): %s", c.data())
    c.put(2, 2)
    logger.info("State after put(2, 2): %s", c.data())
    assert c.get(1) == -1
    assert c.get(2) == 2
    logger.info("test_capacity_one passed")


def test_get_miss_on_empty():
    logger.info("Running test_get_miss_on_empty")
    result = LRUCache(3).get(42)
    logger.info("Empty cache get(42) result: %s", result)
    assert result == -1
    logger.info("test_get_miss_on_empty passed")

def main():
    test_leetcode_example()
    test_update_refreshes_recency()
    test_capacity_one()
    test_get_miss_on_empty()

if __name__ == "__main__":
    main()