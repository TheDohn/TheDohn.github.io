
## Comparing long-term weather forecasts

A common debate in our household is whether it is worth commiting to long-term plans that are highly weather dependent. i.e. should we make nonrefundable reservations on a Monday for the following Sunday? In order to address this question I decided to see just how accurate some popular weather website's forecasts are. I could not find any saved long term forecasts, and many weather APIs are limited in their scope, so I wrote some code to scrape forecasts from a variety of popular weather websites. While I started this project with the intent to simply get ahold of some unique data to work with, the scraping ended up being a learning experience in and of itself. The code and results are in the 3 notebooks in this directory: 

* get_daily_weather_forecasts_notebook.ipynb: For scraping daily forecasts

* get_historical_weather_data.ipynb: For scraping historical weather forecasts

* weather_analysis.ipynb: The final analysis and plots, including some brief conclusions. 

I am overall not very satisfied with the final results since I only scraped for 1 month, which isn't a lot of data for a project like this. I had originally planned to scrape data for a second, longer, period of time but I have since abandoned this goal as I found that over time minor changes to the websites make it extremely difficult to run the scraping code for long periods of time without babysitting it. None-the-less all the scraping code did run and I consider the project complete.
