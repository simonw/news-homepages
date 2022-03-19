```{include} _templates/nav.html
```

# Adding a site

## Add record to sites file

Adding a new site requires that a new row be added to [`newshomepages/sources/sites.csv`](https://github.com/palewire/news-homepages/blob/main/newshomepages/sources/sites.csv) with, at a minimum, the handle, URL, name and timezone of the target. You can also override the system’s defaults by adding optional attributes for the width, height and time delay for the screenshots.

## Test the screenshot

After doing that, you should verify the site works by running the `shoot.py` command and inspecting the result.

```bash
pipenv run python -m newshomepages.tweet single your-sites-handle
```

## Hide ads and pop ups

If there are popups or ads that interfere with the screenshot, you should devise a file in [`newshomepages/sources/javascript`](https://github.com/palewire/news-homepages/tree/main/newshomepages/sources/javascript). It’s name should be slugged to match the handle in the sites data file. Consult the examples there to borrow techniques for targeting and hiding page elements.

## Add to a bundle

Then you should link the site’s row to one of the regional bundles defined in [`newshomepages/sources/bundles.csv`](https://github.com/palewire/news-homepages/blob/main/newshomepages/sources/bundles.csv). This is done by putting the slug of the desired bundle into the site’s bundle field.

If an suitable bundle does not exist, you can add one to the bundle data file, filling out the fields there.

New bundles also require the creation of a workflow file [`.github/workflows`](https://github.com/palewire/news-homepages/tree/main/.github/workflows) to run the code on a schedule. You can copy one of the examples there as a starting point.
