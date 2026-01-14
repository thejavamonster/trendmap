import requests
import json

states = [
    "US-AL","US-AK","US-AZ","US-AR","US-CA","US-CO","US-CT","US-DE",
    "US-FL","US-GA","US-HI","US-ID","US-IL","US-IN","US-IA","US-KS",
    "US-KY","US-LA","US-ME","US-MD","US-MA","US-MI","US-MN","US-MS",
    "US-MO","US-MT","US-NE","US-NV","US-NH","US-NJ","US-NM","US-NY",
    "US-NC","US-ND","US-OH","US-OK","US-OR","US-PA","US-RI","US-SC",
    "US-SD","US-TN","US-TX","US-UT","US-VT","US-VA","US-WA","US-WV",
    "US-WI","US-WY"
]

trends = {}

for state in states:
    url = f"https://trends.google.com/trending/rss?geo={state}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        text = r.text

        # parse top <item> manually
        start = text.find("<item>")
        end = text.find("</item>")
        if start != -1 and end != -1:
            item_xml = text[start:end]
            title_start = item_xml.find("<title>") + len("<title>")
            title_end = item_xml.find("</title>")
            link_start = item_xml.find("<link>") + len("<link>")
            link_end = item_xml.find("</link>")
            title = item_xml[title_start:title_end].strip()
            link = item_xml[link_start:link_end].strip()
            trends[state] = {"title": title, "link": link}
        else:
            trends[state] = {"title": None, "link": None}
    except Exception as e:
        trends[state] = {"title": None, "link": None}
        print(f"Error fetching {state}: {e}")

with open("trends.json", "w") as f:
    json.dump(trends, f, indent=2)
