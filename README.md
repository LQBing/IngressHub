# IngressHub

## software dependency

mysql, rabbitmq, python 2.7+ or python 3.4+, git

[https://github.com/LQBing/IngressHub/blob/master/INSTALL.md](https://github.com/LQBing/IngressHub/blob/master/INSTALL.md)

## clone project

    git clone git@github.com:LQBing/IngressHub.git

## install project python packages with pip

change direct to project folder

    pip install -r requirements.txt

## get cookies and field pars

Grab your cookies from Chrome F12 or Firefox and use the format like this:

    SACSID=AAAA...AAAA; csrftoken=BBBB....BBBB; ingress.intelmap.shflt=viz; ingress.intelmap.lat=40.0000000000000; ingress.intelmap.lng=120.00000000000000; ingress.intelmap.zoom=16

You can copy the field with this format from Chrome's F12.

Network, request 'getPlexts', right click, 'Copy as cURL', pick cookies and field info from it.

You will text as blow info:

    curl 'https://www.ingress.com/r/getPlexts' -H 'origin: https://www.ingress.com' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: zh-CN,zh;q=0.8' -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36' -H 'x-csrftoken: vjAhzZjmvV0HSdXn17GjUXmXHOlWVtPj' -H 'content-type: application/json; charset=UTF-8' -H 'accept: */*' -H 'referer: https://www.ingress.com/intel' -H 'authority: www.ingress.com' -H 'cookie: SACSID=AAAA...AAAA; csrftoken=BBBB....BBBB; ingress.intelmap.shflt=viz; ingress.intelmap.lat=40.0000000000000; ingress.intelmap.lng=120.00000000000000; ingress.intelmap.zoom=16' --data-binary '{"minLatE6":24443143,"minLngE6":117961106,"maxLatE6":24483299,"maxLngE6":118065219,"minTimestampMs":1469450441105,"maxTimestampMs":-1,"tab":"all","ascendingTimestampOrder":true,"v":"3372ba001844bd4a42680f3e6a2372d2490580f9"}' --compressed

get cookies from parameter `-H`  begin with `cookie: `, remove string `cookie: `

get field from parameter `--data-binary`, you get a json, `maxLngE6`, `maxLatE6`, `minLngE6`, `minLatE6` are useful for you.

## set configs

### sender

1. open manage page and login, open senders manage page

senders manage page : http://your.domain/admin/IngressWatcher/sender/

2. access add sender page

Click the button `ADD SENDER` on the top right of the page.

3. fill sender parameter

name : sender name

cookies : fill it with cookie you get

4 field parameters : fill them with you get.  They must be get from ingress intel site, or maybe cause error.

faction : the faction of sender account, it will affect welcome message send

disable : skip, or you want disable it.

### watcher

1. open manage page and login, open watchers manage page

watchers manage page : http://your.domain/admin/IngressWatcher/watcher/

2. access add sender page

Click the button `ADD WATCHER` on the top right of the page.

3. fill watcher parameter

name : watcher name

cookies : fill it with cookie you get

### watch point

1. open manage page and login, open watch points manage page

watch points manage page : http://your.domain/admin/IngressWatcher/watchpoint/

2. access add sender page

Click the button `ADD WATCH POINT` on the top right of the page.

3. fill watch point parameter

name : watch point name

4 field parameters : fill them with you get. They must be get from ingress intel site, or maybe cause error.

disable : skip, or you want disable it.

### setting

ps : must have and just one record


Welcome message send condition: choice a solution for welcome message send. Never send, just freshman, or all newcomers.

Welcome message : fill what message you want send to new agents.

Fetch message tab : witch messages need to get. just alert messages, faction messages, or all messages

Sender : select a sender for send welcome message.

watcher : select a watcher account for fetch messages.

watch point : select a field for fetch message, just one.


# quote

[https://github.com/LQBing/IngressApiParser](https://github.com/LQBing/IngressApiParser)
[https://github.com/blackgear/ingrex_lib](https://github.com/blackgear/ingrex_lib)
