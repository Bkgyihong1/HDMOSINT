from thesis.data_collectors import LinkedIncrawler, wikipediacrawler, twitterspider, insspider


class Crawler:
    def __init__(self):
        print("Collecting the target's social media names, incase you don't know, input None")
        self.firstname = input("Who is our target (Enter firstname) : ")
        self.surname = input("Who is our target (Enter surname): ")
        self.insuser = input("Enter the target's instagram handle: ")
        self.twitteruser = input("Enter the target's twitter handle: ")
        self.linkedin = input("Enter the Linkedin page link of the target,\n"
                              "Enter the end of the link after ..linkedin\in\: ")
        self.wiki()
        if self.twitteruser == ("None" or "none"):
            print("Unable to collect twitter data")
        else:
            self.twitter()

        if self.linkedin == ("None" or "none"):
            print("No Data collected from LinkedIn")
        else:
            self.li_link()

        if self.insuser == ("None" or "none"):
            print("Unable to collect instagram data")
        else:
            self.instagram()

    def li_link(self):
        linkedIn = LinkedIncrawler.LinkedInCrawl(self.linkedin)

    def wiki(self):
        wiki = wikipediacrawler.WikiPage(self.firstname, self.surname)

    def twitter(self):
        twitter = twitterspider.twittercollect(self.twitteruser)

    def instagram(self):
        instagram = insspider.InstagramOSINT(self.insuser)
