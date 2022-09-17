import json
import os
import re  # 正则表达式提取文本
import random
from time import sleep

from jsonpath import jsonpath  # 解析json数据
import requests  # 发送请求
import pandas as pd  # 存取csv文件
import datetime  # 转换时间用
from fake_useragent import UserAgent

# 请求头

Gheaders = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
}


def trans_time(v_str):
    """转换GMT时间为标准格式"""
    GMT_FORMAT = '%a %b %d %H:%M:%S +0800 %Y'
    timeArray = datetime.datetime.strptime(v_str, GMT_FORMAT)
    ret_time = timeArray.strftime("%Y-%m-%d %H:%M:%S")
    return ret_time


def tran_gender(gender_tag):
    """转换性别"""
    if gender_tag == 1:
        return '男'
    elif gender_tag == 0:
        return '女'
    else:  # -1
        return '未知'


def num_out(data):
    data = str(data) + '\t'
    return data


def getLongText(v_id):
    """爬取长微博全文"""
    url = 'https://m.weibo.cn/statuses/extend?id=' + str(v_id)
    r = requests.get(url, headers=Gheaders)
    json_data = r.json()
    long_text = json_data['data']['longTextContent']
    # 微博内容-正则表达式数据清洗
    dr = re.compile(r'<[^>]+>', re.S)
    long_text2 = dr.sub('', long_text)
    # print(long_text2)
    return long_text2


