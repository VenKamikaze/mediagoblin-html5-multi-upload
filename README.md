mediagoblin-html5-multi-upload (0.5.0-dev)
==============================

Mediagoblin v0.5.0-dev html5 multi-upload plugin

This was based against mediagoblin v0.4.1 / 0.5.0-dev (early git clone, around 2013-08-26).
Does not work against 0.6.0-dev, and possibly not even for release v0.5.0 as it depends on functions in the standard upload form which have changed between releases.

To deploy, put the files from this github repository (0.5.0-dev branch) in your mediagoblin/plugins/ directory
Then, do:
<pre>
echo '[[mediagoblin.plugins.html5-multi-upload]]' >> /path/to/mediagoblin/mediagoblin_local.ini
</pre>
Then restart mediagoblin.

You should be able to reach the page at http://yoursite/html5-multi-upload/

Note that if using fcgi, you may need to increase the maximum size of a POST that it can process. I did this by adding this to my httpd configuration:
<pre>
# Accept up to 64MB requests
FcgidMaxRequestLen 67108864
</pre>
You'll probably have to do something similar for other methods aswell.

It requires HTML5 support to be able to add multiple files. Files are processed one at a time (at least with my instance). 
This was intentional, as I run my mediagoblin on a low power device with extremely limited CPU and RAM.

Hope this is useful for someone.
