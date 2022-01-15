import requests
from datetime import date

class notion:
    def __init__(self, notionSecret, notionDB):
        self.secret = notionSecret
        self.base_url = "https://api.notion.com/v1/databases/"
        self.database_id = notionDB
        self.date = str(date.today())
        self.header = {"Authorization":self.secret, "Notion-Version":"2021-08-16", "Content-Type": "application/json"}

    def taskToday(self):
        query = '{"filter":{"and":[{"property":"Done","checkbox":{"equals":false}},{"property":"Due","date":{"equals":'+'"'+self.date+'"'+'}}]}}'
        response = requests.post(self.base_url + self.database_id + "/query", headers=self.header, data=query)
        results = [i["properties"]["Task"]["title"][0]["text"]["content"] for i in response.json()["results"]]
        return results