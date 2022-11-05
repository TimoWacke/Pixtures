# 👇️ Old import for versions older than Python3.10

# ⛔️ AttributeError: module 'collections' has no attribute 'MutableMapping'
import collections.abc
print(collections.MutableMapping)

#👇️ New import for versions Python3.10+

# ✅ <class 'collections.abc.MutableMapping'>
print(collections.abc.MutableMapping)