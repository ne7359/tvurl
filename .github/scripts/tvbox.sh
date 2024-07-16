#!/bin/bash

find $GITHUB_WORKSPACE -maxdepth 1 -type f -name "*.json"

for file in $(find $GITHUB_WORKSPACE -maxdepth 1 -type f -name "*.json"); do
	sed -i '/^{"name":"磁力廣告"/ s/"regex":.*\]},/"regex":\["更多","最新","更新","直播","社區","社区","有趣","新葡京","英皇体育","新片首发","xuu","UUE29"\]},/' $file 2>/dev/null
done
sed -si '/"name":"live"/a\{"name":"俊于•综合","type":0,"url":"http://home.jundie.top:81/Cat/tv/live.txt","playerType":1,"epg":"http://epg.112114.xyz/?ch={name}&date={date}","logo": "https://epg.112114.xyz/logo/{name}.png"}, \
{"name":"tvboxtv","type":0,"url":"./tvboxtv.txt","playerType":1,"epg":"http://epg.112114.xyz/?ch={name}&date={date}","logo":"https://epg.112114.xyz/logo/{name}.png"}, \
{"name":"tvlive","type":0,"url":"./tvlive.txt","playerType":1,"epg":"http://epg.112114.xyz/?ch={name}&date={date}","logo":"https://epg.112114.xyz/logo/{name}.png"}, \
{"name":"YanG•综合","type":0,"url":"https://fongmi.cachefly.net/YanG-1989/m3u/main/Gather.m3u","playerType":1,"epg":"http://epg.112114.xyz/?ch={name}&date={date}","logo":"https://epg.112114.xyz/logo/{name}.png"}, \
{"name":"初秋语•综合","type":0,"url":"./list.txt","playerType":1,"epg":"http://epg.112114.xyz/?ch={name}&date={date}","logo":"https://epg.112114.xyz/logo/{name}.png"}, \
{"name":"YueChan•综合","type":0,"url":"https://fongmi.cachefly.net/YueChan/Live/main/IPTV.m3u","playerType":1,"epg":"http://epg.112114.xyz/?ch={name}&date={date}","logo":"https://epg.112114.xyz/logo/{name}.png"}, \
{"name":"Yoursmile•综合","type":0,"url":"https://agit.ai/Yoursmile7/TVBox/raw/branch/master/live.txt","playerType":1,"epg":"http://epg.112114.xyz/?ch={name}&date={date}","logo":"https://epg.112114.xyz/logo/{name}.png"}, \
{"name":"饭太硬•综合","type":0,"url":"https://agit.ai/fantaiying/0/raw/branch/main/tvlive.txt","playerType":1,"ua": "okhttp/3.15","epg":"http://epg.112114.xyz/?ch={name}&date={date}","logo": "https://epg.112114.xyz/logo/{name}.png"}, \
{"name":"肥猫•综合","type":0,"url":"http://我不是.肥猫.live/TV/tvzb.txt","playerType":1,"epg":"http://epg.112114.xyz/?ch={name}&date={date}","logo":"https://epg.112114.xyz/logo/{name}.png"},' $GITHUB_WORKSPACE/js.json $GITHUB_WORKSPACE/jsm.json 2>/dev/null
sed -szi 's|"ads":\[.*\]|"ads":\["raw.githubusercontent.com",\
".*boku.*",\
".*nivod.*",\
".*ulivetv.*",\
"ae01.alicdn.com",\
"api.htpan.net",\
"c.biggggg.com",\
"c.cnzz.com",\
"c.olddddd.com",\
"cdn.bootcss.com",\
"cdn.iz8qkg.com",\
"cdn.kin6c1.com",\
"cdn.v82u1l.com",\
"cdnjs.hnfenxun.com",\
"cms.qdwght.com",\
"cnzz.hhttm.top",\
"cnzz.mmstat.com",\
"ehwe.yhdtns.com",\
"f5w.as12df.top",\
"googlevideo.com",\
"haiwaikan.com",\
"hm.baidu.com",\
"img.mosflower.cn",\
"img.xunzhuo123.com",\
"iqiyi.hbuioo.com",\
"k.jinxiuzhilv.com",\
"k.wudejia.com",\
"mav.mavuz.com",\
"mc.usihnbcq.cn",\
"mg.g1mm3d.cn",\
"mimg.0c1q0l.cn",\
"mscs.svaeuzh.cn",\
"ppl.xunzhuo123.com",\
"q11.cnzz.com",\
"qiu.xixiqiu.com",\
"s13.cnzz.com",\
"s19.cnzz.com",\
"s23.cnzz.com",\
"s4.cnzz.com",\
"s9.cnzz.com",\
"s96.cnzz.com",\
"sp.chemacid.cn",\
"stj.v1vo.top",\
"thy.dacedsfa.cn",\
"tips.gamevvip.com",\
"tj.tianwenhu.com",\
"tp.vinuxhome.com",\
"uhibo.com",\
"um.cavuc.com",\
"vip.ffzyad.com",\
"vivovip.mmszxc.top",\
"wan.51img1.com",\
"wofwk.aoidf3.com",\
"www.92424.cn",\
"www.baihuillq.com",\
"www.google-analytics.com",\
"www.googletagmanager.com",\
"www.histar.tv",\
"www.jixunkyy.cn",\
"xc.hubeijieshikj.cn",\
"xdn.cqqc3.com",\
"xg.gars57.cn",\
"xg.huataisangao.cn",\
"xg.whsbpw.cn",\
"xomk.jiangjunmh.top",\
"youtube.com",\
"z1.cnzz.com",\
"z12.cnzz.com",\
"z2.cnzz.com",\
"z3.cnzz.com",\
"z5.cnzz.com",\
"z6.cnzz.com",\
"z7.cnzz.com",\
"z8.cnzz.com"\]|' $GITHUB_WORKSPACE/js.json $GITHUB_WORKSPACE/jsm.json 2>/dev/null
for file in $(find $GITHUB_WORKSPACE -maxdepth 1 -type f -name "*.txt"); do
	sed -i '/^DJ音乐,#genre#/d; /^斗鱼音乐/d; /^MTV/d; /^高清舞曲/d; /.mp4$/d; /.mov$/d; /^2022几首DJ串烧/d; /^$/d' $file 2>/dev/null
done
# rm -rf $GITHUB_WORKSPACE/9918.json