def get_comments(answer_idlist, v_commonsfile):
    for answer_id in answer_idlist:

        ua = UserAgent(verify_ssl=False)
        headers = {
            # "user-agent": ua.random,
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': '_zap=12fcd22e-649c-4413-a808-22469005e5aa; d_c0="APAdW5L5ORWPTt7Jt_aMiDq6Q90AzKsKjRY=|1657447881"; _9755xjdesxxd_=32; _xsrf=9a6b002a-4c64-41b7-afe5-b145564b52f5; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1662170291; captcha_session_v2=2|1:0|10:1662170289|18:captcha_session_v2|88:ZnZYMTV4SWJRMXdmUEhISnJVc1lCVXR3S1crSkFoYnhUQ1o5Nks0NHlhK29UeXliVWp4Ty9QMWx4SXZuRmRBRA==|8dcfe7d7c520196dd4f3979ce017cc4bd238432364cceebdb77c2c8051031636; SESSIONID=qiiOgignAAk9ZEQiIiUUSzA7JsvQUHdpemAKNptEBWW; JOID=WlAdAkqUi0gVRcu3UZyynl3-88NE5eIoWiui0DbcyiMlH4fmOCY2U39My75YGctMdRLJiSWSnvrQ2ZtvDOhI62o=; osd=UVEcAU2fikkWQsC2UJ-1lVz_8MRP5OMrXSCj0TXbwSIkHIDtOSc1VHRNyr1fEspNdhXCiCSRmfHR2JhoB-lJ6G0=; __snaker__id=ZyWieWgpiMMtHR6Q; gdxidpyhxdE=wkgGg9b%5CiWiNXD5D4A%5CdPT2qE7JQoKuIxnmt%2Bt%5CaYRm5h2GlThY2EQgiGZOoz9A26oYcR63SgZ3K7c4S8cp6tYgHIWwh6Scv6Iu9dd%2BYneu3R35qyTrzEs3RV7essuj%2BrDT4Xer%2Bn%5CORnfaRvDjEaiDUJd%2F3jn8V1gh7U7IRLKHy%5C%2FBM%3A1662171191938; YD00517437729195%3AWM_NI=ssaOBMpS8FZdia3%2BwclF80u5xraRosWTFvoDMAfnlSoq1Toj9cN2FW9xDS5Ozrb4YTNsM8qym0zGGGGHqeJwHI7YzDXB6kcXpSjliY3unpaRzdOAfRevhFRyfpk%2BK1vdZUI%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6ee98f443838fba98d65fa3eb8ea7c85f929a8eadd85dbc9f9da6eb6aabb6f9bad72af0fea7c3b92ab1adafb0c147b48df8a7d970abbffdccf669b09af8d1f83fbcaeafb3ee79958c8a97ee508f9faa8fef59adafffb5ee62fbbd82d3c55dfba88cb4b845baaeaed5dc608ead83d9f473aff0b6a8c64d8598bf86c97d8c97f9baf9509c9efa8ce254b48da68dec53f1aba291e45ababc81a2e55aa7aaa8a7d173a6b0a5ccca3bb6bc96b6cc37e2a3; YD00517437729195%3AWM_TID=iqkRpxp%2BxVxBREAQQAKFW0RTRlLjj7IX; o_act=login; ref_source=other_https://www.zhihu.com/signin?next=/; expire_in=15552000; z_c0=2|1:0|10:1662170305|4:z_c0|92:Mi4xQmJqOUJRQUFBQUFBOEIxYmt2azVGUmNBQUFCZ0FsVk53UUlBWkFCSnNJaUI5ZGNlNWZwSHlmbkdpSTNJYS1IaURn|285d49759cba7d6367b46d540442c0e591464bd405787c02d07317df5b9a7cc9; q_c1=139da0ca4b824c1fbcf69f4f0f152fbe|1662170306000|1662170306000; NOT_UNREGISTER_WAITING=1; tst=r; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1662170490; KLBRSID=af132c66e9ed2b57686ff5c489976b91|1662170490|1662170288',
            'referer': 'https://www.zhihu.com/',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'x-requested-with': 'fetch',
            'x-zse-93': '101_3_3.0',
            'x-zse-96': '2.0_+pwbphVjJgNCMIu5RkKrx90qyR0j5WjB2izyY+IYKc5eKJdf7QIhCI7taVzw0+w/'

        }

        i = 0
        while True:
            next_pageUrl = 'https://www.zhihu.com/api/v4/comment_v5/answers/{}/root_comment?order_by=score&limit=20&offset=&status=open'.format(
                answer_id)
            i += 20
            wait_seconds = random.uniform(1, 2)
            print('开始时间{}s'.format(wait_seconds))
            sleep(wait_seconds)
            # r = requests.get(url, headers=headers)  # 发送请求
            #
            res = requests.get(next_pageUrl, headers=headers)
            res1=res.content.decode('utf-8')
            jsonfile = json.loads(res1)
            next_page = jsonfile['paging']['is_end']

            total = jsonfile['counts']['total_counts']  # 一共多少条评论
            if total==0:
                break
            print('一共{}条评论'.format(total))
            comments = jsonfile['data']
            paging = jsonfile['paging']
            authors = []
            genders = []
            answer_urls = []
            author_homepages = []
            author_pics = []
            create_times = []
            contents = []
            child_tag = []
            for c in comments:  # 一级评论
                # 评论作者
                author = c['author']['member']['name']
                authors.append(author)
                print('作者：', author)
                # 作者性别
                gender_tag = c['author']['member']['gender']
                genders.append(tran_gender(gender_tag))
                child_tag.append('一级')
                answer_urls.append(c['url'])
                author_homepages.append(c['author']['member']['url'])
                author_pics.append(c['author']['member']['avatar_url'])
                create_times.append(c['created_time'])
                contents.append(c['content'])
                if c['child_comments']:  # 如果二级评论存在
                    for child in c['child_comments']:  # 二级评论
                        answer_urls.append(child['url'])
                        author_homepages.append(child['author']['member']['url'])
                        author_pics.append(child['author']['member']['avatar_url'])
                        create_times.append(child['created_time'])
                        contents.append(child['content'])
                        # 评论作者
                        print('子评论作者：', child['author']['member']['name'])
                        authors.append(child['author']['member']['name'])
                        # 作者性别
                        genders.append(tran_gender(child['author']['member']['gender']))
                        child_tag.append('二级')
            df = pd.DataFrame(
                {
                    '回答url': answer_urls,
                    '页码': [i + 1] * len(answer_urls),
                    '评论作者': authors,
                    '作者性别': genders,
                    '作者主页': author_homepages,
                    '作者头像': author_pics,
                    '评论时间': create_times,
                    '评论内容': contents,
                    '评论级别': child_tag,
                }
            )
            v_comment_file = '微博评价.csv'
            if os.path.exists(v_comment_file):  # 如果文件存在，不再设置表头
                header = False
            else:  # 否则，设置csv文件表头
                header = True
            # 保存csv文件
            df.to_csv(v_comment_file, mode='a+', index=False, header=header, encoding='utf_8_sig')
            print('结果保存成功:{}'.format(v_comment_file))
            if next_page == True:
                break
            else:
                next_pageUrl = jsonfile['paging']['next']



if __name__ == '__main__':
    # 爬取前几页
    max_search_page = 8  # 爬前n页
    # 爬取关键字
    search_keyword = '李子柒事件'
    # 保存文件名
    v_weibo_file = '知乎_{}_前{}页.csv'.format(search_keyword, max_search_page)
    # 如果csv文件存在，先删除之
    if os.path.exists(v_weibo_file):
        os.remove(v_weibo_file)
        print('微博清单存在，已删除: {}'.format(v_weibo_file))
    # 调用爬取微博函数
    get_comments(['2655484653'], 'fv_weibo_file')
    # 数据清洗-去重
    df = pd.read_csv(v_weibo_file)
    # 再次保存csv文件
    df.to_csv(v_weibo_file, index=False, encoding='utf_8_sig')

    print('数据清洗完成')
