# 程序功能: 按关键字爬取微博清单
# 程序作者: 马哥python说
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
    if gender_tag == 'f':
        return '女'
    elif gender_tag == 'm':
        return '男'
    else:
        return '未知'


def num_out(data):
    data = str(data)+'\t'
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


def get_comments(v_weibo_ids, v_commonsfile, v_max_page):
    for weibo_id in v_weibo_ids:
        max_id = 0
        for page in range(1, v_max_page+1):
            wait_seconds=random.uniform(1,2)
            print('开始时间{}s'.format(wait_seconds))
            sleep(wait_seconds)
            if page == 1:
                url = 'https://m.weibo.cn/comments/hotflow?id=' + str(weibo_id) + '&mid=' + str(
                    weibo_id) + '&max_id_type=0'
            else:
                if max_id == 0:
                    break
                url = 'https://m.weibo.cn/comments/hotflow?id=' + str(weibo_id) + '&mid=' + str(
                    weibo_id) + '&max_id=' + str(max_id) + '&max_id_type=0'
            ua =UserAgent(verify_ssl=False)
            headers = {
                "user-agent": ua.random,
                "cookie": "SUB=_2A25ODwaEDeRhGedJ71cV8ynNwj2IHXVt86rMrDV6PUJbkdAKLUTGkW1NVhyqRH7i9iR35768EV_p9zm-k9VF_X_7; _T_WM=76570933324; WEIBOCN_FROM=1110006030; MLOGIN=1; XSRF-TOKEN=de52ec; mweibo_short_token=664e07b295; M_WEIBOCN_PARAMS=oid%3D4785707983832954%26luicode%3D20000061%26lfid%3D4785707983832954%26uicode%3D20000061%26fid%3D4785707983832954",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept": "application/json, text/plain, */*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "zh-CN,zh;q=0.9",
                "referer": "https://m.weibo.cn/detail/{}".format(weibo_id),
                "mweibo-pwa": '1',
                "x-requested-with": "XMLHttpRequest"

            }
            r = requests.get(url, headers=headers)
            jsonres_data = r.json()
            if (jsonres_data.get('ok') == 0):
                break
            if (jsonres_data.get('ok') != 0):
                datas = jsonres_data['data'].get('data')
                max_id = jsonres_data['data'].get('max_id')

                page_list = []
                id_list = []
                text_list = []
                time_list = []
                like_count_list = []
                source_list = []
                user_name_list = []
                user_id_list = []
                user_gender_list = []
                follow_count_list = []
                followers_count_list = []
                parent_list = []
                for data in datas:
                    if data['comments']:
                        for c in data['comments']:
                            parent_list.append(num_out(c['rootid']))
                            page_list.append(c['floor_number'])
                            id_list.append(num_out(str(c['id'])))
                            dr = re.compile(r'<[^>]+>', re.S)  # 用正则表达式清洗评论数据
                            text2 = dr.sub('', c['text'])
                            text_list.append(text2)  # 评论内容
                            time_list.append(trans_time(v_str=c['created_at']))  # 评论时间
                            like_count_list.append(0)  # 评论点赞数
                            source_list.append(c['source'])  # 评论者IP归属地
                            user_name_list.append(c['user']['screen_name'])  # 评论者姓名
                            user_id_list.append(num_out(c['user']['id']))  # 评论者id
                            user_gender_list.append(c['user']['gender'])  # 评论者性别
                            follow_count_list.append(c['user']['follow_count'])  # 评论者关注数
                            followers_count_list.append(data['user']['followers_count'])  # 评论者粉丝数
                    page_list.append(data['floor_number'])
                    parent_list.append(0)
                    id_list.append(num_out(data['id']))
                    dr = re.compile(r'<[^>]+>', re.S)  # 用正则表达式清洗评论数据
                    text2 = dr.sub('', data['text'])
                    text_list.append(text2)  # 评论内容
                    time_list.append(trans_time(v_str=data['created_at']))  # 评论时间
                    like_count_list.append(data['like_count'])  # 评论点赞数
                    source_list.append(data['source'])  # 评论者IP归属地
                    user_name_list.append(data['user']['screen_name'])  # 评论者姓名
                    user_id_list.append(num_out(data['user']['id'])) # 评论者id
                    user_gender_list.append(data['user']['gender'])  # 评论者性别
                    follow_count_list.append(data['user']['follow_count'])  # 评论者关注数
                    followers_count_list.append(data['user']['followers_count'])  # 评论者粉丝数
                df = pd.DataFrame(
                    {
                        'id': num_out(weibo_id),
                        '父级': parent_list,
                        '评论页码': page_list,
                        '评论id': id_list,
                        '评论时间': time_list,
                        '评论点赞数': like_count_list,
                        '评论者IP归属地': source_list,
                        '评论者姓名': user_name_list,
                        '评论者id': user_id_list,
                        '评论者性别': user_gender_list,
                        '评论者关注数': follow_count_list,
                        '评论者粉丝数': followers_count_list,
                        '评论内容': text_list,
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
            # getNextConsultText(v_id, m_id, maxId)




def get_weibo_list(v_keyword, v_max_page):
    """
    爬取微博内容列表
    :param v_keyword: 搜索关键字
    :param v_max_page: 爬取前几页
    :return: None
    """
    for page in range(1, v_max_page + 1):
        print('===开始爬取第{}页微博==='.format(page))
        # 请求地址
        url = 'https://m.weibo.cn/api/container/getIndex'
        # 请求参数
        params = {
            "containerid": "100103type=1&q={}".format(v_keyword),
            "page_type": "searchall",
            "page": page
        }

        # 发送请求
        r = requests.get(url, headers=Gheaders, params=params)
        print(r.status_code)

        # 解析json数据
        cards = r.json()["data"]["cards"]
        # cards = list(filter(lambda x:  'card_group' not in x , result))
        # print(cards)
        # 微博内容
        text_list = jsonpath(cards, '$..mblog.text')
        # 微博内容-正则表达式数据清洗
        dr = re.compile(r'<[^>]+>', re.S)
        text2_list = []
        print('text_list is:')
        print(text_list)
        if not text_list:  # 如果未获取到微博内容，进入下一轮循环
            continue
        if type(text_list) == list and len(text_list) > 0:
            for text in text_list:
                text2 = dr.sub('', text)  # 正则表达式提取微博内容
                print(text2)
                text2_list.append(text2)
        # 微博创建时间
        time_list = jsonpath(cards, '$..mblog.created_at')
        time_list = [trans_time(v_str=i) for i in time_list]
        # 微博作者
        author_list = jsonpath(cards, '$..mblog.user.screen_name')
        # 微博id
        id_list = jsonpath(cards, '$..mblog.id')
        # 微博mid
        mid_list = jsonpath(cards, '$..mblog.mid')
        # 判断是否存在全文
        isLongText_list = jsonpath(cards, '$..mblog.isLongText')
        idx = 0
        for i in isLongText_list:
            if i == True:
                long_text = getLongText(v_id=id_list[idx])
                text2_list[idx] = long_text
            idx += 1
        # 转发数
        reposts_count_list = jsonpath(cards, '$..mblog.reposts_count')
        # 评论数
        comments_count_list = jsonpath(cards, '$..mblog.comments_count')
        # 点赞数
        attitudes_count_list = jsonpath(cards, '$..mblog.attitudes_count')
        # 把列表数据保存成DataFrame数据
        df = pd.DataFrame(
            {
                '页码': [page] * len(id_list),
                '微博id': id_list,
                '微博ids': mid_list,
                '微博作者': author_list,
                '发布时间': time_list,
                '微博内容': text2_list,
                '转发数': reposts_count_list,
                '评论数': comments_count_list,
                '点赞数': attitudes_count_list,
            }
        )

        # 表头
        if os.path.exists(v_weibo_file):
            header = None
        else:
            header = ['页码', '微博id', '微博ids', '微博作者', '发布时间', '微博内容', '转发数', '评论数', '点赞数']  # csv文件头
        # 保存到csv文件
        df.to_csv(v_weibo_file, mode='a+', index=False, header=header, encoding='utf_8_sig')
        fv_weibo_file = '微博评价.csv'
        get_comments(id_list, fv_weibo_file, 500)
        print('csv保存成功:{}'.format(v_weibo_file))


if __name__ == '__main__':
    # 爬取前几页
    max_search_page = 8  # 爬前n页
    # 爬取关键字
    search_keyword = '李子柒事件'
    # 保存文件名
    v_weibo_file = '微博清单_{}_前{}页.csv'.format(search_keyword, max_search_page)
    v_weibopingjia_file = '微博评价.csv'
    # 如果csv文件存在，先删除之
    if os.path.exists(v_weibo_file):
        os.remove(v_weibo_file)
        print('微博清单存在，已删除: {}'.format(v_weibo_file))
    if os.path.exists(v_weibopingjia_file):
        os.remove(v_weibopingjia_file)
        print('微博清单存在，已删除: {}'.format(v_weibopingjia_file))
    # 调用爬取微博函数
    get_weibo_list(v_keyword=search_keyword, v_max_page=max_search_page)
    # 数据清洗-去重
    df = pd.read_csv(v_weibo_file)
    # 删除重复数据
    df.drop_duplicates(subset=['微博id'], inplace=True, keep='first')
    df['微博id'] = df['微博id'].map(num_out)
    df['微博ids'] = df['微博ids'].map(num_out)
    # 再次保存csv文件
    df.to_csv(v_weibo_file, index=False, encoding='utf_8_sig')

    # 数据清洗-去重
    df = pd.read_csv(v_weibopingjia_file)
    # 删除重复数据
    df.drop_duplicates(subset=['评论id'], inplace=True, keep='first')
    df['id'] = df['id'].map(num_out)
    df['父级'] = df['父级'].map(num_out)
    df['评论id'] = df['评论id'].map(num_out)
    # 再次保存csv文件
    df.to_csv(v_weibopingjia_file, index=False, encoding='utf_8_sig')
    print('数据清洗完成')
