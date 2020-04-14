# County Data Scraper

### Disclaimer: This project is meant for personal user and is very specific to my use case :(

That said, it scraps Wikipedia for Kenyan county data (counties, constituencies and wards).

The data on Wikipedia is incomplete and some constituency links point to pages that do not have ward data. If you need complete data, this is propably not what you should be using ~ but should be fine for test data.

### Usage:

```
# Python 3.7.5

pipenv install
pipenv shell
python scrapper.py
```

If all goes well, `python scrapper.py` will generate a `county.json` file containing data in the format below.

```
[
  {
    "county": "Mombasa ",
    "url": "https://en.wikipedia.org/wiki/Mombasa_County",
    "constituencies": [
      {
        "constituency": "Changamwe",
        "url": "https://en.wikipedia.org/wiki/Changamwe_Constituency",
        "wards": [
          "Changamwe",
          "Jomvu Kuu",
          "Kipevu",
          "Mikindani",
          "Miritini",
          "Port Reitz",
          "Tudor Estate",
          "Tudor Four"
        ]
      },
      {
        "constituency": "Jomvu",
        "url": "https://en.wikipedia.org/wiki/Jomvu_Constituency",
        "wards": []
      },
      {
        "constituency": "Kisauni",
        "url": "https://en.wikipedia.org/wiki/Kisauni_Constituency",
        "wards": [
          "Bamburi",
          "Frere Town",
          "Kizingo",
          "Kongowea",
          "Maweni",
          "Mjambere",
          "Mji wa Kale / Makadara",
          "Mwakirunge"
        ]
      },
      ...
    ]
  },
  ... 
]
```