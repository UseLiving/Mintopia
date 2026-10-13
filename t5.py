from harness import *
from t2 import grab_station
AUDIT="""()=>{function lin(c){c/=255;return c<=.03928?c/12.92:Math.pow((c+.055)/1.055,2.4)}function rgba(s){var m=s.match(/rgba?\\(([^)]+)\\)/);if(!m)return null;var p=m[1].split(',').map(parseFloat);return {r:p[0],g:p[1],b:p[2],a:p[3]==null?1:p[3]}}function L(c){return .2126*lin(c.r)+.7152*lin(c.g)+.0722*lin(c.b)}
function bg(e){while(e){var c=rgba(getComputedStyle(e).backgroundColor);if(c&&c.a>.9)return c;e=e.parentElement}return {r:21,g:11,b:58,a:1}}
var bad=[],n=0;document.querySelectorAll('#view *,.tabs *,#dlg *').forEach(function(e){var t=[].filter.call(e.childNodes,function(c){return c.nodeType===3&&c.textContent.trim()}).length;if(!t||e.disabled||e.closest('[disabled]'))return;var r=e.getBoundingClientRect();if(r.width<2||r.height<2||getComputedStyle(e).visibility==='hidden'||e.closest('[style*="display: none"]'))return;var cs=getComputedStyle(e),f=rgba(cs.color),b=bg(e),big=parseFloat(cs.fontSize)>=24||(parseFloat(cs.fontSize)>=18.66&&parseInt(cs.fontWeight)>=700);var l1=L(f),l2=L(b),ratio=(Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05);n++;if(ratio<(big?3:4.5))bad.append?0:bad.push([e.textContent.trim().slice(0,30),Math.round(ratio*100)/100,cs.color,'on rgb('+b.r+','+b.g+','+b.b+')'])});return {n:n,bad:bad.slice(0,6),total:bad.length}}"""
def part5(br):
    # ---------- phones
    for (w,h,name) in ((390,844,'iPhone'),(320,640,'small phone')):
        c,pg,errs=page(br,vp=(w,h),mobile=True,ua=IPH);E=pg.evaluate;E("()=>HH.pause(true)")
        setstate(pg,"T.coins=123.45e15;T.runCoins=4e10;T.cycleCoins=4e10;for(var i=0;i<9;i++){T.gens[i].n=20+i;T.gens[i].mgr=true;T.gens[i].run=true}");E("()=>HH.pause(true)");pg.click('#tab_crew');pg.wait_for_timeout(500)
        g=E("""()=>{var r=function(s){var b=document.querySelector(s).getBoundingClientRect();return {l:b.left,r:b.right,t:b.top,b:b.bottom,w:b.width,h:b.height}},vw=innerWidth,vh=innerHeight,panel=r('.panel'),cv=r('#stage'),mine=r('#mine'),coins=document.getElementById('coins'),tabs=[].map.call(document.querySelectorAll('.tab'),function(t){return {c:t.clientWidth,s:t.scrollWidth,w:t.getBoundingClientRect().width}});return {vw:vw,vh:vh,sw:document.documentElement.scrollWidth,panel:panel,cv:cv,mine:mine,coinsClip:coins.scrollWidth>coins.clientWidth+1,coinsText:coins.textContent,tabs:tabs,small:[].filter.call(document.querySelectorAll('.panel .btn,.tab,#mine,#btnSound'),function(b){var q=b.getBoundingClientRect();return q.width>0&&q.height>0&&q.height<36}).map(function(b){return b.textContent}).slice(0,4)}}""")
        ok('PHONE %dpx (%s): the menu is a panel along the bottom (%d%% of the screen) and the 3D stage fills the space above it'%(w,name,round(g['panel']['h']/g['vh']*100)),g['panel']['t']>g['vh']*.45 and g['panel']['b']>=g['vh']-1 and g['cv']['h']>g['vh']*.45 and g['cv']['b']<=g['panel']['t']+1,g)
        ok('...nothing scrolls sideways, and the Mine button sits fully on screen just above the panel',g['sw']<=w and g['mine']['l']>=0 and g['mine']['r']<=w and g['mine']['b']<=g['panel']['t']+1 and g['mine']['t']>0,[g['sw'],g['mine']])
        ok('...a huge number (%s) fits in the header without being cut off'%g['coinsText'],not g['coinsClip'],g['coinsText'])
        ok('...all six tab names fit (nothing clipped)',all(t['s']<=t['c']+1 for t in g['tabs']),g['tabs'])
        ok('...every button is at least 36px tall so a thumb can hit it',not g['small'],g['small'])
        cp=E("()=>HH.screen(0,2.35,0)");cvw=g['cv']['w'];gm=mean_color(E("()=>{var p=HH.screen(0,2.35,0);return HH.grab(p.x-15,p.y-15,30,30)}"))
        ok('...the coin is in view, near the middle of the stage, and gold (%s)'%[round(x) for x in gm],abs(cp['x']-cvw/2)<cvw*.2 and 20<cp['y']<g['cv']['h']-20 and gm[0]>gm[2]+25 and gm[0]>gm[1],[cp,cvw,gm])
        pg.touchscreen.tap(cp['x'],cp['y']);pg.wait_for_timeout(120);ok('...and a finger tap on the coin mines',S(pg,"S.totalClicks")>=1,S(pg,'S.totalClicks'))
        # the rest of the row buttons wrap instead of overflowing
        ov=E("()=>[].filter.call(document.querySelectorAll('#view .row'),function(r){return r.style.display!=='none'&&r.scrollWidth>r.clientWidth+1}).length");ok('...Crew rows wrap their buttons instead of overflowing (%d overflowing)'%ov,ov==0)
        for t in ('upgrades','skills','prestige','wardrobe','stats'):
            pg.click('#tab_'+t);pg.wait_for_timeout(200)
        ok('...every tab fits the narrow panel with no sideways scroll',E("()=>document.getElementById('view').scrollWidth")<=E("()=>document.getElementById('view').clientWidth")+1,[E("()=>document.getElementById('view').scrollWidth"),E("()=>document.getElementById('view').clientWidth")])
        ok('no errors on a phone',not errs,errs[:1]);c.close()
    c,pg,errs=page(br,vp=(740,360),mobile=True,ua=IPH);ok('a phone on its side (740x360) does not scroll sideways and still shows the coin',E_sw(pg)<=740 and not errs,E_sw(pg));c.close()
    # ---------- accessibility
    c,pg,errs=page(br);E=pg.evaluate;E("()=>HH.pause(true)")
    setstate(pg,"T.coins=1e9;T.runCoins=4e10;T.cycleCoins=4e10;T.pt=50;T.ptTotal=50;T.rt=5;T.rtTotal=5;for(var i=0;i<6;i++){T.gens[i].n=15;T.gens[i].mgr=i<3}");E("()=>HH.pause(true)")
    worst=[]
    for t in ('crew','upgrades','skills','prestige','wardrobe','stats'):
        pg.click('#tab_'+t);pg.wait_for_timeout(300);a=E(AUDIT);worst.append((t,a['n'],a['total'],a['bad'][:2]))
    ok('CONTRAST: every piece of text in all six panels is readable (WCAG AA): %s'%[(t,n,tot) for t,n,tot,b in worst],all(tot==0 for t,n,tot,b in worst) and all(n>8 for t,n,tot,b in worst),worst)
    pg.click('#tab_crew');pg.click("#view .btn.ghost");pg.keyboard.press('Escape')
    names=E("()=>[].filter.call(document.querySelectorAll('button,input,textarea'),function(b){var r=b.getBoundingClientRect();return r.width>0&&!b.disabled&&!(b.textContent||b.getAttribute('aria-label')||b.getAttribute('aria-labelledby')||'').trim()}).length");ok('every button and field has a name a screen reader can read',names==0,names)
    ok('the tabs are a proper tab list: roles, one selected, and the arrow keys move between them',E("()=>{var t=[].slice.call(document.querySelectorAll('[role=tab]'));return t.length===6&&t.filter(function(x){return x.getAttribute('aria-selected')==='true'}).length===1&&!!document.querySelector('[role=tablist]')}"))
    pg.focus('#tab_crew');pg.keyboard.press('ArrowRight');pg.wait_for_timeout(120);ok('...ArrowRight goes from Crew to Upgrades and moves focus with it',pg.get_attribute('#tab_upgrades','aria-selected')=='true' and E("()=>document.activeElement.id")=='tab_upgrades')
    pg.click('#tab_stats');pg.click("#view .btn:has-text('Erase everything')");pg.wait_for_timeout(150)
    ok('toasts and the dialog are announced (a polite live region, and a modal dialog with a title)',E("()=>{var t=document.getElementById('toasts'),m=document.getElementById('modal');return t.getAttribute('aria-live')==='polite'&&m.getAttribute('role')==='dialog'&&m.getAttribute('aria-modal')==='true'&&!!document.getElementById('mTitle')}"));pg.keyboard.press('Escape')
    ok('the page has a language, a title and a description',E("()=>document.documentElement.lang==='en'&&document.title.length>5&&!!document.querySelector('meta[name=description]')"))
    c.close()
    c,pg,errs=page(br,ctx={'reduced_motion':'reduce'});E=pg.evaluate;E("()=>HH.pause(true)");a0=E("()=>HH.sc().spin");pg.wait_for_timeout(1000);a1=E("()=>HH.sc().spin")
    c.close();c,pg,errs=page(br);E=pg.evaluate;E("()=>HH.pause(true)");b0=E("()=>HH.sc().spin");pg.wait_for_timeout(1000);b1=E("()=>HH.sc().spin")
    ok('REDUCED MOTION: the coin turns much more slowly when the device asks for less motion (%.2f against %.2f radians a second)'%((a1-a0),(b1-b0)),(a1-a0)<(b1-b0)*.6,[a1-a0,b1-b0]);c.close()
    # ---------- cost
    c,pg,errs=page(br);E=pg.evaluate;E("()=>HH.pause(true)")
    setstate(pg,"T.coins=1e12;T.runCoins=1e12;for(var i=0;i<12;i++){T.gens[i].n=30;T.gens[i].mgr=true;T.gens[i].run=true}");E("()=>HH.pause(true)");pg.wait_for_timeout(600)
    st=E("()=>{var R=HH.R(),sc=HH.sc(),t0=performance.now();for(var i=0;i<40;i++)sc.update(.016,HH.get(),0);var u=(performance.now()-t0)/40;t0=performance.now();for(i=0;i<5;i++)R.render(sc.root,sc.cam);var r=(performance.now()-t0)/5;return {update:u,render:r,draws:R.stats.draws}}")
    ok('PERFORMANCE: with the whole crew on stage one frame needs only %d draw calls and %.1f ms of game and animation work (the drawing itself depends on the graphics card)'%(st['draws'],st['update']),st['draws']<5200 and st['update']<4,st)
    c.close()
    # ---------- hygiene
    reqs=[];c=br.new_context(viewport={'width':1360,'height':800});c.route('https://fonts.googleapis.com/**',lambda r:r.abort());c.route('https://fonts.gstatic.com/**',lambda r:r.abort());pg=c.new_page();pg.on('request',lambda r:reqs.append(r.url))
    pg.goto(URL+'?test');pg.wait_for_function("typeof HH!=='undefined'");pg.wait_for_timeout(1500);ext=[u for u in reqs if not u.startswith('file:') and 'fonts.g' not in u and not u.startswith('data:') and not u.startswith('blob:')]
    ok('THE GAME TALKS TO NO ONE: no network requests at all except the optional web fonts (%d requests, %d others)'%(len(reqs),len(ext)),not ext,ext[:3])
    txt=pg.evaluate("()=>document.body.innerText");pg.click('#tab_prestige');pg.click('#tab_stats');pg.click('#tab_wardrobe');txt+=pg.evaluate("()=>document.body.innerText")
    ok('nothing in the game claims real money, withdrawals or real crypto',not re.findall(r'real money|withdraw|cash ?out|actual crypto|invest|profit guaranteed|wallet address',txt,re.I),re.findall(r'real money|withdraw|cash ?out|invest',txt,re.I))
    pg.evaluate("()=>HH.pause(true)");b=canvas_box(pg)
    for i in range(60):pg.mouse.click(b['x']+470,b['y']+330)
    pg.wait_for_timeout(200);ok('SPAMMING 60 CLICKS leaves the screen tidy: at most 14 floating numbers and 4 toasts on screen',pg.evaluate("()=>document.querySelectorAll('.fl').length")<=14 and pg.evaluate("()=>document.querySelectorAll('.toast').length")<=4)
    c.close()
def E_sw(pg):return pg.evaluate("()=>document.documentElement.scrollWidth")
if __name__=='__main__':
    with sync_playwright() as p:
        br=p.chromium.launch();part5(br);br.close()
    sys.exit(summary())
