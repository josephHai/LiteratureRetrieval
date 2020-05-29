from urllib.parse import urlencode


def wf(keywords):
    for page in range(1, 5):
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
    for page in range(1, 5):
        params = {
            'search_type': '',
            'q': keywords,
            'page': page
        }
        yield 'https://www.ixueshu.com/search/index.html?' + urlencode(params)
