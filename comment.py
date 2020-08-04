import requests
import json
import numpy as np
from myspider.create_save import save

#评论数据处理
def comment_data(source_id, reply_count_page):
    url = "http://mguba.eastmoney.com/mguba2020/interface/GetData.aspx"
    data = {
        "param": "postid={}&type=0&ps=50&p={}&sort=1&sorttype=1".format(source_id, reply_count_page),
        "plat": "Wap",
        "path": "reply/api/Reply/ArticleNewReplyList",
        "env": "1",
        "origin": "",
    }
    rep = requests.post(url, data=data).content.decode()
    ret1 = json.loads(rep)

    for count in np.arange(0, len(ret1['re'])):

        if len(ret1['re'][count]['child_replys']) > 0:
            for count1 in np.arange(0, len(ret1['re'][count]['child_replys'])):
                ret1['re'][count]['child_replys'][count1]['source_post_id'] = ret1['re'][count]['reply_id']
                ret1['re'][count]['child_replys'][count1]['comment_level']='2'
                del ret1['re'][count]['child_replys'][count1]['source_reply']
                save(ret1['re'][count]['child_replys'][count1], ret1['re'][count]['child_replys'][count1]['reply_id'],
                     source_id)
            del ret1['re'][count]['child_replys']
            del ret1['re'][count]['fake_child_replys']
            ret1["re"][count]["comment_level"] = "1"
            save(ret1['re'][count],
                 ret1['re'][count]['reply_id'], source_id)
        else:
            del ret1['re'][count]['child_replys']
            del ret1['re'][count]['fake_child_replys']
            ret1["re"][count]["comment_level"]="1"
            save(ret1['re'][count], ret1['re'][count]['reply_id'], source_id)