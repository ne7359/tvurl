# -*- coding: utf-8 -*-
# by @Qist
"""
ITalkBB TV - 海外华人影视
"""
import re
import json
import subprocess
import requests
from base.spider import Spider


class Spider(Spider):
    def getName(self):
        return 'ITalkBB TV'

    def init(self, extend=""):
        pass

    def __init__(self):
        self.host = 'https://www.italkbbtv.com'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
            'Referer': 'https://www.italkbbtv.com/'
        }
        self.timeout = 20

        self.class_names = '电视剧&电影&综艺&动画'.split('&')
        self.class_urls = 'drama/62c670dc1dca2d424404499c&movie/62ac4ef36e0b5a13ed291544&variety/62ce7417c7daaa4a5d3fea14&cartoon/62ac4e6e4beefe53586478ca'.split('&')

        self.key_map = {
            'drama': 'dramaSeriesLists',
            'movie': 'movieSeriesLists',
            'variety': 'varietySeriesLists',
            'cartoon': 'cartoonSeriesLists',
            'shorts': 'shortsSeriesLists'
        }

    def get_nuxt_data(self, html):
        """从HTML中提取并解析__NUXT__数据"""
        m = re.search(r'window\.__NUXT__=([\s\S]*?);</script>', html)
        if not m:
            return None
        js_expr = m.group(1)
        try:
            result = subprocess.run(
                ['node', '-e', f'process.stdout.write(JSON.stringify({js_expr}))'],
                capture_output=True, timeout=15
            )
            if result.returncode == 0 and result.stdout:
                return json.loads(result.stdout)
        except Exception as e:
            print(f"get_nuxt_data error: {e}")
        return None

    def pick_pic(self, obj):
        """提取图片URL"""
        if not obj:
            return ''
        images = obj.get('images', {}) or {}
        poster = (images.get('poster') or [''])[0] if images.get('poster') else ''
        landscape = (images.get('landscape') or [''])[0] if images.get('landscape') else ''
        return poster or landscape or obj.get('imgUrl', '')

    def join_stars(self, stars):
        """拼接演员/导演名"""
        if not isinstance(stars, list):
            return ''
        return '/'.join([s.get('name', '') for s in stars if s.get('name')])

    def make_vod_from_series(self, series, fallback_name=''):
        """从series对象构建vod字典"""
        if not series:
            return None
        category_id = series.get('category_id', [])
        if isinstance(category_id, list):
            category_id = category_id[0] if category_id else ''
        root_id = series.get('root_id', '')
        series_id = series.get('id', '') or series.get('series_id', '')
        route = 'shortsPlay' if root_id == '66b1d25cf2dde82c215f9b59' else 'play'
        type_name = series.get('rootName', '') or series.get('categoryName', '')
        remark = (series.get('latest_episode_name', '') or
                  series.get('latest_episode_shortname', '') or
                  ('更新至' + str(series.get('episode_count', ''))) if series.get('episode_count') else '')
        released_at = series.get('released_at')
        vod_year = ''
        if released_at:
            try:
                from datetime import datetime
                vod_year = str(datetime.fromtimestamp(released_at).year)
            except:
                pass
        stars = series.get('stars', {}) or {}
        return {
            'vod_id': route + '$' + series_id,
            'vod_name': series.get('name', '') or fallback_name,
            'vod_pic': self.pick_pic(series),
            'vod_remarks': remark,
            'vod_year': vod_year,
            'type_name': type_name,
            'vod_content': series.get('description', ''),
            'vod_actor': self.join_stars(stars.get('actor', []) or []),
            'vod_director': self.join_stars(stars.get('director', []) or [])
        }

    def make_vod_from_card(self, card):
        """从card对象构建vod字典（搜索用）"""
        if not card:
            return None
        series = card.get('series') or card.get('target') or card
        fallback = card.get('name', '') or card.get('title', '')
        vod = self.make_vod_from_series(series, fallback)
        if not vod:
            return None
        if not vod['vod_name']:
            vod['vod_name'] = fallback
        if not vod['vod_pic']:
            vod['vod_pic'] = (self.pick_pic(card) or
                              ((card.get('image', {}) or {}).get('poster', '')) or
                              ((card.get('image', {}) or {}).get('landscape', '')))
        if not vod['vod_remarks']:
            vod['vod_remarks'] = card.get('description', '')
        return vod

    def unique_by_id(self, vod_list):
        """按vod_id去重"""
        seen = {}
        result = []
        for v in vod_list:
            vid = v.get('vod_id', '') if v else ''
            if vid and vid not in seen:
                seen[vid] = 1
                result.append(v)
        return result

    def fetch(self, url):
        """发送GET请求"""
        try:
            resp = requests.get(url, headers=self.header, timeout=self.timeout)
            resp.encoding = 'utf-8'
            return resp.text
        except Exception as e:
            print(f"fetch error: {e}")
            return ''

    def homeContent(self, filter):
        """首页推荐"""
        result = {'class': [], 'list': []}
        for name, cid in zip(self.class_names, self.class_urls):
            result['class'].append({'type_name': name, 'type_id': cid})

        # 默认加载电视剧列表
        url = f"{self.host}/drama/62c670dc1dca2d424404499c"
        html = self.fetch(url)
        nuxt = self.get_nuxt_data(html)
        if nuxt:
            try:
                store = nuxt.get('state', {}).get('pageList', {}).get('dramaSeriesLists', {})
                data = store.get('62c670dc1dca2d424404499c', {})
                series_list = data.get('series', [])
                vods = []
                for s in series_list:
                    v = self.make_vod_from_series(s)
                    if v:
                        vods.append(v)
                result['list'] = self.unique_by_id(vods)
            except Exception as e:
                print(f"homeContent parse error: {e}")
        return result

    def homeVideoContent(self):
        """首页视频内容"""
        return {}

    def categoryContent(self, tid, pg, filter, extend):
        """分类内容"""
        result = {'list': [], 'page': int(pg), 'pagecount': 999, 'limit': 24, 'total': 999999}
        parts = tid.split('/')
        alias = parts[0]
        cid = parts[1] if len(parts) > 1 else ''
        url = f"{self.host}/{tid}"
        if int(pg) > 1:
            url += f"?page={pg}"
        html = self.fetch(url)
        nuxt = self.get_nuxt_data(html)
        if nuxt:
            try:
                store = nuxt.get('state', {}).get('pageList', {}).get(self.key_map.get(alias, ''), {})
                data = store.get(cid, {})
                series_list = data.get('series', [])
                vods = []
                for s in series_list:
                    v = self.make_vod_from_series(s)
                    if v:
                        vods.append(v)
                result['list'] = self.unique_by_id(vods)
            except Exception as e:
                print(f"categoryContent parse error: {e}")
        return result

    def detailContent(self, ids):
        """详情页"""
        if not ids or not ids[0]:
            return {'list': []}
        vid = ids[0]
        parts = vid.split('$')
        route = parts[0] if len(parts) > 1 else 'play'
        sid = parts[1] if len(parts) > 1 else vid
        url = f"{self.host}/{route}/{sid}"
        html = self.fetch(url)
        nuxt = self.get_nuxt_data(html)
        if not nuxt:
            return {'list': []}
        try:
            play = nuxt.get('state', {}).get('play', {})
            info = play.get('SeriesInfo', {})
            eps = play.get('EpisodeList', [])
            vod = self.make_vod_from_series(info) or {'vod_id': vid}
            tabs = 'ITalkBB短剧' if route == 'shortsPlay' else 'ITalkBB'
            play_urls = []
            for ep in eps:
                name = ep.get('shortname', '') or ep.get('name', '')
                ep_id = ep.get('id', '')
                play_urls.append(f"{name}${route}@{sid}@{ep_id}")
            vod['vod_id'] = vid
            vod['vod_name'] = info.get('name', '') or vod.get('vod_name', '')
            vod['vod_pic'] = self.pick_pic(info) or vod.get('vod_pic', '')
            vod['type_name'] = info.get('rootName', '') or info.get('categoryName', '') or vod.get('type_name', '')
            vod['vod_content'] = info.get('description', '') or vod.get('vod_content', '')
            stars = info.get('stars', {}) or {}
            vod['vod_actor'] = self.join_stars(stars.get('actor', []) or [])
            vod['vod_director'] = self.join_stars(stars.get('director', []) or [])
            vod['vod_remarks'] = (info.get('latest_episode_name', '') or
                                  info.get('latest_episode_shortname', '') or
                                  vod.get('vod_remarks', ''))
            vod['vod_play_from'] = tabs
            vod['vod_play_url'] = '#'.join(play_urls)
            return {'list': [vod]}
        except Exception as e:
            print(f"detailContent parse error: {e}")
            return {'list': []}

    def searchContent(self, key, quick, pg="1"):
        """搜索"""
        url = f"{self.host}/?keyword={key}"
        html = self.fetch(url)
        nuxt = self.get_nuxt_data(html)
        vod_list = []
        if nuxt:
            try:
                data = nuxt.get('data', [{}])[0]
                banners = data.get('bannerData', []) or []
                groups = data.get('serverGroupDataList', []) or []
                for card in banners:
                    v = self.make_vod_from_card(card)
                    if v:
                        vod_list.append(v)
                for g in groups:
                    for card in (g.get('list', []) or []):
                        v = self.make_vod_from_card(card)
                        if v:
                            vod_list.append(v)
            except Exception as e:
                print(f"searchContent parse error: {e}")
        # 客户端过滤
        filtered = []
        for v in vod_list:
            if not v or not v.get('vod_name'):
                continue
            text = ' '.join([v.get('vod_name', ''), v.get('vod_remarks', ''),
                             v.get('vod_content', ''), v.get('type_name', '')])
            if key in text:
                filtered.append(v)
        return {'list': self.unique_by_id(filtered)}

    def playerContent(self, flag, id, vipFlags):
        """播放"""
        parts = id.split('@')
        route = parts[0] if len(parts) > 1 else 'play'
        sid = parts[1] if len(parts) > 1 else ''
        eid = parts[2] if len(parts) > 2 else ''
        url = f"{self.host}/{route}/{sid}"
        if eid:
            url += f"?ep={eid}"
        return {
            'jx': 0,
            'parse': 1,
            'url': url,
            'header': self.header
        }

    def localProxy(self, param):
        return None
