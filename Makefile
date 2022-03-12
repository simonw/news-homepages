clean:
	rm *.jpg
	rm *.png

install:
	pipenv run shot-scraper install


.PHONY: clean install
