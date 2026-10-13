from harness import *
from t2 import grab_station,stn_box
def part3(br):
    c,pg,errs=page(br);E=pg.evaluate
    E("()=>HH.pause(true)")
    # ---------- prestige
    setstate(pg,"T.cycleCoins=4e10;T.runCoins=4e10;T.allCoins=4e10;T.coins=1e8;T.gens[0].n=5;T.gens[0].mgr=true;T.gens[0].run=true;T.ups.c0=1");E("()=>HH.pause(true)");pg.click('#tab_prestige');pg.wait_for_timeout(300)
    ok('PRESTIGE: the tab says how many tokens are ready (63) and the button offers them',  '63 token' in pg.inner_text('#view') and 'Prestige for +63' in pg.inner_text('#view .btn.teal'),pg.inner_text('#view')[:200])
    ok('...the Prestige tab shows a dot when tokens are waiting',E("()=>document.getElementById('dot_prestige').classList.contains('show')"))
    pg.click("#view .btn.teal:has-text('Prestige for')");pg.wait_for_timeout(200)
    ok('A CONFIRMATION appears first, explaining what resets and what is kept, with Cancel focused (so Enter cannot reset by accident)',E("()=>document.getElementById('modal').classList.contains('show')")and 'reset' in pg.inner_text('#dlg') and 'keep' in pg.inner_text('#dlg') and E("()=>document.activeElement.textContent")=='Cancel',pg.inner_text('#dlg')[:120])
    pg.keyboard.press('Tab');pg.keyboard.press('Tab');ok('...Tab stays inside the dialog (focus is trapped)',E("()=>document.getElementById('dlg').contains(document.activeElement)"))
    pg.keyboard.press('Escape');pg.wait_for_timeout(100);ok('Escape closes it and nothing is lost',not E("()=>document.getElementById('modal').classList.contains('show')") and S(pg,"S.pt")==0 and S(pg,"S.gens[0].n")==5)
    pg.click("#view .btn.teal:has-text('Prestige for')");pg.click("#dlg .btn:has-text('Prestige for')");toast_txt=pg.inner_text('#toasts');pg.wait_for_function("()=>document.getElementById('coinName').textContent==='Dust'",timeout=6000);pg.wait_for_timeout(300)
    ok('CONFIRMING gives 63 tokens and resets coins, generators and upgrades',S(pg,"S.pt")==63 and S(pg,"S.ptTotal")==63 and S(pg,"S.prestiges")==1 and S(pg,"S.coins")==0 and S(pg,"S.gens[0].n")==0 and S(pg,"Object.keys(S.ups).length")==0,[S(pg,'S.pt'),S(pg,'S.coins')])
    ok('...and a toast celebrates it, the crew leaves the stage (the character is hidden), and the coin goes back to Dust','Prestige! +63' in toast_txt and E("()=>HH.station(0).visible")==False and pg.inner_text('#coinName')=='Dust')
    ok('...and the screen says you now earn x%s from tokens'%E("()=>fmt(ptMult(HH.get()))"),'x'+E("()=>fmt(ptMult(HH.get())*rtMult(HH.get()))") in pg.inner_text('#view'),pg.inner_text('#view')[:260])
    # prestige shop
    pg.click("#view .shoprow:has-text('Golden Finger') .btn");pg.wait_for_timeout(250)
    ok('THE PRESTIGE SHOP: buying Golden Finger costs 3 tokens, shows Lv 1/10, and doubles clicks',S(pg,"S.pt")==60 and S(pg,"S.pshop.p_click")==1 and 'Lv 1/10' in pg.inner_text('#view .shoprow:has-text("Golden Finger")') and abs(E("()=>clickMult(HH.get())")-2)<1e-9,[S(pg,'S.pt')])
    setstate(pg,"T.pt=1;T.ptTotal=1");E("()=>HH.pause(true)");pg.click('#tab_crew');pg.click('#tab_prestige');pg.wait_for_timeout(300);ok('items you cannot afford are disabled, and the first free slot of tokens is respected',E("()=>[].every.call(document.querySelectorAll('#view .shoprow .btn'),function(b){return b.disabled})"))
    setstate(pg,"T.pt=20;T.ptTotal=20");E("()=>HH.pause(true)");pg.click('#tab_crew');pg.click('#tab_prestige');pg.wait_for_timeout(300);pg.click("#view .shoprow:has-text('Head Start') .btn");pg.wait_for_timeout(300)
    ok('HEAD START hires the first manager for you straight away, and the 3D character appears',S(pg,"S.gens[0].mgr")==True and S(pg,"S.gens[0].n")==1 and E("()=>HH.station(0).visible")==True)
    setstate(pg,"T.pt=1e6;T.ptTotal=1e6");E("()=>HH.pause(true)");pg.click('#tab_crew');pg.click('#tab_prestige');pg.wait_for_timeout(300)
    for _ in range(12):
        if E("()=>{var r=[].filter.call(document.querySelectorAll('#view .shoprow'),function(x){return /Golden Finger/.test(x.textContent)})[0];return !!r&&!r.querySelector('.btn').disabled}"):pg.click("#view .shoprow:has-text('Golden Finger') .btn");pg.wait_for_timeout(60)
    ok('a shop item stops at its maximum level and says "Maxed"',S(pg,"S.pshop.p_click")==10 and 'Maxed' in pg.inner_text('#view .shoprow:has-text("Golden Finger")'))
    # ---------- rebirth
    setstate(pg,"T.ptTotal=99;T.pt=99");E("()=>HH.pause(true)");pg.click('#tab_crew');pg.click('#tab_prestige');pg.wait_for_timeout(300)
    ok('REBIRTH is locked below 100 prestige tokens and says how many you have',E("()=>document.querySelector('#view .btn.pink').disabled")and 'locked' in pg.inner_text('#view') and '99 of 100' in pg.inner_text('#view'),pg.inner_text('#view')[:200])
    setstate(pg,"T.ptTotal=200;T.pt=140;T.pshop.p_click=3;T.rt=1;T.rtTotal=1;T.rshop.r_mult=1;T.gens[0].n=3;T.coinSkin.owned.neon=1;T.ach.first=1;T.cycleCoins=5e9;T.runCoins=5e9");E("()=>HH.pause(true)");pg.click('#tab_crew');pg.click('#tab_prestige');pg.wait_for_timeout(300)
    ok('with 200 tokens, rebirth is open and offers 2 rebirth tokens',not E("()=>document.querySelector('#view .btn.pink').disabled") and 'Rebirth for +2' in pg.inner_text('#view .btn.pink'),pg.inner_text('#view .btn.pink'))
    pg.click("#view .btn.pink");pg.wait_for_timeout(200);ok('the rebirth confirmation warns that prestige tokens and the prestige shop reset, and what stays forever','prestige tokens' in pg.inner_text('#dlg') and 'stay forever' in pg.inner_text('#dlg'),pg.inner_text('#dlg')[:200])
    pg.click("#dlg .btn:has-text('Rebirth for')");pg.wait_for_timeout(300)
    ok('REBORN: rebirth tokens go from 1 to 3, prestige tokens and the prestige shop reset, the rebirth shop, skins and achievements are kept',S(pg,"S.rt")==3 and S(pg,"S.rtTotal")==3 and S(pg,"S.rebirths")==1 and S(pg,"S.pt")==0 and S(pg,"Object.keys(S.pshop).length")==0 and S(pg,"S.rshop.r_mult")==1 and S(pg,"S.coinSkin.owned.neon")==1 and S(pg,"S.ach.first")==1,[S(pg,'S.rt'),S(pg,'S.pt')])
    pg.click("#view .shoprow:has-text('Rebirth Power') .btn");pg.wait_for_timeout(250)
    ok('THE REBIRTH SHOP: Rebirth Power costs 2 rebirth tokens at level 1, and adds +50% income',S(pg,"S.rt")==1 and S(pg,"S.rshop.r_mult")==2 and abs(E("()=>rtMult(HH.get())")-(1+.5*3+.5*2))<1e-9,[S(pg,'S.rt'),E("()=>rtMult(HH.get())")])
    c.close()
    # ---------- skins and the 3D look
    c,pg,errs=page(br);E=pg.evaluate;E("()=>HH.pause(true)")
    setstate(pg,"T.pt=100;T.ptTotal=100;T.rt=10;T.rtTotal=10");E("()=>HH.pause(true)");pg.click('#tab_wardrobe');pg.wait_for_timeout(300)
    ok('SKINS: the coin skins are listed, Classic Gold is worn, and the others show their price',pg.inner_text('#view .skincard.worn').startswith('Classic Gold') and 'Buy 5 tokens' in pg.inner_text('#view') and 'Buy 3 rebirth' in pg.inner_text('#view'))
    def coinpix():
        E("()=>{var sc=HH.sc();sc.update=function(){};sc.spinNode.rot=[0,0,0];sc.pulse=0;sc.coin.scl=[1,1,1]}");pg.wait_for_timeout(250);return E("()=>{var p=HH.screen(0,2.35,0);return HH.grab(p.x-45,p.y-45,90,90)}")
    gold=coinpix();gm=mean_color(gold)
    pg.click("#view .skincard:has-text('Neon Pulse') .btn");pg.wait_for_timeout(350);neon=coinpix();nm=mean_color(neon)
    ok('BUYING Neon Pulse costs 5 tokens, wears it at once, and the real 3D coin changes colour (gold %s to %s)'%([round(x) for x in gm],[round(x) for x in nm]),S(pg,"S.pt")==95 and S(pg,"S.coinSkin.active")=='neon' and math.dist(gm,nm)>40,[S(pg,'S.pt'),math.dist(gm,nm)])
    dist={}
    for sk in ('lava','pixel','galaxy','diamond'):
        pg.click("#view .skincard:has-text('%s') .btn"%{'lava':'Lava Core','pixel':'Pixel Coin','galaxy':'Galaxy','diamond':'Diamond'}[sk]);pg.wait_for_timeout(300);dist[sk]=mean_color(coinpix())
    ok('every coin skin looks different from the others (lava, pixel, galaxy, diamond, neon, gold: smallest gap %.0f)'%min(math.dist(a,b) for i,(ka,a) in enumerate(list(dist.items())+[('n',nm),('g',gm)]) for kb,b in (list(dist.items())+[('n',nm),('g',gm)])[i+1:]),all(math.dist(a,b)>15 for i,(ka,a) in enumerate(list(dist.items())+[('n',nm),('g',gm)]) for kb,b in (list(dist.items())+[('n',nm),('g',gm)])[i+1:]),{k:[round(x) for x in v] for k,v in dist.items()})
    ok('...the skin you wear is saved, and you can switch back to one you own for free',S(pg,"S.coinSkin.active")=='diamond' and (pg.click("#view .skincard:has-text('Classic Gold') .btn"),pg.wait_for_timeout(250),S(pg,"S.coinSkin.active")=='gold')[2])
    setstate(pg,"T.pt=1;T.ptTotal=1");E("()=>HH.pause(true)");pg.click('#tab_crew');pg.click('#tab_wardrobe');pg.wait_for_timeout(300);ok('a skin you cannot afford is disabled',E("()=>document.querySelector('#view .skincard:nth-child(2) .btn').disabled"))
    # character skins in 3D
    setstate(pg,"T.pt=100;T.ptTotal=100;T.rt=10;T.rtTotal=10;T.gens[0].n=3;T.gens[0].mgr=true;T.gens[0].run=true;T.gens[2].n=3;T.gens[2].mgr=true;T.gens[2].run=true");E("()=>HH.pause(true)");pg.click('#tab_crew');pg.click('#tab_wardrobe');pg.wait_for_timeout(500)
    E("()=>{var sc=HH.sc();sc.update=function(){}}");pg.wait_for_timeout(250)
    base=grab_station(pg,0);out={}
    def dark(g):
        d=g['data'];return sum(1 for k in range(0,len(d),4) if .299*d[k]+.587*d[k+1]+.114*d[k+2]<45)
    for name in ('Neon','Golden','Shadow'):
        pg.click("#view .card:has-text('Crew skins') .skincard:has-text('%s') .btn"%name);pg.wait_for_timeout(500)
        E("()=>{var sc=HH.sc();sc.update=function(){};sc.stations[0].pop=1;sc.stations[0].c.sc.scl=[sc.stations[0].c.B.scale,sc.stations[0].c.B.scale,sc.stations[0].c.B.scale]}");pg.wait_for_timeout(300);out[name]=grab_station(pg,0)
    gaps={k:diff(base,v) for k,v in out.items()}
    ok('CREW SKINS: Penny Pocket really changes in 3D with each skin bought (Neon, Golden, Shadow each differ from the original: pixel gaps %s)'%{k:round(v,1) for k,v in gaps.items()},all(v>2.5 for v in gaps.values()),gaps)
    ok('...Shadow has far more dark pixels than Golden (%d against %d)'%(dark(out['Shadow']),dark(out['Golden'])),dark(out['Shadow'])>dark(out['Golden'])+150,[dark(out['Shadow']),dark(out['Golden'])])
    ok('...and the price came out of the right tokens (Neon 10 prestige, Golden 2 and Shadow 3 rebirth)',S(pg,"S.pt")==90 and S(pg,"S.rt")==5,[S(pg,'S.pt'),S(pg,'S.rt')])
    ok('...each character keeps their own skin (Dr. Volt is still in her original)',S(pg,"S.charSkins[2].active")=='default' and S(pg,"S.charSkins[0].active")=='shadow')
    c.close()
if __name__=='__main__':
    with sync_playwright() as p:
        br=p.chromium.launch();part3(br);br.close()
    sys.exit(summary())
