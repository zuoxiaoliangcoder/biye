# -*- coding: utf-8 -*-
'''

@author: shawn
'''
from __future__ import division
from elasticsearch import Elasticsearch, client
import math
# -*- coding: utf-8 -*-
# 核心计算算法
def TF_IDF_Calute(*words):
    es = Elasticsearch()
    indices = client.IndicesClient(es)
    fenci_word = indices.analyze(text='我的天啊这是什么鬼东西啊', analyzer='ik')
    for i in fenci_word['tokens']:
        print i['token'], '  '
    print fenci_word, type(fenci_word)
    data = '.'
    word_in_afile_stat={}
    word_in_allfiles_stat={}
    files_num=0 
    # 每一行的data 由两部分组成 book_index: word1, word1 . 这些word表示书籍摘要进行分词处理后的结果
    while(data!=""):
        text = 
        #data = 
        data_temp_1=data.split(":") # 得到的是一个列表 [0] 表示book_index; [1]是分词列表   
        data_temp_2=data_temp_1[1].split(",")#key words of a file
        """
        for word in data_temp_2:
            print word
            print "\n"
        """
        
        file_name=data_temp_1[0]
        data_temp_len=len(data_temp_2)
        files_num+=1
        #print data_temp_2
        for word in words:
            if word in data_temp_2:
                # 所有的文档中出现某个关键词的次数, 这个值不会大于文档总数
                if not word_in_allfiles_stat.has_key(word):
                    word_in_allfiles_stat[word] = 1
                else: 
                    word_in_allfiles_stat[word] += 1
               #记录某本书中出现 匹配关键词的 次数和该 书籍所有的分词数量 
                if not word_in_afile_stat.has_key(file_name):
                    word_in_afile_stat[file_name]={}
                if not word_in_afile_stat[file_name].has_key(word):
                    word_in_afile_stat[file_name][word]=[]
                    word_in_afile_stat[file_name][word].append(data_temp_2.count(word))
                    word_in_afile_stat[file_name][word].append(data_temp_len)
        data=data_source.readline()
    data_source.close()
    # 公式计算
    if (word_in_afile_stat) and (word_in_allfiles_stat) and (files_num !=0):
        TF_IDF_result={}
        for filename in word_in_afile_stat.keys():
            TF_IDF_result[filename]={}
            for word in word_in_afile_stat[filename].keys():
                word_n = word_in_afile_stat[filename][word][0] # 某本书中搜索关键词的 次数越大,权重越大
                word_sum = word_in_afile_stat[filename][word][1] # 分词数量
                with_word_sum = word_in_allfiles_stat[word] # 这个关键词在 其它书籍中出现的次数, 在一本书中出现就加上1 
                # 核心公式的计算
                TF_IDF_result[filename][word] = ((word_n/word_sum))*(math.log10(files_num/with_word_sum))
        TF_IDF_total={}
        # 有多个关键字的情况下, 将每一个的 result进行求和
        for filename in TF_IDF_result.keys():
            TF_IDF_total[filename] = reduce(lambda x,y:x+y, TF_IDF_result[filename].values())       
        
        result_temp = sorted(TF_IDF_total.iteritems(),key=lambda x:x[1],reverse=True)
        return result_temp 
if __name__ == '__main__':
    TF_IDF_Calute('JAVA入门')
