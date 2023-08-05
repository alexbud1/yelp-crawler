# yelp-crawler
This is CLI application written in Python with BeautifulSoup. It scraps all businesses from yelp.com on a basis of desired parameters.

Script parses all the businesses from yelp.com by entered category and location(city or city + country). It fetches ONLY results from part on website, that is showed like this : "All "{category}" results in {location}".
Results on all pages are parsed. The data is then written into a file "data.json" from dictionary. In case of no results - an exception is throwed.

In order to launch crawler follow this steps:
1. Clone repository
2. Install required modules using `pip install -r requirements.txt` or alternative command for your system
3. Launch crawler using command `python crawler.py {category} {city}`.


   Examples: `python crawler.py Contractors London` or `python crawler.py burgers "New York"`

If you encounter any bugs or have ideas for improvement - feel free to create an issue with this info.
