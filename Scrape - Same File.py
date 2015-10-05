from bs4 import BeautifulSoup
import requests
import time

page_number = 0
valid_page = True
number_quotes = 0

with open("Bash.org Scrape.txt", "w", encoding="utf-8") as f:
    print("Scrape started.")

    while valid_page is True:
        page_number += 1
        r = requests.get(
            "http://bash.org/?browse=" + str(page_number),
            stream=True
        )
        soup = BeautifulSoup(r.text, "html.parser")

        center_tags = soup.find_all("center")

        # Page validity check
        for center in center_tags:
            if center.contents[0] == "Invalid page.":
                valid_page = False

        if valid_page is True:
            print("Current page: " + str(page_number))

            # Get the stats for all of the quotes
            quotes_stat = soup.find_all("table")[3] \
                .find_all("p", {"class": "quote"})

            # Get the contents for all of the quotes
            quotes_content = soup.find_all("table")[3] \
                .find_all("p", {"class": "qt"})

            for i in range(len(quotes_stat)):
                number_quotes += 1
                f.write(quotes_stat[i].find_all("a")[0].contents[0].getText())
                f.write(" - (" + quotes_stat[i].find_all("font")[0]
                        .getText() + ")")
                f.write("\n")
                for row in quotes_content[i]:
                    if str(row) != "<br/>":
                        f.write(row.replace("\r", "").replace("\n", "") + "\n")
                f.write("\n")

        # You should probably control how fast you're making requests
        # but it shouldn't be too much trouble if you don't
        # time.sleep(1)

print("Scrape complete.")
print(str(number_quotes) + " quotes processed.")
