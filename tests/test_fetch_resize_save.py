import os
import unittest

from google_images_search.google_api import GoogleCustomSearch
from google_images_search.fetch_resize_save import FetchResizeSave

items = {
    'items': [
        {'link': 'https://www.gstatic.com/webp/gallery3/1.png'},
        {'link': 'https://www.gstatic.com/webp/gallery3/2.png'}
    ]
}

GoogleCustomSearch._query_google_api = \
    lambda self, search_params, cache_discovery: items


class TestFetchResizeSave(unittest.TestCase):

    def setUp(self):
        self._api_key = '__api_key__'
        self._api_cx = '__api_cx__'
        self._frs = FetchResizeSave(self._api_key, self._api_cx)

        self._base_dir = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            ), 'tests'
        )
        self._file_paths = [
            os.path.join(self._base_dir, '1.png'),
            os.path.join(self._base_dir, '2.png'),
        ]

    def tearDown(self):
        self._frs = None
        for path in self._file_paths:
            try:
                os.remove(path)
            except OSError:
                pass

    def test_init(self):
        self.assertEqual(self._frs._search_resut, [])

    def test_search_url(self):
        self._frs.search({})
        for i, item in enumerate(self._frs.results()):
            self.assertEqual(item.url, items['items'][i]['link'])

    def test_search_path(self):
        self._frs.search({}, path_to_dir=self._base_dir, width=100, height=100)
        for i, item in enumerate(self._frs.results()):
            self.assertEqual(item.path, self._file_paths[i])


if __name__ == '__main__':
    unittest.main()
