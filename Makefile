clean:
	rm *.jpg
	rm *.png

install:
	pipenv run shot-scraper install

run:
	pipenv run shot-scraper multi config.yml

tweet:
	pipenv run python tweet.py


.PHONY: clean install run tweet
