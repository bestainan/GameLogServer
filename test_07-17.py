# # -*- coding: utf-8 -*-
# """
# 下面这个是一个有趣的例子，主要使用了deque的rotate方法来实现了一个无限循环
# 的加载动画
# """
# import sys
# import time
# from collections import deque
# fancy_loading = deque('>--------------------')
# while True:
#     print '\r%s' % ''.join(fancy_loading),
#     fancy_loading.rotate(1)
#     sys.stdout.flush()
#     time.sleep(0.08)
# # Result:
# # 一个无尽循环的跑马灯


# -*- coding: utf-8 -*-
"""
下面这个例子就是使用Counter模块统计一段句子里面所有字符出现次数
"""
from collections import Counter
s = '''A Counter is a dict subclass for counting hashable objects. It is an unordered collection where elements are stored as dictionary keys and their counts are stored as dictionary values. Counts are allowed to be any integer value including zero or negative counts. The Counter class is similar to bags or multisets in other languages.'''.lower()
c = Counter(s)
# 获取出现频率最高的5个字符
print c.most_common(1)
# Result:
