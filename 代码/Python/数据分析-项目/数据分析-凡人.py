import requests
import pandas as pd
import xml.etree.ElementTree as ET

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.bilibili.com/"
}


# 获取番剧单集信息：ep_id -> bvid / cid / 标题
def get_ep_info(ep_id):
    url = "https://api.bilibili.com/pgc/view/web/season"

    r = requests.get(
        url,
        params={"ep_id": ep_id},
        headers=headers,
        timeout=10
    )

    result = r.json()["result"]
    episodes = result["episodes"]

    for ep in episodes:
        if str(ep["id"]) == str(ep_id):
            return {
                "ep_id": ep_id,
                "title": ep.get("long_title", ""),
                "bvid": ep.get("bvid", ""),
                "cid": ep.get("cid", "")
            }

    return None


# 获取普通视频统计信息：播放、点赞、投币、收藏等
def get_video_info(bvid):
    url = "https://api.bilibili.com/x/web-interface/view"

    r = requests.get(
        url,
        params={"bvid": bvid},
        headers=headers,
        timeout=10
    )

    result = r.json()

    if result.get("code") != 0:
        print(f"获取视频信息失败：{bvid}")
        return {
            "bvid": bvid,
            "view": None,
            "like": None,
            "coin": None,
            "favorite": None,
            "share": None,
            "reply": None
        }

    data = result["data"]
    stat = data["stat"]

    return {
        "bvid": bvid,
        "view": stat.get("view"),
        "like": stat.get("like"),
        "coin": stat.get("coin"),
        "favorite": stat.get("favorite"),
        "share": stat.get("share"),
        "reply": stat.get("reply")
    }


# 获取弹幕
def get_danmaku(cid):
    url = f"https://comment.bilibili.com/{cid}.xml"

    r = requests.get(url, headers=headers, timeout=10)
    r.encoding = "utf-8"

    root = ET.fromstring(r.text)
    rows = []

    for d in root.findall("d"):
        p = d.attrib["p"].split(",")

        rows.append({
            "time_sec": float(p[0]),
            "mode": p[1],
            "font_size": p[2],
            "color": p[3],
            "send_time": p[4],
            "text": d.text
        })

    return rows


# 这里放番剧链接里的 ep 号
ep_ids = [
    "3854801",
    "3854802",
    "733316",
    "733317",
    "733333",
    "733334",
    "428988",
    "428989",
    "471898",
    "471899",
    "762895",
    "762896",
    "1231533",
    "1231534"
]


video_rows = []
danmaku_rows = []

for ep_id in ep_ids:
    info = get_ep_info(ep_id)

    if info is None:
        print(f"没有找到 ep_id: {ep_id}")
        continue

    video_info = get_video_info(info["bvid"])

    video_info["ep_id"] = ep_id
    video_info["title"] = info["title"]
    video_info["cid"] = info["cid"]

    video_rows.append(video_info)

    danmus = get_danmaku(info["cid"])

    for item in danmus:
        item["ep_id"] = ep_id
        item["bvid"] = info["bvid"]
        item["title"] = info["title"]
        danmaku_rows.append(item)


video_df = pd.DataFrame(video_rows)
danmaku_df = pd.DataFrame(danmaku_rows)

video_df.to_csv( r"D:\python\1\pythontest\pythonProject1\数据分析-项目\bilibili_ep_info.csv", index=False, encoding="utf-8-sig")
danmaku_df.to_csv(r"D:\python\1\pythontest\pythonProject1\数据分析-项目\bilibili_danmaku.csv", index=False, encoding="utf-8-sig")

print(video_df)
print(danmaku_df.head())