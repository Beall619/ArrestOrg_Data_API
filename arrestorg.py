import bs4, requests, random
class arrestorg():
    def __init__(self):
        self.state = ""
        self.arrestsession = requests.session()
        self.page = self.arrestsession.get("https://arrests.org/", headers = {'User-Agent': self.RandomAgent()})

    def RandomAgent(self):
        agents_list = []
        with open("useragents.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    agents_list.append(line)
        return agents_list[random.randint(0, len(agents_list))]

    def GetArrest(self, profilelink):
        arrestpage = self.arrestsession.get(profilelink, headers = {'User-Agent': self.RandomAgent()})
        #get the page in sessions
        arrestsoup = bs4.BeautifulSoup(arrestpage.content, "lxml")
        info = arrestsoup.find("div", { "class" : "info" })
        firstsec = info.find("div", {"class" : "section-content"})
        secondsec = info.find("div", {"class" : "section-content personal-information"})
        chargessec = arrestsoup.find("div", {"class" : "section-content charges"})
        arrestinfo = {}
        arrestinfo["arrest_url"] = profilelink
        arrestinfo["charges"] = []
        charges = []
        descriptions = []

        for i in firstsec.find_all("div"):
            i = i.text.replace("\n", " ").replace(": ", ":").split(":")
            if(i[0] == "Time"):
                k = i
                i = []
                i.append("Time")
                i.append(k[1] + ":" + k[2])
            arrestinfo[i[0]] = i[1]

        for i in secondsec.find_all("div"):
            i = i.text.replace("\n", " ").replace(": ", ":").split(":")
            arrestinfo[i[0]] = i[1]

        for charge in chargessec.find_all("div"):
            chargedict = {}
            if(charge.attrs == {'class': ['charge-title']}):
                charges.append(charge.text)
            else:
                if(charge.attrs == {'class': ['charge-description']}):
                    descriptions.append(charge.text)

        inc = -1
        for charge in charges:
            inc += 1
            chargedict = {}
            chargedict["charge"] = charge
            chargedict["description"] = descriptions[inc]
            arrestinfo["charges"].append(chargedict)
        return arrestinfo

    def GetArrestsInState(self):
        pagesoup = bs4.BeautifulSoup(self.page.content, "lxml")
        searchresultsoup = bs4.BeautifulSoup(str(pagesoup.find("div", { "class" : "search-results" })), "lxml")
        failedsearchtest = pagesoup.find("h2", { "class" : "search-failed" })
        faileddatatest = pagesoup.text
        if(failedsearchtest is not None or faileddatatest == 'database error' or faileddatatest == ""):
            if(failedsearchtest is not None):
                raise Exception("No results")
            if(faileddatatest == 'database error' or faileddatatest == ""):
                raise Exception("server returned nothing")
        arrests = []
        for arrest in searchresultsoup.find_all("div", { "class" : "profile-card" }, "lxml"):
            thissoup = bs4.BeautifulSoup(str(arrest), "lxml")
            profilelink = self.state + thissoup.find("a")["data-src"]
            arrests.append(self.GetArrest(profilelink))
        return arrests
    def SearchState(self, fname=None, lname=None, page=None, resultsperpage=None, partialmatch=True):
        ua = {'User-Agent': self.RandomAgent()}
        params = {}
        if(fname is None):
            pass
        elif(not(isinstance(fname, str))):
            raise TypeError("first name must be str")
        else:
            params["fname"] = fname
        if(lname is None):
            pass
        elif(not(isinstance(lname, str))):
            raise TypeError("last name must be str")
        else:
            params["lname"] = lname
        if(page is None):
            params["page"] = "1"
        elif(not(isinstance(page, int))):
            raise TypeError("page must be int")
        else:
            params["page"] = str(page)
        if(resultsperpage is None):
            params["results"] = "56"
        elif(not(isinstance(resultsperpage, int))):
            raise TypeError("resultsperpage must be int")
        else:
            params["results"] = str(resultsperpage)
        if(not(isinstance(partialmatch, bool))):
            raise TypeError("partial match must be bool")
        else:
            params["partialmatch"] = str(partialmatch)

        #print(self.state+"search.php/"+headerstring[:-1])
        #self.page = self.arrestsession.get(self.state+"search.php/"+headerstring[:-1])
        self.page = self.arrestsession.get(self.state, headers = ua, params = params)
    def statesf(self):
        return ['alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut', 'delaware', 'district of columbia', 'florida', 'georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 'kentucky', 'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota', 'mississippi', 'missouri', 'montana', 'nebraska', 'nevada', 'new hampshire', 'new jersey', 'new mexico', 'new york', 'north carolina', 'north dakota', 'ohio', 'oklahoma', 'oregon', 'pennsylvania', 'rhode island', 'south carolina', 'south dakota', 'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington', 'west virginia', 'wisconsin', 'wyoming']
    def statess(self):
        return ['ak', 'al', 'ar', 'az', 'ca', 'co', 'ct', 'dc', 'de', 'fl', 'ga', 'hi', 'ia', 'id', 'il', 'in', 'ks', 'ky', 'la', 'ma', 'md', 'me', 'mi', 'mn', 'mo', 'ms', 'mt', 'nc', 'nd', 'ne', 'nh', 'nj', 'nm', 'nv', 'ny', 'oh', 'ok', 'or', 'pa', 'ri', 'sc', 'sd', 'tn', 'tx', 'ut', 'va', 'vt', 'wa', 'wi', 'wv', 'wy']
    def SetState(self, state):
        self.pagenumber=1
        if(state.lower() in self.statesf() or state.lower() in self.statess()):
            try:
                link = 'https://'+ state +'.arrests.org/'
                headers = {'User-Agent': self.RandomAgent()}
                self.page = self.arrestsession.get(link, headers=headers)
                self.state = link
            except:
                raise ConnectionError(state + ' isnt compatible, check https://arrests.org for compatible states')
        else:
            raise ValueError(state + " isnt a state")

    def BuildAllStateSearch(self, headers, storelocation):
        page = None
        resultsperpage = 56
        statess = self.statess()
        #self.SearchState(headers)

