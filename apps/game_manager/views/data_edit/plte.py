__author__ = 'Administrator'
import string
lst = ['1','4']
a = string.join(lst,'$$')
dic = {1:{23},4:5}
print len(dic)
print a
print a.split("ss")

for i in xrange(5):
    key_str = string.join(['has_reward_lst', str(i)],'$$')
    print key_str