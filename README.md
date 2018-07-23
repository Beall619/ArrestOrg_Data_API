# ArrestOrg_Data_API
An unofficial API to scrape data from https://arrests.org , using Python and BeautifulSoup.

# ExampleUsage

```
import arrestorg, pprint
ao = arrestorg.arrestorg()
ao.SetState("california")
ao.SearchState(resultsperpage = 14, fname="Joseph", lname="j", page=1, partialmatch=True)
p = pprint.PrettyPrinter()
p.pprint(ao.GetArrestsInState())
```
