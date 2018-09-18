# AutoImagist Bot

This is some Python code that will create poems that are generically in the style of imagist poets like William Carlos Williams. It uses Microsoft Azure's Computer Vision API to describe random photos from Flickr, combines two or more of those descriptions to make similes or juxtapositions, then formats it like a poem.

Basically, it's [@PicDescBot](https://twitter.com/picdescbot) without the images and a little bit of poetic license.

If you want to run this on your own, store the essential credentials (Twitter, Flickr, and Azure keys) in a file called `keys`, and store the Mastodon user and client secret files in the same directory as `imagist.py`. Speaking of which, all directory paths in the example code are specific to my Raspberry Pi, so you should probably update that as well.
 
Check Out the Results:
 * Mastodon: [botsin.space/@AutoImagist](botsin.space/@AutoImagist)
 * Twitter: [@AutoImagist](http://www.twitter.com/autoimagist)
