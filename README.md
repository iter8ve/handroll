handroll
========

Website development is a finely crafted art.

You need simple. You know what you're doing. You don't want to waste time.

`handroll` knows you are the boss. With one command, you gracefully blend your
theme and content into one precise result.

```bash
$ handroll site
Complete.
```

Just the facts
--------------

`handroll` walks your website source (i.e. `site` as shown above), copying
everything that it can find. When it encounters:

1.  `template.html` at the root of your site, the file will be skipped.
2.  anything ending in `.md`, the file will be read, the first line of the file
    will become the `title`, and the remainder will be converted from Markdown
    into HTML to become the `content`. `title` and `content` will be combined
    with `template.html` to produce the final HTML file.

