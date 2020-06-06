from urllib.parse import urlencode
from scrapy.utils.project import get_project_settings


max_page = get_project_settings()['MAX_PAGE'] + 1


def wf(keywords):
    for page in range(1, max_page):
        params = {
            'beetlansyId': 'aysnsearch',
            'searchType': 'all',
            'pageSize': 50,
            'page': page,
            'searchWord': keywords,
            'order': 'correlation',
            'showType': 'detail',
            'isCheck': 'check',
            'firstAuthor': 'false',
            'corePerio': 'false',
            'alreadyBuyResource': 'false',
            'navSearchType': 'all'
        }
        yield 'http://www.wanfangdata.com.cn/search/searchList.do?' + urlencode(params)


def ixs(keywords):
    for page in range(1, max_page):
        params = {
            'search_type': '',
            'q': keywords,
            'page': page
        }
        yield 'https://www.ixueshu.com/search/index.html?' + urlencode(params)


def wp(keywords):
    param = {}

    for page in range(1, max_page):
        param['ObjectType'] = 1
        param['ClusterUse'] = 'Article'
        param['UrlParam'] = 'u={}'.format(keywords)
        param['Sort'] = 0
        param['UserID'] = 189654
        param['PageNum'] = page
        param['PageSize'] = 100
        param['ShowRules'] = '任意字段={}'.format(keywords)

        yield {'searchParamModel': str(param)}
