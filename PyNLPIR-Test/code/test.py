import sys
import pynlpir
import importlib
from Splitwords import split

importlib.reload(sys)

pynlpir.open()

s = '我想要一个直方图。'

pynlpir.nlpir.ImportUserDict('userdic.txt'.encode('utf-8'))

segments1 = pynlpir.segment(s.encode('utf-8'),pos_tagging=True,pos_english=True,pos_names=None)
segments2 = pynlpir.get_key_words(s.encode('utf-8'),weighted=True)

dict1 = split.build_dic(segments1)
dict2 = split.build_dic(segments2)
dict3 = split.rebuild_dic(dict1,dict2)


print(split.kwd_pic2map(dict3))
print(split.kwd_verb2map(dict3))
print(split.kwd_ad2map(dict1))
print(split.kwd_encoding2map(dict1))
