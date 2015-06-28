# Copyright (c) 2015, Matt Layman

import os

try:
    import ConfigParser as configparser
except ImportError:  # pragma: no cover
    import configparser

from werkzeug.contrib.atom import AtomFeed, FeedEntry

from handroll import date
from handroll.exceptions import AbortError
from handroll.extensions.base import Extension
from handroll.i18n import _


class BlogPost(object):

    def __init__(self, **kwargs):
        self.date = kwargs['date']
        self.source_file = kwargs['source_file']
        self.title = kwargs['title']
        self.url = kwargs['url']


class BlogExtension(Extension):
    """Track files marked as blog entries and generate a feed."""

    handle_frontmatter_loaded = True
    handle_pre_composition = True
    handle_post_composition = True

    required_metadata = {
        'author': 'atom_author',
        'id': 'atom_id',
        'title': 'atom_title',
        'url': 'atom_url',
    }

    def __init__(self, config):
        super(BlogExtension, self).__init__(config)
        self.posts = []
        self.atom_metadata = {}
        self.atom_output = ''
        self._resolver = None

    def on_pre_composition(self, director):
        """Check that all the required configuration exists."""
        if not self._config.parser.has_section('blog'):
            raise AbortError(
                _('A blog section is missing in the configuration file.'))
        for metadata, option in self.required_metadata.items():
            self._add_atom_metadata(metadata, option)
        self.atom_output = self._get_option('atom_output')
        # Grab the resolver from the director for determining URLs for posts.
        self._resolver = director.resolver

    def on_frontmatter_loaded(self, source_file, frontmatter):
        """Scan for blog posts.

        If a post is found, record it.
        """
        is_post = frontmatter.get('blog', False)
        if type(is_post) != bool:
            raise AbortError(
                _('Invalid blog frontmatter (expects True or False): '
                  '{blog_value}').format(blog_value=is_post))
        # TODO: Validate that the post has the required fields.
        if is_post:
            self._update_date(frontmatter)
            self.posts.append(BlogPost(
                date=frontmatter['date'],
                source_file=source_file,
                title=frontmatter['title'],
                url=self._resolver.as_url(source_file),
            ))

    def on_post_composition(self, director):
        """Generate the atom feed."""
        builder = FeedBuilder(self.atom_metadata)
        for post in self.posts:
            builder.add(post)
        output_file = os.path.join(director.outdir, self.atom_output)
        builder.write_to(output_file)

    def _add_atom_metadata(self, name, option):
        """Add atom metadata from the config parser."""
        self.atom_metadata[name] = self._get_option(option)

    def _get_option(self, option):
        """Get an option out of the blog section."""
        try:
            return self._config.parser.get('blog', option)
        except configparser.NoOptionError:
            raise AbortError(
                _('The blog extension requires the {option} option.').format(
                    option=option))

    def _update_date(self, frontmatter):
        """Update the frontmatter date into an actual datetime instance."""
        frontmatter['date'] = date.convert(frontmatter['date'])


class FeedBuilder(object):
    """Transform blog metadata and posts into an Atom feed."""

    def __init__(self, metadata):
        self.metadata = metadata
        self._feed = AtomFeed(**metadata)

    def add(self, post):
        """Add a blog post to the feed."""
        entry = FeedEntry(
            title=post.title,
            url=post.url,
            updated=post.date,
        )
        self._feed.add(entry)

    def write_to(self, filepath):
        """Write the feed to the provided filepath."""
        with open(filepath, 'wb') as out:
            out.write(self._feed.to_string().encode('utf-8'))
            out.write(b'<!-- handrolled for excellence -->\n')
