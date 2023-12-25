import os
import sys
from pathlib import Path
from textwrap import wrap
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

year = sys.argv[1]
day = sys.argv[2]

token: str = Path(".token").read_text().strip()
html: str = (
    urlopen(
        Request(
            f"https://adventofcode.com/{year}/day/{day}",
            headers={"Cookie": f"session={token}"},
        )
    )
    .read()
    .decode("utf-8")
)
(Path.cwd() / year / day / "PROBLEM.html").write_text(html)


def text(item: ET.Element) -> str:
    return (item.text or "") + "".join(text(e) for e in item) + (item.tail or "")


with (Path.cwd() / year / day / "PROBLEM.md").open("w") as f:

    def render(item: ET.Element) -> str:
        match item.tag:
            case "h2":
                return f"## {item.text}\n\n"

            case "p":
                return (
                    "\n".join(
                        wrap(
                            (item.text or "")
                            + "".join(render(e) for e in item)
                            + (item.tail or ""),
                            width=80,
                        )
                    )
                    + "\n\n"
                )

            case "pre":
                return f"```\n{os.linesep.join(text(code).rstrip(os.linesep) for code in item)}\n```\n{item.tail or ''}"

            case "em":
                return f"**{item.text or ''}{''.join(render(e) for e in item)}**{item.tail or ''}"

            case "span":
                return (
                    (item.text or "")
                    + "".join(render(e) for e in item)
                    + (item.tail or "")
                )

            case "article":
                return (
                    (item.text or "")
                    + "".join(render(e) for e in item)
                    + (item.tail or "")
                )

            case "code":
                return f"`{item.text or ''}{''.join(e.text for e in item)}`{item.tail or ''}"

            case "a":
                return f"[{item.text}]({item.attrib['href']}){item.tail or ''}"

            case "ul":
                return "\n".join(f"- {render(e)}" for e in item) + "\n\n"

            case "li":
                return "\n".join(
                    wrap(
                        (item.text or "")
                        + "".join(render(e) for e in item)
                        + (item.tail or ""),
                        width=78,
                    )
                )

            case _:
                print("Unknown tag:", item.tag)

    start = 0
    while True:
        start = html.find("<article ", start)
        if start == -1:
            break
        end = html.find("</article>", start)
        article_html = html[start : end + 10]
        try:
            article = ET.fromstring(article_html)
        except Exception as e:
            print("Failed to parse article:", e)
            break
        start = end

        print(render(article), file=f)
