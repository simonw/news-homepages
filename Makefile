clean:
	rm *.jpg
	rm *.png

install:
	pipenv run shot-scraper install

run:
	pipenv run shot-scraper multi config.yml


.PHONY: clean install run
