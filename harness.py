import os,sys,json,re,time,subprocess,math
from playwright.sync_api import sync_playwright
HERE=os.path.dirname(os.path.abspath(__file__))
for c in (os.path.join(HERE,'..','public','index.html'),os.path.join(HERE,'..','mintopia.html')):
    if os.path.exists(c):URL='file://'+os.path.abspath(c);break
PASS=0;FAIL=0;ERR=[]
IPH='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
def ok(name,cond,detail=None):
    global PASS,FAIL
    if cond:PASS+=1;print('PASS',name)
    else:FAIL+=1;print('FAIL',name,'|',json.dumps(detail,default=str)[:260] if detail is not None else '')
BENIGN=re.compile(r'ERR_NAME_NOT_RESOLVED|GroupMarkerNotSet|GL Driver Message|software WebGL|Failed to load resource|ReadPixels',re.I)
def page(br,vp=(1360,800),mobile=False,ua=None,init=None,query='?test',noGL=False,storage=None,route_fonts=True,ctx=None):
    c=br.new_context(viewport={'width':vp[0],'height':vp[1]},is_mobile=mobile,has_touch=mobile,user_agent=ua,device_scale_factor=1,**(ctx or {}))
    if route_fonts:
        c.route('https://fonts.googleapis.com/**',lambda r:r.abort());c.route('https://fonts.gstatic.com/**',lambda r:r.abort())
    if noGL:c.add_init_script("(function(){var o=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(t){if(t==='webgl'||t==='experimental-webgl'||t==='webgl2')return null;return o.apply(this,arguments)}})()")
    if storage is not None:c.add_init_script("try{if(!sessionStorage.getItem('__seeded')){localStorage.setItem('mintopia_save_v1',%s);sessionStorage.setItem('__seeded','1')}}catch(e){}"%json.dumps(storage))
    if init:c.add_init_script(init)
    pg=c.new_page();errs=[];pg.on('pageerror',lambda e:errs.append('PAGEERROR '+str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' and not BENIGN.search(m.text) else None)
    pg.goto(URL+query);pg.wait_for_function("typeof HH!=='undefined'&&HH.get()!==null",timeout=8000);pg.wait_for_timeout(300)
    return c,pg,errs
def setstate(pg,js):
    pg.evaluate("()=>{var T=newGame(Date.now()/1000);%s;HH.set(T);HH.nextAir(1e9)}"%js);pg.wait_for_timeout(150)
def S(pg,expr):return pg.evaluate("()=>{var S=HH.get();return %s}"%expr)
def canvas_box(pg):return pg.query_selector('#stage').bounding_box()
def click_coin(pg,n=1):
    b=canvas_box(pg);p=pg.evaluate("()=>{var s=HH.screen(0,2.35,0);return s}")
    for _ in range(n):pg.mouse.click(b['x']+p['x'],b['y']+p['y'])
    return p
def lum(c):return .299*c[0]+.587*c[1]+.114*c[2]
def mean_color(g):
    d=g['data'];n=len(d)//4;return [sum(d[i*4+k] for i in range(n))/n for k in range(3)]
def diff(a,b):
    n=min(len(a['data']),len(b['data']));return sum(abs(a['data'][i]-b['data'][i]) for i in range(0,n,4))/(n/4)
def summary():
    print('SUMMARY: %d/%d passed'%(PASS,PASS+FAIL));return FAIL
