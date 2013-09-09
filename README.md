mediagoblin-html5-multi-upload
==============================

Mediagoblin v0.4.1 html5 multi-upload plugin

This was based against mediagoblin v0.4.1.
May not work against later versions of mediagoblin as it depends on functions in the standard upload form, but please give it a try, let me know how you go.

To deploy, put these files in your mediagoblin/plugins/ directory
Then, do:
echo '[[mediagoblin.plugins.html5-multi-upload]]' >> /path/to/mediagoblin/mediagoblin_local.ini

Restart mediagoblin.

You should be able to reach the page at http://yoursite/html5-multi-upload/

Note that if using fcgi, you may need to increase the maximum size of a POST that it can process. I did this by adding this to my httpd configuration:
# Accept up to 64MB requests
FcgidMaxRequestLen 67108864

You'll probably have to do something similar for other methods aswell.

It requires HTML5 support to be able to add multiple files. Files are processed one at a time (at least with my instance). 
This was intentional, as I run my mediagoblin on a low power device with extremely limited CPU and RAM.

Hope this is useful for someone.
