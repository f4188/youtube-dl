# coding: utf-8
from __future__ import unicode_literals

import re

from .common import InfoExtractor
from ..utils import (
    determine_ext,
    float_or_none,
    int_or_none,
    mimetype2ext,
    parse_age_limit,
    parse_iso8601,
    strip_or_none,
    try_get,
)


class BTKuluValleyIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?bt\.kuluvalley\.com/view/(?P<id>[a-zA-Z0-9]+)'
    _TEST = {
        'url': 'https://bt.kuluvalley.com/view/I9tnOFRRssI',
        'md5': 'TODO: md5 sum of the first 10241 bytes of the video file (use --test)',
        'info_dict': {
            'id': 'I9tnOFRRssI',
            'ext': 'mpg',
           # 'title': 'Video title goes here',
            'thumbnail': r're:^https?://.*\.jpg$',
            # TODO more properties, either as:
            # * A value
            # * MD5 checksum; start the string with md5:
            # * A regular expression; start the string with re:
            # * Any Python type (for example int or float)
        }
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        json_str = self._search_regex(r'<script>[^<]*KV\s*=\s*(?P<json_str>{[\S\s]*});[^<]*</script>', webpage, 'json',group='json_str')
        
        #data = """{ Name: "test", Address: "xyz"}"""
        json_str = re.sub(r"([\{\s,])([a-zA-Z][\w]*)(:)(?!\",)[^\/]", r'\1"\2"\3',  json_str)
        #print(json_str)
        
        json_data = self._parse_json(json_str, video_id)
        #print(json_data["kulu"]["media"])
        #print(json_data["kulu"]["metadata"])
        video_meta = try_get(json_data, lambda x: x["kulu"]["metadata"])

        print(video_meta)
        #print(json_data["kulu"]["media"]["variants"])
        video_formats = try_get(json_data, lambda x: x["kulu"]['media']["variants"], list) or []
        #variants
        print(video_formats)


        title = ""
        

        # TODO more code goes here, for example ...
        #title = self._html_search_regex(r'<h1>(.+?)</h1>', webpage, 'title')

        return {
            'id': video_id,
            'title': title or self._og_search_title(webpage),
            'formats': video_formats,
            'description': self._og_search_description(webpage),
           # 'uploader': self._search_regex(r'<div[^>]+id="uploader"[^>]*>([^<]+)<', webpage, 'uploader', fatal=False),
            # TODO more properties (see youtube_dl/extractor/common.py)
        }