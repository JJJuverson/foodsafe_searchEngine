from scrapy import cmdline
import sys
import os
sys.path.append(os.path.join(os.getcwd())) #给Python解释器，添加模块新路径 ,将main.py文件所在目录添加到Python解释器
cmdline.execute(['scrapy', 'crawl', 'foodmate.py','--nolog'])