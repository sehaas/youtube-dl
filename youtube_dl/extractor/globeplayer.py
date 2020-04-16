# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor


class GlobePlayerIE(InfoExtractor):
    _VALID_URL = r'https?://player\.(hader\.at|globe\.wien)/[^/]+/(?P<id>[^/?#]+)'
    _TESTS = [{
        'url': 'https://player.hader.at/hader/hader-homestory-teil-5',
        'md5': '74cccdd759cf1b970dfb7bcd58af3a2d',
        'info_dict': {
            'id': 'hader-homestory-teil-5',
            'ext': 'mp4',
            'title': 'Struktur ist alles',
            'duration': 192,
            'description': '',
        },
        'params': {
            'format': 'bestvideo',
        }
    }, {
        'url': 'https://player.globe.wien/globe-wien/romeoundjulia',
        'md5': '1170c16bb63c1f7b704321ed6d1e19a3',
        'info_dict': {
            'id': 'romeoundjulia',
            'ext': 'mp4',
            'title': 'Romeo & Julia',
            'duration': 11760,
            'description': 'Romeo und Julia sind nur deswegen das gr\xf6\xdfte Liebespaar der Weltliteratur, weil sie nie miteinander leben mussten, sondern rechtzeitig gestorben sind. Im Falle unserer h\xf6chst beklagenswerten ...',
        },
        'params': {
            'format': 'bestvideo',
        }
    }, {
        'url': 'https://player.hader.at/hader/hader-imkeller-audio',
        'md5': '6f70247d83e792652a7ac27bbfb202c9',
        'info_dict': {
            'id': 'hader-imkeller-audio',
            'ext': 'mp3',
            'title': 'Im Keller',
            'duration': 7140,
            'description': 'Ein erfolgreicher Werbefritze, der gerade an einem Slogan f\xfcr feuchtes Klopapier arbeitet und keine Kullerparty ausl\xe4sst, verwandelt sich in einen miesen Spie\xdfer. <br/><br/> Josef Hader nimmt den Zuschauer mit auf eine Reise mit in den Keller. <br/><br/> Live-Mitschnitt aus dem Orpheum Graz, 17. und 18. J\xe4nner 1993',
        }
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)
        next_data = self._parse_json(
            self._search_regex(
                r'<script[^>]+id="__NEXT_DATA__"[^>]+type="application/json"[^>]*>([^<]+)</script>',
                webpage, 'next data'),
            video_id)

        vod = next_data.get('props').get('initialState').get('vod')

        formats = []
        streamUrl = vod.get('streamUrl')
        for key in streamUrl:
            src_url = streamUrl.get(key)
            if key == 'hls':
                formats.extend(self._extract_m3u8_formats(
                    src_url, video_id, ext='mp4', m3u8_id=key, fatal=False))
            elif key == 'dash':
                formats.extend(self._extract_mpd_formats(
                    src_url, video_id, mpd_id=key, fatal=False))
            else:
                formats.append({
                    'format_id': key,
                    'url': src_url
                })

        self._check_formats(formats, video_id)
        self._sort_formats(formats)

        return {
            'id': vod.get('id'),
            'title': vod.get('title'),
            'description': vod.get('teaserDescription'),
            'release_year': vod.get('year'),
            'duration': (vod.get('durationMinutes') or 0) * 60,
            'formats': formats
        }
