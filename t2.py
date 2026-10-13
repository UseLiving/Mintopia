from harness import *
def stn_box(pg,i):
    p=pg.evaluate("i=>{var s=HH.station(i);return HH.screen(s.x,1.2,s.z)}",i);return p
def grab_station(pg,i,w=150,h=190):
    p=stn_box(pg,i);return pg.evaluate("([x,y,w,h])=>HH.grab(x-w/2,y-h*.65,w,h)",[p['x'],p['y'],w,h])
def part2(br):
    c,pg,errs=page(br);E=pg.evaluate
    setstate(pg,"T.coins=3");pg.click('#tab_crew');pg.wait_for_timeout(300)
    ok('CREW: only the first generator is shown to start with, as "Paper Wallet"',E("()=>[].filter.call(document.querySelectorAll('.row'),function(r){return r.style.display!=='none'}).length")==1 and pg.inner_text('#gen0 .rname').startswith('Paper Wallet'),E("()=>[].map.call(document.querySelectorAll('.row'),function(r){return r.style.display})"))
    ok('...the buy button is disabled while you cannot afford it, and says what it costs ("Buy first - 4")',E("()=>document.querySelector('#gen0 .btn.teal').disabled")and 'Buy first - 4' in pg.inner_text('#gen0'),pg.inner_text('#gen0'))
    S0=pg.evaluate("()=>{HH.get().coins=10;return 1}");pg.wait_for_timeout(350);ok('...and becomes available as soon as you have enough',not E("()=>document.querySelector('#gen0 .btn.teal').disabled"))
    pg.click('#gen0 .btn.teal');pg.wait_for_timeout(150);ok('BUYING takes the price (4 of 10 coins) and gives you one generator, and the next generator appears',abs(S(pg,"S.coins")-6)<1e-9 and S(pg,"S.gens[0].n")==1 and E("()=>document.querySelector('#gen1').style.display!=='none'") and E("()=>document.querySelector('#gen2').style.display==='none'"),[S(pg,'S.coins')])
    ok('...the 3D station gets its prop (the wallet) and the row shows x1',E("()=>HH.sc().stations[0].prop.visible")==True and 'x1' in pg.inner_text('#gen0 .rname'))
    ok('...an unmanaged generator offers "Run cycle" and "Hire Penny Pocket" (priced 1K), the hire button disabled for now',pg.inner_text('#gen0 .btn.blue')=='Run cycle' and 'Hire Penny Pocket - 1K' in pg.inner_text('#gen0 .btn.pink') and E("()=>document.querySelector('#gen0 .btn.pink').disabled"),pg.inner_text('#gen0'))
    E("()=>HH.pause(true)");c0=S(pg,"S.coins");pg.click('#gen0 .btn.blue');E("()=>HH.refresh()");running=pg.inner_text('#gen0 .btn.blue')=='Running...'
    E("()=>{HH.get().gens[0].prog=.4;HH.refresh()}");w=E("()=>parseFloat(document.querySelector('#gen0 .bar i').style.width)")
    ok('RUN CYCLE starts the one second cycle: the button says "Running..." and the bar shows how far along it is (40%% progress shows as %.0f%%)'%w,running and 39<w<41,[running,w])
    E("()=>{HH.pause(false);HH.advance(1.2)}");E("()=>HH.refresh()");pg.wait_for_timeout(100)
    ok('...when it ends it pays out 1 coin and goes back to waiting for you',abs(S(pg,"S.coins")-c0-1)<.2 and pg.inner_text('#gen0 .btn.blue')=='Run cycle',[S(pg,'S.coins')-c0])
    # buying modes
    setstate(pg,"T.coins=1e6;T.gens[0].n=1");pg.click('#tab_crew');pg.wait_for_timeout(300)
    for q,lab,n in (('x10','Buy x10',10),('x100','Buy x100',100),('Max','Buy max',None)):
        pg.click("button:has-text('%s')"%q);pg.wait_for_timeout(300)
        t=pg.inner_text('#gen0 .btn.teal');ok('BUY MODE %s: the button reads "%s ..." and shows the cost'%(q,lab),t.startswith(lab) and ' - ' in t,t)
    mb=E("()=>maxBuy(HH.get(),0)");pg.click('#gen0 .btn.teal');pg.wait_for_timeout(150);ok('Max buys exactly as many as you can afford (%d), leaving less than the next one costs'%mb,S(pg,"S.gens[0].n")==1+mb and S(pg,"S.coins")<E("()=>genCost(HH.get(),0,1)")+1e-9,[mb,S(pg,'S.gens[0].n')])
    pg.click("button:has-text('x1')")
    # hire
    setstate(pg,"T.coins=5000;T.gens[0].n=5;T.gens[1].n=2");pg.click('#tab_crew');pg.wait_for_timeout(350)
    ok('a red dot appears on the Crew tab when you can afford a manager',E("()=>document.getElementById('dot_crew').classList.contains('show')"))
    st0=grab_station(pg,0);pg.click('#gen0 .btn.pink');pg.wait_for_timeout(250);toast_ok=E("()=>/Penny Pocket joined/.test(document.getElementById('toasts').innerText)");E("()=>HH.hover(0)");pg.wait_for_timeout(250);lab_ok=E("()=>[].some.call(document.querySelectorAll('.lab'),function(l){return l.style.display!=='none'&&/Penny Pocket/.test(l.textContent)})");pg.wait_for_timeout(1300)
    ok('HIRING: Penny Pocket costs 1,000, joins you, and the button is replaced by "Penny Pocket runs this for you."',S(pg,"S.gens[0].mgr")==True and 3999<S(pg,"S.coins")<4000+E("()=>cps(HH.get(),Date.now()/1000)")*30 and 'runs this for you' in pg.inner_text('#gen0'),[S(pg,'S.coins')])
    st1=grab_station(pg,0);ok('...the character really appears in 3D at her station (the picture there changes, difference %.1f)'%diff(st0,st1),diff(st0,st1)>6)
    ok('...a toast welcomes her and a label with her name floats over her',toast_ok and lab_ok,[toast_ok,lab_ok])
    c1=S(pg,"S.coins");pg.wait_for_timeout(2300);ok('...and from now on she earns for you with no clicking (coins rose by %.1f)'%(S(pg,'S.coins')-c1),S(pg,"S.coins")>c1+1,[c1,S(pg,'S.coins')])
    ok('the income per second in the HUD matches the rules (managed generators only)',abs(E("()=>cps(HH.get(),Date.now()/1000)")-float(pg.inner_text('#ps').split(' per')[0].replace('K','e3').replace('M','e6')))<max(.05,E("()=>cps(HH.get(),Date.now()/1000)")*.02),pg.inner_text('#ps'))
    # tapping a station in 3D
    setstate(pg,"T.coins=100;T.gens[1].n=2");b=canvas_box(pg);p=stn_box(pg,1);pg.click('#tab_upgrades');pg.mouse.click(b['x']+p['x'],b['y']+p['y']);pg.wait_for_timeout(250)
    ok('TAPPING A STATION IN 3D runs its cycle when it has no manager',S(pg,"S.gens[1].run")==True)
    setstate(pg,"T.coins=100");p=stn_box(pg,5);pg.mouse.click(b['x']+p['x'],b['y']+p['y']);pg.wait_for_timeout(250);ok('...and tapping a station you do not own yet takes you to the Crew tab to buy it',pg.get_attribute('#tab_crew','aria-selected')=='true')
    # upgrades
    setstate(pg,"T.coins=1e4;T.gens[0].n=12");pg.click('#tab_upgrades');pg.wait_for_timeout(350)
    names=E("()=>[].map.call(document.querySelectorAll('#view .rname'),function(n){return n.textContent})");ok('UPGRADES: the list shows what you can buy (click upgrades, a global boost, and Paper Wallet Overclock because you own 10+)',any('Fast Fingers' in n for n in names) and any('Bull Market' in n for n in names) and any('Paper Wallet Overclock' in n for n in names) and not any('Mining Rig Overclock' in n for n in names),names)
    v0=S(pg,"clickValue(S,Date.now()/1000)");pg.click("#view .row:has-text('Fast Fingers') .btn");pg.wait_for_timeout(250)
    ok('buying Fast Fingers takes 100 coins, doubles your click, and removes it from the list',abs(S(pg,"S.coins")-9900)<1 and abs(S(pg,"clickValue(S,Date.now()/1000)")-2*v0)<.01 and 'Steel Fingers' in pg.inner_text('#view') and 'Fast Fingers' not in pg.inner_text('#view'),[S(pg,'S.coins'),v0,S(pg,"clickValue(S,Date.now()/1000)")])
    ok('...and the Mine button shows the new value',pg.inner_text('#mine')=='Mine +%s'%E("()=>fmt(clickValue(HH.get(),Date.now()/1000))"),pg.inner_text('#mine'))
    setstate(pg,"T.coins=50");pg.click('#tab_crew');pg.click('#tab_upgrades');pg.wait_for_timeout(300);ok('upgrades you cannot afford are disabled',E("()=>[].every.call(document.querySelectorAll('#view .row .btn'),function(b){return b.disabled})"))
    c.close()
    # the coin ladder
    c,pg,errs=page(br);E=pg.evaluate
    names=[];coinpix=[];bad=[]
    for k in range(40):
        E("k=>{var S=HH.get();S.runCoins=TIER_AT[k];S.cycleCoins=TIER_AT[k]}",k);pg.wait_for_timeout(180)
        n=pg.inner_text('#coinName');names.append(n)
        if n!=E("k=>COINS[k]",k):bad.append((k,n))
    ok('THE COIN LADDER: climbing through all 40 coins, the HUD names each one in order from Dust to Mintopia',not bad and names[0]=='Dust' and names[39]=='Mintopia' and len(set(names))==40,bad[:3])
    E("()=>{var S=HH.get();S.runCoins=0}");pg.wait_for_timeout(250);g1=E("()=>{var p=HH.screen(0,2.35,0);return HH.grab(p.x-50,p.y-50,100,100)}");E("()=>{HH.sc().update=function(){}}");
    E("()=>{var sc=HH.sc();sc.spinNode.rot=[0,0,0];sc.pulse=0;sc.coin.scl=[1,1,1]}");pg.wait_for_timeout(200);a=E("()=>{var p=HH.screen(0,2.35,0);return HH.grab(p.x-60,p.y-60,120,120)}")
    E("()=>{var S=HH.get();S.runCoins=TIER_AT[15]}");pg.wait_for_timeout(300);E("()=>{var sc=HH.sc();sc.spinNode.rot=[0,0,0];sc.pulse=0}");pg.wait_for_timeout(200);b2=E("()=>{var p=HH.screen(0,2.35,0);return HH.grab(p.x-60,p.y-60,120,120)}")
    ok('each coin has its own face: the picture on the coin differs between Dust and Bitcoin (difference %.1f)'%diff(a,b2),diff(a,b2)>3)
    E("()=>{var S=HH.get();S.runCoins=TIER_AT[3]*1.5}");pg.wait_for_timeout(250)
    bar0=E("()=>parseFloat(document.querySelector('#tierBar i').style.width)");E("()=>{var S=HH.get();S.runCoins=Math.sqrt(TIER_AT[3]*TIER_AT[4])}");pg.wait_for_timeout(250);bar1=E("()=>parseFloat(document.querySelector('#tierBar i').style.width)")
    ok('the progress bar fills as you approach the next coin (%.0f%% then %.0f%%) and reads about 50%% halfway on the log scale'%(bar0,bar1),bar0<bar1 and 40<bar1<60,[bar0,bar1])
    E("()=>{var S=HH.get();S.runCoins=TIER_AT[38]}");pg.wait_for_timeout(250);E("()=>{HH.get().runCoins=TIER_AT[39]}");pg.wait_for_timeout(250);ok('at the last coin the bar is full and the game says you mined every coin','mined every coin' in pg.inner_text('#tierNote') and E("()=>document.querySelector('#tierBar i').style.width")=='100%',pg.inner_text('#tierNote'))
    c.close()
    # the toast on a new coin
    c,pg,errs=page(br);E=pg.evaluate;pg.wait_for_timeout(1200)
    E("()=>{HH.get().runCoins=30}");pg.wait_for_timeout(300);ok('reaching a new coin celebrates it ("New coin unlocked: Pepe!") and adds +3% income',E("()=>/New coin unlocked: Pepe/.test(document.getElementById('toasts').innerText)") and abs(E("()=>tierMult(HH.get())")-1.03)<1e-9)
    c.close()
if __name__=='__main__':
    with sync_playwright() as p:
        br=p.chromium.launch();part2(br);br.close()
    sys.exit(summary())
