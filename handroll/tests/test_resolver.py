# Copyright (c) 2017, Matt Layman

import os

from handroll.composers import Composers
from handroll.resolver import FileResolver, URLResolver
from handroll.tests import TestCase


class TestFileResolver(TestCase):

    def test_as_url(self):
        site = self.factory.make_site()
        config = self.factory.make_configuration()
        composers = Composers(config)
        resolver = FileResolver(site.path, composers, config)
        md_file = os.path.join(site.path, 'a_dir', 'test.md')
        url = resolver.as_url(md_file)
        self.assertEqual('http://www.example.com/a_dir/test.html', url)

    def test_as_route(self):
        site = self.factory.make_site()
        config = self.factory.make_configuration()
        composers = Composers(config)
        resolver = FileResolver(site.path, composers, config)
        md_file = os.path.join(site.path, 'a_dir', 'test.md')
        route = resolver.as_route(md_file)
        self.assertEqual('/a_dir/test.html', route)


class TestURLResolver(TestCase):

    def test_use_relative_image(self):
        config = self.factory.make_configuration()
        base_url = 'https://www.example.com/route/default.png'
        resolver = URLResolver(config, '')
        url = resolver.resolve(base_url, 'python.png')
        self.assertEqual('https://www.example.com/route/python.png', url)

    def test_use_absolute_image(self):
        config = self.factory.make_configuration()
        base_url = 'https://www.example.com/route/default.png'
        resolver = URLResolver(config, '')
        url = resolver.resolve(base_url, '/images/javascript.png')
        self.assertEqual('http://www.example.com/images/javascript.png', url)

    def test_use_default(self):
        config = self.factory.make_configuration()
        resolver = URLResolver(config, 'https://www.example.com/default.png')
        url = resolver.resolve('', '')
        self.assertEqual('https://www.example.com/default.png', url)
