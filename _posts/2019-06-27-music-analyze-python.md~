---
layout: post
title: 用Python实现自己下载音乐的统计
date: 2017-03-05 15:23:44 +0800
categories: [code]
tags: [Python]
---

今天看Python实例，学习了如何对文件进行操作，突然想把自己网易云音乐下载到本地的歌曲名单写到一个txt中，看看具体情况。当然，我现在肯定无法做到直接去网易云音乐上爬取，就做个最简单的吧，嘻嘻^-^。

## 代码实现

```python
import os
def split_songs_name(s) :
    '''
    拆分歌曲名，去掉歌手和一些其他信息，只保留歌曲名
    :param s: 歌曲文件名
    :return: 歌曲名
    '''
    if isinstance(s,str) :
        if s.find('-') :
            return s.split('-')[-1].strip()
        else:
            return s
def get_all_mp3(path) :
    '''
    获取指定目录下所有的.mp3文件，存入一个list中
    :param path: 指定路径
    :return: 歌曲名list
    '''
    songs_list=[]
    for f in os.listdir(path) :
        file_path=os.path.join(path,f)
        if os.path.isfile(file_path) and    os.path.splitext(file_path)[1]=='.mp3':
            songs_list.append(split_songs_name(os.path.basename(file_path).split('.')[0]))
        elif os.path.isdir(file_path) :
            get_all_mp3(file_path)
    return songs_list
songs_list=get_all_mp3(r'D:\网易云音乐')
#指定路径
with open(r'D:\song.txt','w',encoding='utf-8') as  f:
    '''
    写入指定的txt文件中
    '''
    for s in songs_list:
        f.write(s+'\n')

```

 这些就是今天的小收获了，python注重简洁高效，我这里还有很多功能无法实现，如：没有考虑歌曲名存在多个'-'划分的情况；无法查询歌曲所属专辑、发行时间等。希望自己以后能多多改善！
 哈哈，前辈们说学编程得多动手，今天动了一下小手，再说一下接下来的目标：用Python爬取豆瓣电影并输出Excel格式的文件，加油，fighting！
