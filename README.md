# ArrestOrg_Data_API
An unofficial API to scrape data from https://arrests.org , using Python and BeautifulSoup.

# Example Usage

```
import arrestorg, pprint
ao = arrestorg.arrestorg()
ao.SetState("california")
ao.SearchState(resultsperpage = 14, fname="Joseph")
p = pprint.PrettyPrinter()

arrestlist = ao.GetListOfArrests()
p.pprint(arrestlist)

arrestsdata = []
for arrest in arrestlist:
    arrest = ao.GetArrest(arrest)
    arrestsdata.append(arrest)
    p.pprint(arrest)

```
