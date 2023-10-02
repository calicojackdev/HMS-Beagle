# HMS Beagle   
![HMS Beagle in Straits of Magellan](https://digitalcollections.lib.washington.edu/digital/api/singleitem/image/fishimages/47233/default.jpg)  
HMS Beagle was a British brig that surveyed South America and later Australia, commanded by Robert FitzRoy for the South American voyages. FitzRoy was the namesake of Mount Fitz Roy, the silhouette made famous by clothing company Patagonia.  

This code is intended to automate checking for new colorways of Patagonia's Snap-T Fleece and notify if any are found.  

### File Blurbs
`runner.py` scrape, then examine stock data  
`scrape_stock_data.py` scrape Patagonia's website for stock details about the popular Snap-T Fleece  
`examine_stock_data.py` compare stock data from the past two scrape runs to determine if any new colors in size medium have been added  
`queries.py` db queries used across files  
`helpers.py` miscellaneous functions  
`sitemap.py` for use in case of stale product urls  
`notify.py` notification logic  

### Links of Interest 
[HMS Beagle Wikipedia](https://en.wikipedia.org/wiki/HMS_Beagle)  
[HMS Beagle, 1820-1870](https://www.jstor.org/stable/43707188)  
[Francisco Moreno](https://fredericofreitas.org/2009/08/18/the-journeys-of-francisco-moreno/)  
[Fitz Roy Ascents](https://www.pataclimb.com/climbingareas/chalten/fitzgroup/fitz.html)  
[_Voyages of the Adventure and Beagle_](https://www.gutenberg.org/files/38961/38961-h/38961-h.htm)  
[_The Voyage of the Beagle_](https://www.gutenberg.org/cache/epub/944/pg944-images.html)  