# Copyright (c) 2017, Matt Layman

import os
import tempfile

from handroll.site import Site
from handroll.tests import TestCase


class TestSite(TestCase):

    def test_finds_valid_site_root_from_templates(self):
        original = os.getcwd()
        valid_site = os.path.realpath(tempfile.mkdtemp())
        open(os.path.join(valid_site, 'template.html'), 'w').close()
        os.chdir(valid_site)

        site = Site()

        self.assertEqual(valid_site, site.path)
        os.chdir(original)

    def test_finds_valid_site_root_from_conf(self):
        original = os.getcwd()
        valid_site = os.path.realpath(tempfile.mkdtemp())
        open(os.path.join(valid_site, Site.CONFIG), 'w').close()
        os.chdir(valid_site)

        site = Site()

        self.assertEqual(valid_site, site.path)
        os.chdir(original)

    def test_site_has_absolute_path(self):
        original = os.getcwd()
        tempdir = os.path.realpath(tempfile.mkdtemp())
        site_path = os.path.join(tempdir, 'site')
        os.mkdir(site_path)
        os.chdir(tempdir)

        site = Site('site')

        self.assertEqual(site_path, site.path)
        os.chdir(original)

    def test_skips_directory(self):
        dirnames = ['keep', '.sass-cache', 'another_keeper']
        site = self.factory.make_site()

        site._prune_skip_directories(dirnames)

        self.assertEqual(2, len(dirnames))
        self.assertEqual('keep', dirnames[0])
        self.assertEqual('another_keeper', dirnames[1])
