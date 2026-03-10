"""
VentureLens AI - Trends Service
"""
import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)

TIMEFRAME_MAP = {
    '1M':  'today 1-m',
    '3M':  'today 3-m',
    '12M': 'today 12-m',
    '5Y':  'today 5-y',
    '10Y': 'all',
}
DEFAULT_TIMEFRAME = '12M'


class TrendsService:

    def _get_pytrends(self):
        try:
            from pytrends.request import TrendReq
            return TrendReq(hl='en-US', tz=360, timeout=(10, 25))
        except ImportError:
            logger.warning("pytrends not installed")
            return None
        except Exception as e:
            logger.warning(f"pytrends init error: {e}")
            return None

    def fetch_trends(self, keywords: list, timeframe_key: str = DEFAULT_TIMEFRAME) -> dict:
        timeframe = TIMEFRAME_MAP.get(timeframe_key, TIMEFRAME_MAP[DEFAULT_TIMEFRAME])
        pt = self._get_pytrends()

        if pt is None:
            return self._mock_trends(keywords, timeframe_key)

        keywords = [kw for kw in keywords[:5] if kw]

        try:
            pt.build_payload(keywords, cat=0, timeframe=timeframe, geo='', gprop='')
            time.sleep(0.5)
            df = pt.interest_over_time()

            if df.empty:
                return self._mock_trends(keywords, timeframe_key)

            if 'isPartial' in df.columns:
                df = df.drop(columns=['isPartial'])

            labels = [d.strftime('%Y-%m-%d') for d in df.index]
            colors = [
                ('rgba(99,102,241,1)',  'rgba(99,102,241,0.1)'),
                ('rgba(16,185,129,1)',  'rgba(16,185,129,0.1)'),
                ('rgba(245,158,11,1)',  'rgba(245,158,11,0.1)'),
                ('rgba(239,68,68,1)',   'rgba(239,68,68,0.1)'),
                ('rgba(168,85,247,1)',  'rgba(168,85,247,0.1)'),
            ]
            datasets = []
            for i, kw in enumerate(keywords):
                if kw in df.columns:
                    b, bg = colors[i % len(colors)]
                    datasets.append({
                        'label': kw, 'data': df[kw].tolist(),
                        'borderColor': b, 'backgroundColor': bg,
                        'borderWidth': 2, 'tension': 0.4, 'fill': True,
                        'pointRadius': 0, 'pointHoverRadius': 4,
                    })

            return {'labels': labels, 'datasets': datasets, 'timeframe_key': timeframe_key, 'is_mock': False}

        except Exception as e:
            logger.error(f"Google Trends error: {e}")
            return self._mock_trends(keywords, timeframe_key)

    def _mock_trends(self, keywords: list, timeframe_key: str = DEFAULT_TIMEFRAME) -> dict:
        import random
        from datetime import timedelta

        config = {
            '1M':  (30,  timedelta(days=1)),
            '3M':  (13,  timedelta(weeks=1)),
            '12M': (52,  timedelta(weeks=1)),
            '5Y':  (60,  timedelta(weeks=4)),
            '10Y': (120, timedelta(weeks=4)),
        }
        points, delta = config.get(timeframe_key, config[DEFAULT_TIMEFRAME])
        base_date = datetime.now() - delta * points
        labels = [(base_date + delta * i).strftime('%Y-%m-%d') for i in range(points)]

        colors = [
            ('rgba(99,102,241,1)',  'rgba(99,102,241,0.1)'),
            ('rgba(16,185,129,1)',  'rgba(16,185,129,0.1)'),
            ('rgba(245,158,11,1)',  'rgba(245,158,11,0.1)'),
        ]
        datasets = []
        for i, kw in enumerate(keywords[:3]):
            base = random.randint(20, 50)
            inc = random.uniform(0.2, 0.8)
            val = float(base)
            data = []
            for _ in range(points):
                val = max(5, min(100, val + inc + random.uniform(-6, 8)))
                data.append(round(val))
            b, bg = colors[i % len(colors)]
            datasets.append({
                'label': kw, 'data': data,
                'borderColor': b, 'backgroundColor': bg,
                'borderWidth': 2, 'tension': 0.4, 'fill': True,
                'pointRadius': 0, 'pointHoverRadius': 4,
            })

        return {'labels': labels, 'datasets': datasets, 'timeframe_key': timeframe_key, 'is_mock': True}


trends_service = TrendsService()