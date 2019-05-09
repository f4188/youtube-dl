# coding: utf-8
from __future__ import unicode_literals

import time

from .common import InfoExtractor


class NudogramIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?nudogram\.com/videos/\d+/(?P<id>[\w-]+)'
    _TEST = {
        'url': 'https://nudogram.com/videos/598/megan-barton-hanson-photoshoot/',
        'md5': 'TODO: md5 sum of the first 10241 bytes of the video file (use --test)',
        'info_dict': {
            'id': '42',
            'ext': 'mp4',
            'title': 'Video title goes here',
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

        video_url = self._html_search_regex(
            r"""video_url\s*:\s*\'(function\/0\/)?(?P<url>https?:\/\/nudogram.com\/get_file\/[^']*.mp4\/?)""", webpage, 'url', group='url')

        rnd = self._html_search_regex(
            r"""rnd\s*:\s*\'(\w+)\'""", webpage, 'rnd')

        now = int(time.time()*1000)
        video_url = video_url + '?rnd={0}'.format(now)
        print(video_url)



        title = 'Video title goes here'

        return {
            'id': video_id,
            'url': video_url,
            'title': title or self._og_search_title(webpage),
            'description': self._og_search_description(webpage),
           # 'uploader': self._search_regex(r'<div[^>]+id="uploader"[^>]*>([^<]+)<', webpage, 'uploader', fatal=False),
            # TODO more properties (see youtube_dl/extractor/common.py)
        }