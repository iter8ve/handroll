# Copyright (c) 2015, Matt Layman

import mock

from handroll import scaffolder
from handroll.i18n import _
from handroll.tests import TestCase


class TestScaffolder(TestCase):

    def test_default_scaffolder_label(self):
        label = scaffolder.get_label('default')
        self.assertEqual(_('A complete site to get you going'), label)

    def test_list_format(self):
        display = scaffolder.display_scaffold('scaffold', 'It rocks')
        self.assertEqual('  scaffold    | It rocks', display)
        display = scaffolder.display_scaffold('short', 'Rocks too')
        self.assertEqual('  short       | Rocks too', display)

    @mock.patch('handroll.scaffolder.display_scaffold')
    def test_displays_scaffolds(self, display_scaffold):
        scaffolder.make(scaffolder.LIST_SCAFFOLDS, 'dontcare')
        self.assertTrue(display_scaffold.called)

    @mock.patch('handroll.scaffolder.make_scaffold')
    def test_makes_scaffold(self, make_scaffold):
        scaffolder.make('default', 'site')
        make_scaffold.assert_called_once_with('default', 'site')
