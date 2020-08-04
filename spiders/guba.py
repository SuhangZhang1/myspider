import scrapy
import re
import json
import numpy as np
from scrapy import Request
from myspider.source_re import replace_tag
from myspider.source_re import user_data_re
from myspider.create_save import create_file
from myspider.comment import comment_data

class ItcastSpider(scrapy.Spider):
    name = 'guba'
    allowed_domains = ['http://guba.eastmoney.com,http://mguba.eastmoney.com,https://i.eastmoney.com']  # 爬取范围
    start_urls = ['http://guba.eastmoney.com/list,uslk,f_{}.html'.format(i) for i in np.arange(69,86, 1)]  # 起始页
    #69-86
    def source(self, response):
        ret1 = response.text
        res = r'<script>(.*?)</script>'
        mm = re.findall(res, ret1, re.S | re.M)  # 正则表达式提取数据
        # 避免下面三种情况报错
        a = mm[1][23:len(mm[1]) - 2]
        b = json.loads(a)
        # print(type(b))
        global false, null, true
        false = null = true = ''
        source_file = {}
        c = b["post"]
        source_file["post_id"] = c["post_id"]
        source_file["post_user"]={}
        source_file["post_user"]["user_id"] = c["post_user"]["user_id"]
        source_file["post_user"]["user_nickname"] = c["post_user"]["user_nickname"]
        source_file["post_user"]["user_name"] = c["post_user"]["user_name"]
        source_file["post_user"]["user_first_en_name"] = c["post_user"]["user_first_en_name"]
        source_file["post_user"]["user_age"] = c["post_user"]["user_age"]
        source_file["post_user"]["user_influ_level"] = c["post_user"]["user_influ_level"]
        source_file["post_user"]["user_first_en_name"] = c["post_user"]["user_first_en_name"]
        source_file["post_user"]["user_is_majia"] = c["post_user"]["user_is_majia"]
        source_file["post_guba"] = c["post_guba"]
        source_file["post_title"] = c["post_title"]
        #正则处理
        temp=str(c["post_content"])
        source_file["post_content"]=replace_tag(temp)
        source_file["post_publish_time"] = c["post_publish_time"]
        source_file["post_click_count"] = c["post_click_count"]
        source_file["post_forward_count"] = c["post_forward_count"]
        source_file["post_comment_count"] = c["post_comment_count"]
        source_file["post_comment_authority"] = c["post_comment_authority"]
        source_file["post_like_count"] = c["post_like_count"]
        source_file["post_source_id"] = c["post_source_id"]
        source_file["product_type"] = c["product_type"]
        source_file["source_click_count"] = c["source_click_count"]
        source_file["codepost_count"] = c["codepost_count"]
        next_url='https://i.eastmoney.com/'+source_file["post_user"]['user_id']
        yield Request(next_url, meta={"item":source_file},callback=self.add_sourcedata,dont_filter=True)
    def add_sourcedata(self,response):
        #添加user主页信息
        source_file=response.meta['item']
        source_file["post_user"]['post_user_follow']=user_data_re(response.xpath('//*[@id="tafollownav"]/p/span/text()').extract_first())
        source_file["post_user"]['post_user_fan']=user_data_re(response.xpath('//*[@id="tafansa"]/p/span/text()').extract())
        source_file["post_user"]['post_user_total_click']=user_data_re(response.xpath('//*[@id="others"]/div/div[1]/div[2]/div[3]/p[1]/span[1]/text()').extract_first())
        source_file["post_user"]['post_user_today_click']=user_data_re(response.xpath('//*[@id="others"]/div/div[1]/div[2]/div[3]/p[1]/span[2]/text()').extract_first())
        source_file["post_user"]['post_user_introduce']=user_data_re(response.xpath('//*[@id="others"]/div/div[1]/div[2]/div[3]/p[2]/span[2]/text()').extract_first())
        source_file["post_user"]['post_user_post_number']=user_data_re(response.xpath('//*[@id="mainlist"]/text()').extract_first())
        source_file["post_user"]['post_user_comment']=user_data_re(response.xpath('//*[@id="replaylist"]/text()').extract_first())
        print(source_file["post_id"])
        create_file(source_file["post_id"])
        # print(source_file)
        #保存源文件
        with open("/home/pi/Desktop/spider/{}/source/{}.json".format(source_file['post_id'], source_file['post_id']),
                  "w+") as jsonFile:
            jsonFile.write(json.dumps(source_file, ensure_ascii=False))
        #访问评论并保存
        reply_count = source_file["post_comment_count"]
        for reply_count_page in np.arange(0, reply_count / 50, 1) + 1:
            comment_data(source_file['post_id'], reply_count_page)
    def parse(self, response):
        for li in np.arange(2, 82, 1):
            item = {}
            item["标题链接"] = response.xpath("//*[@id='articlelistnew']/div[{}]/span[3]/a/@href".format(li)).extract()
            next_url = "http://mguba.eastmoney.com/" + item["标题链接"][0]
            ress = re.search(r'[0-9]{9}', next_url, re.S | re.M)
            next_url = "http://mguba.eastmoney.com/mguba/article/0/" + ress.group()
            print(next_url)
            yield Request(next_url, callback=self.source, dont_filter=True)