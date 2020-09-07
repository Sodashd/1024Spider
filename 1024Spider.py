import requests
import re
import os


# headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
#            'cookie': '__cfduid=dc7958a4a96a220f01156690727eda6bd1599222163'
#            }
headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
           }


#第一步抓取主页面中的所有Link, 放到一个Linklist中
# https://cl.tc52.xyz/htm_data/2009/16/4059822.html


def GetLinklist(url,isOnlyGreen):

    mPage = requests.get(url, headers=headers).text
    if isOnlyGreen:
        mPat = re.compile(r'<a href="(.*?html)" target="_blank" id=""><font color=green>')
    else:
        mPat = re.compile(r'<a href="(.*?html)" target="_blank" id="">')
    
    LinkList = mPat.findall(mPage)
    return LinkList


# 第二步遍历Linklist中所有link，然后抓取所有图片Link
def GetPhotos(AllLink):
    for alink in AllLink:
        alink = 'https://cl.tc52.xyz/' + alink
        # alink= 'https://cl.tc52.xyz/htm_data/2008/16/4045162.html'
        html = requests.get(alink, headers=headers).text
        # res.encoding=res.apparent_encoding
        # html=res.text
        pat = re.compile(
            r"ess-data='(.*?)'")

        imgLink = pat.findall(html)

    # s='https://yuoimg.com/u/2020/08/10/\w+\.(jpg|gif)'
    # imgLink = re.findall(s,html)
    # print(html)
    # print(imgLink)

        for item in imgLink:
            name = item.split('/')[-1]
            try:
                picContent = requests.get(item, headers=headers,timeout=30).content
                # root="D:\\Works\\Developers\\C#\Images\\"
                Path=os.getcwd()+r'\Images'
                if not os.path.exists(Path):
                    os.mkdir(Path) 

                with open(Path+f"\{name}", 'wb') as fp:
                    fp.write(picContent)
                print(name+'finish!')
            except:
                pass

    print('全部完成!')

# 第三步将图片保存下载

# 第四步翻页

# def GetLink(url,re):
#     html=requests.get(url,)


if __name__ == "__main__":
    AllLink = []
    PageNo=int(input("请输入要爬取的页数："))
    isOnlyGreen=input("是否只爬取精华帖子？是，请输入Y；否，请输入N：")
    if isOnlyGreen.upper()=='Y':
        isOnlyGreen=True
    else:
        isOnlyGreen=False

    for i in range(PageNo):
        url = 'https://cl.tc52.xyz/thread0806.php?fid=16&search=&page='+str(i+1)
        AllLink = AllLink + GetLinklist(url,isOnlyGreen)
    GetPhotos(AllLink)
