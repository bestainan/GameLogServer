# -*- coding:utf-8 -*-
#
# head_lst = [
#     {'name': u'名称'},
#     {'name': u'当前可领取ID'},
#     {'name': u'下次充值可领取ID'},
# ]
# for i in xrange(1,31):
#     head_lst.append({'name': (u'第%s天' % (i))})
# print head_lst
# lst = [1,2]
# print lst[0]
row_dict = {'name':u'我是王八蛋','val_dic':[{'key_name':u'rrrrr','val_num':u'1'},{'key_name':u'rrrr1r','val_num':u'123423'}]}
# row_dict = {}
for i in row_dict['val_dic']:
    print i['key_name']
