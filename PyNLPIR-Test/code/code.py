import sys
import pynlpir
import codecs
import importlib
from difflib import SequenceMatcher

importlib.reload(sys)
#转换编码问题
def  ReadFile(filePath,encoding='utf-8'):
    with codecs.open(filePath,'r',encoding) as f:
        return f.read()

def WriteFile(filePath,content,encoding='gbk'):
    with codecs.open(filePath,'w',encoding) as f:
        f.write(content)

def UTF8_to_GBK(src,dst):
    content = ReadFile(src,encoding='utf-8')
    WriteFile(dst,content,encoding='gbk')
#可能会用到的转换编码的函数

def similarity(str1,str2):
    return SequenceMatcher(None,str1,str2).ratio()
#相似字符串匹配度函数

pynlpir.open()
#初始化PyNLPIR的API
s = '绘制一个中国石油大学的人流量的条形统计图。'\
    '请帮我绘制一个拥有暑期小学期的大学的散点图。'\
    '我需要一个展示石油大学内5家咖啡店销售额的饼状图。'\
    '绘制本研班内的男女比例图。'\
    '绘制本人各科考试成绩的柱状图。'
#给定的输入指令

# in_words= input()
# with open('userdic.txt','r',encoding='utf-8') as f:
#     lines = f.readlines()
#     in_words = in_words + '\n'
#     if in_words not in lines:
#         with open('userdic.txt','a',encoding='utf-8') as f:
#             f.write(in_words)
#以上注释的部分为添加用户词典的程序

pynlpir.nlpir.ImportUserDict('userdic.txt'.encode('utf-8'))
#导入用户词典

segments1 = pynlpir.segment(s.encode('utf-8'),pos_tagging=True,pos_english=True,pos_names=None)
segments2 =  pynlpir.get_key_words(s.encode('utf-8'),weighted=True)
#segments1用于分词，segments2用于获取关键词

print(segments1)
print(segments2)

key1 = []
val1 = []
#将分词后的句子里分好的词与其对应的词性对应，同时构建字典

for split_words in segments1:
    key1.append(split_words[0])
    val1.append(split_words[1])
user_input_attribute =  dict(zip(key1,val1))
print(user_input_attribute)
#字典构建：分词与对应分词的词性

key2 = []
val2 = []
#将关键词与其对应的权重构建一个字典

for split_words in segments2:
    key2.append(split_words[0])
    val2.append(split_words[1])
keywords_weight =  dict(zip(key2,val2))
keywords_weight_copy = keywords_weight.copy()
print(keywords_weight)
#字典构建：关键词与其权重

for key in keywords_weight_copy:
    keywords_weight_copy[key] = user_input_attribute[key]
keywords_attribute = keywords_weight_copy
print(keywords_attribute)
#构建一个关键词与词性的字典备用

# for segment in segments1:
#     print(segment[0],'\t',segment[1])
#
# for segment in segments2:
#    print(segment[0],'\t',segment[1])
#改变segments的输出形式，易于查看输出结果

pic_type = ['条形图','比例图','散点图','饼图','柱图']
#预设的图像类型
input_pic_type = []
keywords_list = list(keywords_attribute.keys())
for i in range(0,len(keywords_list),1):
    if keywords_attribute[keywords_list[i]] == 'nz':
        input_pic_type.append(keywords_list[i])
# nz词性表示是pic_type里的预设类型
print(input_pic_type)
final_pic_type = []
#最终输出给绘图API的图像类型名称
for s1 in input_pic_type:
    for s2 in pic_type:
        if similarity(s1,s2) >= 0.5:
            final_pic_type.append(s2)
            break
        #关键字相似度判断，减少预设的工作量
        else:
            continue
print(final_pic_type)

pynlpir.close()