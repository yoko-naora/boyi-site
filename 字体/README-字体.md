# 字体来源与许可

20261020 起分两处取（子房定：中文衬线不自己子集化，改用 Google Fonts）：

| 字体 | 用在哪 | 从哪来 | 许可 |
|---|---|---|---|
| Noto Serif SC | 中文衬线（竖排标签、人名、汉字） | **Google Fonts**：`index.html` 里 `<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600&display=swap">`，浏览器按需分片下载，不占仓库 | SIL OFL 1.1（见 `OFL-notoserifsc.txt`） |
| Noto Serif | 英文衬线标题 | 站内 `字体/NotoSerif[wdth,wght].ttf`（20261020 从 `/home/jding/Herdr/业务/boyi/模板/字体/` 复制） | SIL OFL 1.1（见 `OFL-notoserif.txt`） |
| Oswald | 小号大写标签 | 站内 `字体/Oswald[wght].ttf`（同上复制） | SIL OFL 1.1（见 `OFL-oswald.txt`） |
| Allura | 手写签名 Yoko | 站内 `字体/Allura-Regular.ttf`（同上复制） | SIL OFL 1.1（见 `OFL-Allura.txt`） |
| Ma Shan Zheng | 首页人物廊的中文人名 | **Google Fonts**：`index.html` 的 `<link>` 里带 `family=Ma+Shan+Zheng`（不占仓库，全量 ttf 有 5.8 MB）；许可文本放在站内 `字体/OFL-mashanzheng.txt` | SIL OFL 1.1 |

为什么中文衬线改用 Google Fonts：全量 `NotoSerifSC[wght].ttf` 有 24 MB，放进仓库会让手机首屏很慢；子集化要装 fonttools（装软件得老丁批）。Google Fonts 免费、不用装软件。

为什么要复制进站：网站部署只带 `boyi-site` 仓库里的文件，仓外字体上线会 404。

源文件仍在 `/home/jding/Herdr/业务/boyi/模板/字体/`（模板和印刷品还在用）。
