# Beer-Advocate-Scraper

### Info
This scraper was built with python3 and scrapy 1.6.Install Scrapy with `pip install Scrapy`.
This spider scrapes beeradvocate.com and write all reviews, beers, and breweries into seperate csv files.

### How to run
With scrapy installed, open the terminal, go into 'beer_scraper' folder and run `scrapy crawl beer_comments`. The process of crawling data should take a few hours on a reasonable internet connection, and will be saved in your current working directory into three csv files.

## The Data

### About the data
Data are scraped from https://www.beeradvocate.com/, and are stored into 3 seperate csv files. breweryinfo.csv, beerinfo.csv, and comment.csv. Breweryinfo and beerinfo have identifying 'brewery_number' column, and beerinfo and comment have 'beer_number' as identifying keys to link them together. 

### Column Explained
Detailed information can be found [here](https://www.beeradvocate.com/community/threads/beeradvocate-ratings-explained.184726/)
1. breweryinfo
- beer_ratings: the total number of ratings users gave on beers produced by the brewery
- beer_reviews: the total number of reviews users gave on beers produced by the brewery
- beer_score: the mean score of all beers produced by the brewery by all users
- beers: the total number of beers the brewery produce
- brewery_name: the name of the brewery
- brewery_number: the identifying key of the brewery (Primary key)
- brewery_pdev: the percent of deviations within the ratings.
- brewery_ratings: the total number of ratings users gave for the brewery
- brewery_score: the total number of reviews users gave for the brewery
- city
- Country
- Province: States for the US, Province for other countries, and Country for the UK.

2. beerinfo
- beer_number: identifying key for beers (Primary Key)
- brewery_name: name of its brewery
- brewery_number: identifying key for its brewery (Foreign Key)
- note: brewer's additional information about the beer
- pdev
- ranking: weighted ranks of the beer
- ratings
- reviews
- style: style of the beer (eg. American Pale Ale APA)

3. comment
- ba_score:
- beer_number: identifying key for beers (Foreign Key)
- comment: User Comment
- date: date of comment
- feel
- look
- taste
- smell
- overal: User score beers based on the above 4 attributes, and the average is calculated as the overall
- username
