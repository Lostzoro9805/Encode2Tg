import string

import anitopy
import country_converter as coco
import requests

from . import *
from .funcn import VERSION2, WORKING

SIZE_UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]


def get_readable_file_size(size_in_bytes) -> str:
    if size_in_bytes is None:
        return "0B"
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f"{round(size_in_bytes, 2)}{SIZE_UNITS[index]}"
    except IndexError:
        return "File too large"


url = "https://graphql.anilist.co"
anime_query = """
query ($id: Int, $idMal:Int, $search: String, $type: MediaType, $asHtml: Boolean) {
  Media (id: $id, idMal: $idMal, search: $search, type: $type) {
    id
    idMal
    title {
      romaji
      english
      native
    }
    format
    status
    description (asHtml: $asHtml)
    startDate {
      year
      month
      day
    }
    season
    episodes
    duration
    countryOfOrigin
    source (version: 2)
    trailer {
      id
      site
      thumbnail
    }
    coverImage {
      extraLarge
    }
    bannerImage
    genres
    averageScore
    nextAiringEpisode {
      airingAt
      timeUntilAiring
      episode
    }
    isAdult
    characters (role: MAIN, page: 1, perPage: 10) {
      nodes {
        id
        name {
          full
          native
        }
        image {
          large
        }
        description (asHtml: $asHtml)
        siteUrl
      }
    }
    studios (isMain: true) {
      nodes {
        name
        siteUrl
      }
    }
    siteUrl
  }
}
"""


async def parser(name):
    try:
        olif = Path("filter.txt")
        if olif.is_file():
            with open("filter.txt", "r") as file:
                fil = file.read()
                fil1 = fil.split("\n")[0]
                fil2 = fil.split("\n")[1]
                fil3 = fil.split("\n")[2]
                file.close()
        else:
            fil1 = ""
            fil2 = ""
            fil3 = ""
        if olif.is_file() and fil != "Disable":
            name = name.replace(fil1, "")
        if fil3 == "Disable":
            fil3 = ""
        na = anitopy.parse(f"{name}")
        print(na)
        try:
            b = na["anime_title"]
        except Exception:
            b = ""
        try:
            d = na["episode_number"]
        except Exception:
            d = ""
        try:
            c = na["anime_season"]
        except Exception:
            c = ""
        try:
            e = na["release_group"]
        except Exception as er:
            LOGS.info(er)
            e = ""
        try:
            s = na["subtitles"]
        except Exception:
            s = ""
        try:
            st = na["episode_title"]
            st = "" if st == "END" else st
            st = "" if "MULTi" in st else st
        except Exception:
            st = ""
        return b, d, c, e, fil2, fil3, s, st
    except Exception:
        pass


async def conconvert(iso2_codes):
    try:
        iso3_codes = coco.convert(names=iso2_codes, to="ISO3").capitalize()
    except Exception as er:
        LOGS.info(er)
    return iso3_codes


async def parse(name, kk, aa):
    try:
        b, d, c, e, fil2, fil3, s, st = await parser(name)
        if b is None:
            raise Exception("Parsing Failed")
        cb2 = "[ANi-MiNE]"
        con = ""
        olif = Path("filter.txt")
        if olif.is_file():
            try:
                variables = {"search": b, "type": "ANIME"}
                json = (
                    requests.post(
                        url, json={"query": anime_query, "variables": variables}
                    )
                    .json()["data"]
                    .get("Media")
                )
                b = f"{json['title']['english']}"
                b = f"{json['title']['romaji']}" if b == "None" else b
                if fil2 == "Disable":
                    fil2 = f"{json['countryOfOrigin']}"
                    fil2 = await conconvert(fil2)
            except Exception:
                pass
            b = string.capwords(b)
            if len(b) > 33:
                cb = b[:32] + "…"
                cb = cb.split(":")[0]
            else:
                cb = b
            bb = ""
            bb += "[A-M]"
            bb += f" {cb}"
            if c:
                bb += f" S{c}"
            if d:
                bb += f" - {d}"
            if VERSION2:
                bb += "v2"
            if fil2 != "Disable":
                bb += f" [{fil2}]"
            bb2 = bb.replace(cb, b)
            bb2 = bb2.replace("[A-M]", cb2)
            bb += ".mkv"
        else:
            variables = {"search": b, "type": "ANIME"}
            json = (
                requests.post(url, json={"query": anime_query, "variables": variables})
                .json()["data"]
                .get("Media")
            )
            b = f"{json['title']['english']}"
            b = f"{json['title']['romaji']}" if b == "None" else b
            con = f"{json['countryOfOrigin']}"
            con = await conconvert(con)
            g = f"{json.get('episodes')}"
            b = string.capwords(b)
            if len(b) > 33:
                cb = b[:32] + "…"
                cb = cb.split(":")[0]
            else:
                cb = b
            if "MULTi" in name:
                col = "MULTi"
            elif "DUAL" in name or "Dual" in name:
                col = "Dual"
            elif "Yameii" in e:
                col = "Eng"
            else:
                col = con
            bb = ""
            bb += "[A-M]"
            bb += f" {cb}"
            if c:
                bb += f" S{c}"
            if d:
                bb += f" - {d}"
            if VERSION2:
                bb += "v2"
            if g == d:
                bb += " [END]"
            if col:
                bb += f" [{col}]"
            bb2 = bb.replace(cb, b)
            bb2 = bb2.replace("[A-M]", cb2)
            bb += ".mkv"
    except Exception as er:
        LOGS.info(er)
        bb = kk.replace(f".{aa}", " @Ani_Mine.mkv")
        bb2 = bb
    return bb, bb2


