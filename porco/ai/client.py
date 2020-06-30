import requests

def get_first(list_data):
    if list_data:
        return list_data[0]


class SmartItemClient:
    appid = "101007056"
    endpoint = "https://chuangyi.taobao.com/tools/smartPhrase"

    def __init__(self):
        self.session = requests.session()

    def init_app(self, app):
        csrf_token = app.config["SMART_ITEM_CSRF"]
        cookie = app.config["SMART_ITEM_COOKIE"]
        self.session.headers["x-csrf-token"] = csrf_token
        self.session.headers["cookie"] = cookie

    def get_smart_phrase(self, num_iid):
        resp = self.session.post(
            f"{self.endpoint}/generateSuit",
            json=dict(appid=self.appid, id=num_iid)
        )
        resj = resp.json()
        info = resj["result"]["info"]
        phrase = resj["result"]["phrase"]
        result = dict(
            title=info["title"],
            num_iid=num_iid,
            image=info["image"],
            short_title=get_first(phrase["onlineShortTitle"]),
            sellpoint=get_first(phrase["sellpoint"]),
            smartphrase=get_first(phrase["smartphrase"]),
        )
        return result

    def get_highlight(self, title):
        resp = self.session.post(
            f"{self.endpoint}/generateSingle",
            json=dict(
                appid=self.appid,
                title=title,
                scenes="recommend",
                textNum=1,
            )
        )
        resj = resp.json()
        return get_first(resj["result"])