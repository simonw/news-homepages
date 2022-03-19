Screenshots of news homepages around the world

Follow on Twitter at [@newshomepages](https://twitter.com/newshomepages)

## Getting started

Fork the repository and clone it. Move into the code directory and install the Python dependencies.

```bash
pipenv install --dev
```

Install pre-commit hooks.

```bash
pipenv run pre-commit install
```

Install the shot-scraper web browser.

```bash
pipenv run shot-scraper install
```

## Adding a site

Adding a new site requires that a new row be added to [`newshomepages/sources/sites.csv`](./newshomepages/sources/sites.csv) with, at a minimum, the handle, URL and timezone of the target. You can also override the system’s defaults by adding optional attributes for the width, height and time delay for the screenshots.

After doing that, you should verify the site works by running the `shoot.py` command and inspecting the result.

Then you should add the site to our schedule by inserting its handle name in the `matrix` of the relevant[GitHub Action workflow](https://github.com/palewire/news-homepages/blob/main/.github/workflows/socal.yml#L15).