async def dynamicthumb(name, kk, aa):
    try:
        b, d, c, e, fil2, fil3, s, st = await parser(name)
        try:
            variables = {"search": b, "type": "ANIME"}
            json = (
                requests.post(url, json={"query": anime_query, "variables": variables})
                .json()["data"]
                .get("Media")
            )
            b = f"{json['title']['english']}"
            b = f"{json['title']['romaji']}" if b == "None" else b
        except Exception:
            pass
        if c:
            coy = c.replace("0", "")
            coy = f"{b} {coy}"
        else:
            coy = b
        variables = {"search": coy, "type": "ANIME"}
        json = (
            requests.post(url, json={"query": anime_query, "variables": variables})
            .json()["data"]
            .get("Media")
        )
        mog = f"{json.get('coverImage')['extraLarge']}"
        os.system(f"wget {mog} -O thumb2.jpg")
    except Exception:
        pass
    return b, d, e


async def custcap(name, fname):
    try:
        oi, z, y, e, fil2, fil3, s, st = await parser(name)
        if oi is None:
            raise Exception("Parsing Failed")
        try:
            if "MULTi" in name:
                fil3t = "(Multi-Audio) (Multi-Subs)"
            elif "B-Global" in name:
                fil3t = "(Multi-Subs) (B-Global)"
            elif "DUAL" in name or "Dual" in name:
                fil3t = "Dual Audio"
            elif "Multi" in name or "Multi-Subs" in name:
                fil3t = "Multi-Subs"
            elif s:
                fil3t = s
            else:
                fil3t = "English Subtitle"
        except Exception:
            pass
        olif = Path("filter.txt")
        if olif.is_file():
            pass
        else:
            fil3 = fil3t
        try:
            variables = {"search": oi, "type": "ANIME"}
            json = (
                requests.post(url, json={"query": anime_query, "variables": variables})
                .json()["data"]
                .get("Media")
            )
            oi = f"{json['title']['english']}"
            oi = f"{json['title']['romaji']}" if oi == "None" else oi
            g = f"{json.get('episodes')}"
        except Exception:
            g = ""
        oi = string.capwords(oi)
        caption = f"**◉ Title:** `{oi}`\n"
        if z:
            caption += f"**◉ Episode:** `{z}`"
        if VERSION2:
            caption += " (v2)"
        if VERSION2 and WORKING:
            caption += f"\n**◉ (V2) Reason:** `{VERSION2[0]}`"
        if z:
            caption += "\n"
        if y:
            caption += f"**◉ Season:** `{y}`\n"
        if fil3:
            fil3 = fil3.format(**locals())
            caption += f"**◉ Type:** `{fil3}`"
        if z == g:
            caption += " **[END]**\n"
        else:
            caption += "\n"
        if st:
            caption += f"**◉ Episode Title:** `{st}`\n"
        caption += "**🔗 @ANi_MiNE**"
    except Exception:
        om = fname.split(".")[0]
        ot = om.split("@")[0]
        caption = f"**{ot}**\n**🔗 @Ani_Mine**"
    return caption
