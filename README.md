cwta
====

Chinese Wushu &amp; Taichi Association Website

## Code Structure
* **/redesign/website** - the new, redesigned website. Pretty much all changes should be made here
* **/redirector** - a small app for redirecting traffic from the old URL to the new one

## Setup

1. Download and install [Google AppEngine SDK for Python](https://cloud.google.com/appengine/downloads) (and Python if you need it)
2. [Fork this repo](https://help.github.com/articles/fork-a-repo/), and put it somewhere where you can remember
3. Open the Google App Engine Launcher (installed as part of the SDK)
4. Click File / Add Existing Application...
5. Choose the directory from step 2 and add the application

## Making changes
1. Update the version line in redesign/website/app.yaml. I typically just use the current date
1. Open the Google App Engine Launcher
2. Select the project (called "yijiaowushu-hrd") in the list and click the green "Run" button. This runs a small test server on your desktop so you can look at changes as you make them to the code
2. Click the "Browse" button to open the test server URL in your browser
3. Make changes to code. Refresh your browser to see the changes
4. When you're ready to publish changes, submit a [pull request](https://help.github.com/articles/using-pull-requests/)
5. I'll take care of publishing the changes once I approve the pull request
