import re


def title_fix(title):
    title = title.replace(
        r"<em class='search-result-highlight'>", "").replace(r"</em>", "")
    return title


if __name__ == "__main__":
    text = "49个<em class='search-result-highlight'>Python</em> 学习必备资源，附链接 | 收藏"
    print(title_fix(text))
