# Django toplevel files

Simple [Django](http://djangoproject.com) app to manage a few admin-uploaded
files intended to be available at the site root. Typically, those would be:
[/sitemap.xml](http://www.sitemaps.org/) and
[/robots.txt](http://www.robotstxt.org/). It allows to avoid using SSH or
FTP by end users of the site and integrates into Django admin interface.

For more sophisticated way of managing this data, please look at
[django.contrib.sitemaps](https://docs.djangoproject.com/en/dev/ref/contrib/sitemaps/)
and [django-robots](https://github.com/jezdez/django-robots/).

Using it for some random arbitrary named files is not very practical, as this
app mostly depends on the way your web server or project urlconf is setup. Note
that app does not validate file path and allows to create a file within
subdirectories adjacent to `MEDIA_ROOT` (such files are not very useful
though).

## Usage

 * Install with your favourite method (note, the app is not on PyPi yet).
 * Add 'toplevel_files' to `INSTALLED_APPS`.
 * Run `manage.py syncdb` or `manage.py syncdb --migrate` if you are using
  South.
 * Configure your web server (the preferred way) and/or urlconf.
 * Optionally setup permissions through 'django.contrib.auth' so that your
  users are allowed to add files, not file types.

### Rationale

I don't think it is a good idea to use a django view to serve such files:

 * Useful `urlconf` on a typical site for such a view would result in a
  database hit for every request or should be hardcoded.
 * Big (lenghty) files download would block a valuable python process/thread.

### Web server setup

Since, the intended usage is primarily serving a few known files within the
server root, it is more practical to have a suitable config for that.

Let's assume:

 * `MEDIA_ROOT` is something like `'%s/media/uploads' % PROJECT_ROOT`
 * your web server root is at `MEDIA_ROOT`
 * `@django` named location points where it should be (with fastcgi or uWSGI)

Here is [Nginx](http://nginx.org) example.

    location ~* ^/(robots.txt|sitemap.xml)$ {
        access_log  off;
        try_files   /uploads/$uri  other_path/$uri  @django;
    }

`other_path/$uri` can be used to provide scm-controlled location for those
files.

See [try_files](http://wiki.nginx.org/HttpCoreModule#try_files) directive for
details.

### Optional urlconf setup

Sometimes site urlconf is easier to edit than webserver's configuration. It is
not recommended, but you can serve these static files with Django itself.
To do so, just add something like this (probably at the top) to your project's
`ROOT_URLCONF`:

    (r'^(?P<filename>(robots\.txt|sitemap\.xml))/$', 'toplevel_files.views.serve')

Much less strict regexp can be used to match randomly named files typilcally
used by site ownership verfification mechanizms: ```[a-z0-9]+\.(txt|xml|html)```

Note:

 * you'll still have to create apropriate file type with exact file
  name.
 * a broad urlconf line placed on top may capture urls which you possibly
  expect to be handled with some other apps
  (`django.contrib.sitemaps`, for example).

The view checks if requested filename matches existing TopLevelFile object and
tries to read the file from disc. See this app's code and official Django
documentation on
[serving static files](https://docs.djangoproject.com/en/1.4/howto/static-files/#serving-other-directories).

## Internals

The app contains two models tied with one-to-one relationship: one to hold the
file type and the other with the actual file field. This is done to separate
permissions, so that only privileged users might create new file
types (paths, essentially).

 * Once the file is uploaded, it is not possible to change it's type via admin.
 * App subclasses django.core.files.storage.FileSystemStorage.
 * Admin actions are disabled for app's models, since they skip custom method
  we use to actually delete the file itself.
 * Updating an existing file would overwrite the target (unlike Django's
  default, wchich gives new file a unique non-conflicting name). This is what
  makes the app really useful.

### Compatibility

Using such web server setup ensures the Django would receive the request, if
there was no corresponding file found. This way you can use other apps to
manage those URLs and still being able to intercept requests with web server's
custom location processing.

### Note on development server

It's likely, you do not use real web server with fancy configs on your
development machine. Refer to urlconf setup if you want to check the app
works as expected during development.
