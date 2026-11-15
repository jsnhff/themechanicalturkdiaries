# The Mechanical Turk Diaries

*Stories from Amazon's Anonymous Workforce.* A project by [Jason Huff](https://jasonhuff.info), 2009.

This is the site, kept on its own: all 357 stories from the Tumblr blog, at the same addresses they had
(`/post/<id>/`), in the look the blog had, with nothing behind it but static files. It is built with
Jekyll and served by GitHub Pages.

- The stories come from the archive, [jsnhff/mechanical-turk-diaries](https://github.com/jsnhff/mechanical-turk-diaries),
  which has each post with its Tumblr id, date and text. `tools/import_archive.py` turns those into `_posts/`.
- The words are people's own and are not processed: no smart quotes, no dashes, no ellipses. The only
  formatting kept is the italics and links the posts had. Dates are shown in the blog's own timezone
  (US/Eastern), as Tumblr showed them.
- The layout is the **Observer** theme by [Zack Sultan](http://zacksultan.com), which the blog used. The type is
  set after Robert Bringhurst's *The Elements of Typographic Style*, in EB Garamond ([SIL Open Font
  License](fonts/OFL.txt)): a measure of about 66 characters (measured, not guessed), 1.4 leading with every
  vertical space a multiple of a line, sizes on a perfect-fifth scale, indented paragraphs with no gap between,
  small capitals and letterspacing for capitals only, old-style figures in the text. The rules, and the reason for
  each, are in the comment at the top of `css/site.css`. The font is subset from the full release with its small
  capitals and figures kept; the copy Google serves has those removed.
- Apostrophes and quotation marks in story titles are set as typographer's marks (the source had straight ones).
  Nothing in a story's own text is changed: its straight marks are feet and inches.
- Tumblr's Ask box and its notes (who liked or reblogged a story) are not here; the posts' note counts are.

## Run it

```
bundle install
bundle exec jekyll serve
```

Then open <http://127.0.0.1:4000/>.

## Put it on themechanicalturkdiaries.com

The site is served from the domain (`baseurl` is empty and the `CNAME` file names it). It was first previewed at a
project address, with `baseurl: /themechanicalturkdiaries`. The steps that moved it:

1. Set `baseurl: ""` in `_config.yml`, and add a file named `CNAME` containing `themechanicalturkdiaries.com`.
2. In Cloudflare DNS, replace the proxied `A` record pointing at Tumblr (`66.6.44.4`) with four `A` records for
   `@` at `185.199.108.153`, `185.199.109.153`, `185.199.110.153` and `185.199.111.153`, set to *DNS only* until
   GitHub has issued its certificate, plus a `CNAME` for `www` to `jsnhff.github.io`.
3. In the repository's Pages settings, set the custom domain and turn on *Enforce HTTPS*.

To go back to Tumblr, restore the old `A` record and remove the `CNAME` file.

## Layout

```
_posts/            one file per story, named for the day and the words of its title
_layouts, _includes  the page, the header and footer, one story
index.html         the home pages, ten stories each, at / and /page/N/
archive.html       every story, by month
404.html           sends /post/<id>/<title-words> to /post/<id>/, the address Tumblr's links also use
tools/             the importer
```
