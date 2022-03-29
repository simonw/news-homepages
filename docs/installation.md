```{include} _templates/nav.html
```

# Installation

Fork the repository and clone it. Move into the code directory and install the Python dependencies.

```bash
pipenv install --dev
```

Install pre-commit hooks.

```bash
pipenv run pre-commit install
```

Install Chrome as the shot-scraper web browser.

```bash
pipenv run shot-scraper install --browser=chrome
```

You're ready to work.
