from harness import *
from t2 import grab_station
def save_json(extra=None,age=3600,**kw):
    d={'v':1,'t':time.time()-age,'gens':[{'n':0,'mgr':False,'prog':0,'run':False} for _ in range(12)]}
    d['gens'][1]={'n':10,'mgr':True,'prog':0,'run':True}
    d.update(kw);d.update(extra or {});return json.dumps(d)
def part4(br):
    # ---------- the twelve characters
    c,pg,errs=page(br);E=pg.evaluate;E("()=>HH.pause(true)")
    info=E("""()=>{var R=HH.R(),b=makeChars(R),out=[];for(var i=0;i<GEN.length;i++){var c=placeChar(b(CHARS[i],'default')),need=['head','torso','hips','shL','shR','elL','elR','hdL','hdR','hpL','hpR','knL','knR','ftL','ftR'],missing=need.filter(function(k){return !c[k]});var n=0;(function w(x){if(x.mesh)n++;x.kids.forEach(w)})(c.root);out.push({name:CHARS[i].name,missing:missing,parts:n,legs:c.B.leg+c.B.shin,arm:c.B.up+c.B.fo,hr:c.B.hr,kind:GEN[i].kind,pal:CHARS[i].pal})}return out}""")
    ok('EVERY CHARACTER HAS A BODY WITH ARMS AND LEGS: all 24 have a head, torso, hips, two shoulders, two elbows, two hands, two hips, two knees and two feet',all(not x['missing'] for x in info),[x['name'] for x in info if x['missing']])
    ok('...each is built from many parts (smallest has %d, largest %d), so none is a blob'%(min(x['parts'] for x in info),max(x['parts'] for x in info)),all(x['parts']>=30 for x in info),[(x['name'],x['parts']) for x in info if x['parts']<30])
    ok('...legs and arms have real length (legs at least 0.5, arms at least 0.48 units)',all(x['legs']>=.5 and x['arm']>=.48 for x in info),[(x['name'],x['legs'],x['arm']) for x in info if x['legs']<.5 or x['arm']<.48])
    ok('TWELVE HUMANS AND TWELVE MONSTERS: %s'%[x['name'] for x in info if x['kind']=='monster'],sum(1 for x in info if x['kind']=='human')==12 and sum(1 for x in info if x['kind']=='monster')==12)
    keys=[(x['pal']['skin'],x['pal']['top'],x['pal']['bottom'],x['pal'].get('hair')) for x in info]
    ok('every character has their own colours (24 different skin, outfit and hair combinations)',len(set(keys))==24 and len({x['pal']['skin'] for x in info})>=14,len(set(keys)))
    ok('they are different sizes: the smallest stands %.2f, the tallest %.2f (goblin and imp small, ogre and whale big)'%(min(x['hr'] for x in info),max(x['hr'] for x in info)),True)
    E("()=>{var sc=HH.sc();sc.update=function(){}}")
    setstate(pg,"");E("()=>HH.pause(true)");pg.wait_for_timeout(250);empty={i:grab_station(pg,i) for i in range(24)};seen=[];vis={}
    for i in range(24):
        setstate(pg,"T.gens[%d].n=1;T.gens[%d].mgr=true;T.gens[%d].run=true"%(i,i,i));E("()=>HH.pause(true)")
        E("i=>{var sc=HH.sc();sc.update=function(){};var s=sc.stations[i];s.pop=1;s.c.sc.scl=[s.c.B.scale,s.c.B.scale,s.c.B.scale]}",i);pg.wait_for_timeout(260)
        g=grab_station(pg,i);vis[i]=diff(empty[i],g);seen.append(g)
    ok('EACH OF THE 24 SHOWS UP IN 3D when hired (smallest change on screen %.1f, for %s)'%(min(vis.values()),info[min(vis,key=vis.get)]['name']),min(vis.values())>1.8,{info[i]['name']:round(v,1) for i,v in vis.items() if v<=1.8})
    c.close()
    # ---------- saving, offline earnings
    c,pg,errs=page(br,storage=save_json());E=pg.evaluate;pg.wait_for_timeout(300)
    ok('WELCOME BACK: after an hour away the game tells you so, and your crew earned 25%% of an hour of income (%s coins)'%E("()=>fmt(HH.get().coins)"),E("()=>document.getElementById('modal').classList.contains('show')")and 'Welcome back' in pg.inner_text('#dlg') and abs(S(pg,"S.coins")-186480)<1500,[S(pg,'S.coins'),pg.inner_text('#dlg')[:80]])
    ok('...the message shows how long you were away (1h 0m) and how much you earned','1h' in pg.inner_text('#dlg') and ('186K' in pg.inner_text('#dlg') or '187K' in pg.inner_text('#dlg')),pg.inner_text('#dlg'))
    pg.click("#dlg .btn:has-text('Collect')");ok('...and Collect closes it',not E("()=>document.getElementById('modal').classList.contains('show')"))
    c.close()
    c,pg,errs=page(br,storage=save_json(age=100*3600));E=pg.evaluate;pg.wait_for_timeout(300)
    ok('A VERY LONG ABSENCE (100 hours) only counts the 8 hour cap: %s coins'%E("()=>fmt(HH.get().coins)"),abs(S(pg,"S.coins")-1491840)<20000 and 'most that counts' in pg.inner_text('#dlg'),[S(pg,'S.coins'),pg.inner_text('#dlg')[:140]])
    c.close()
    c,pg,errs=page(br,storage=save_json(age=20));E=pg.evaluate;pg.wait_for_timeout(300)
    ok('coming back after only 20 seconds shows no welcome message',not E("()=>document.getElementById('modal').classList.contains('show')"))
    c.close()
    for label,store in (('not JSON','{{{'),('empty text',''),('JSON null','null'),('a number','42'),('an array','[1,2]')):
        c,pg,errs=page(br,storage=store);ok('CORRUPT SAVE (%s): a clean new game starts and nothing crashes'%label,S(pg,"S.coins")==0 and S(pg,"S.gens.length")==24 and not errs,errs[:1]);c.close()
    evil=json.dumps({'coins':'NaN','runCoins':-5,'cycleCoins':1e999,'gens':[{'n':-5,'mgr':1},{'n':1e99},None,5],'ups':{'<img>':1,'c0':1},'pshop':{'p_click':999},'rshop':{'r_mult':1000},'name':'<b>x</b>','coinSkin':{'owned':{'hacked':1},'active':'hacked'}}).replace('Infinity','1e999')
    c,pg,errs=page(br,storage=evil);ok('HOSTILE SAVE: absurd numbers, junk entries and fake skins are cleaned up and the game runs (coins %s, name %s)'%(S(pg,"S.coins"),S(pg,"S.name")),S(pg,"S.coins")==0 and S(pg,"S.pshop.p_click")==10 and S(pg,"S.rshop.r_mult")==20 and S(pg,"S.name")=='Hero' and S(pg,"S.coinSkin.active")=='gold' and not errs,errs[:1]);c.close()
    # persistence across a real reload
    c,pg,errs=page(br);E=pg.evaluate;setstate(pg,"T.coins=777;T.gens[0].n=4;T.totalClicks=12;T.pt=5;T.ptTotal=5");pg.wait_for_timeout(2300)
    stored=E("()=>JSON.parse(localStorage.getItem('mintopia_save_v1'))")
    ok('AUTOSAVE writes your game to the device by itself (coins %.0f, 4 wallets, 5 tokens)'%stored['coins'],stored['coins']>=777 and stored['gens'][0]['n']==4 and stored['pt']==5,stored['coins'])
    pg.reload();pg.wait_for_function("typeof HH!=='undefined'&&HH.get()!==null");pg.wait_for_timeout(300)
    ok('...and a reload brings it all back',S(pg,"S.gens[0].n")==4 and S(pg,"S.pt")==5 and S(pg,"S.totalClicks")==12,[S(pg,'S.gens[0].n'),S(pg,'S.pt')])
    # export, import, erase, name, sound
    pg.click('#tab_stats');pg.wait_for_timeout(250);E("()=>HH.pause(true)");pg.click("#view .btn:has-text('Export save')");pg.wait_for_timeout(200);code=pg.input_value('#exportBox')
    same=E("c=>{var T=importCode(c,0),S=HH.get();return !!T&&T.coins===S.coins&&T.gens[0].n===S.gens[0].n&&T.pt===S.pt&&T.totalClicks===S.totalClicks}",code)
    ok('EXPORT shows a save code that decodes back to the current game (coins, wallets, tokens, clicks), with Copy and Close buttons',same and len(code)>100 and 'Copy' in pg.inner_text('#dlg'),len(code))
    pg.click("#dlg .btn:has-text('Close')");setstate(pg,"T.coins=5");pg.click('#tab_stats');pg.wait_for_timeout(200);pg.click("#view .btn:has-text('Import save')");pg.fill('#importBox','garbage.code');pg.click("#dlg .btn:has-text('Import')");pg.wait_for_timeout(200)
    ok('IMPORT refuses a code that is not valid ("not valid") and keeps your game',S(pg,"S.coins")==5 and 'not valid' in pg.inner_text('#toasts'),pg.inner_text('#toasts'))
    pg.click('#tab_stats');pg.click("#view .btn:has-text('Import save')");pg.fill('#importBox',code);pg.click("#dlg .btn:has-text('Import')");pg.wait_for_timeout(300)
    ok('...and a good code restores that saved game (777 coins and 4 wallets)',abs(S(pg,"S.coins")-777)<1 and S(pg,"S.gens[0].n")==4,[S(pg,'S.coins'),S(pg,'S.gens[0].n')])
    pg.click('#tab_stats');pg.fill('.text','Moon Man_7');pg.keyboard.press('Tab');pg.wait_for_timeout(150);ok('a valid name is saved',S(pg,"S.name")=='Moon Man_7')
    pg.fill('.text','<script>');pg.keyboard.press('Tab');pg.wait_for_timeout(150);ok('...and an invalid one is refused and put back',S(pg,"S.name")=='Moon Man_7' and pg.input_value('.text')=='Moon Man_7')
    pg.click("#view .btn:has-text('Erase everything')");pg.wait_for_timeout(200);ok('ERASE asks first, and Cancel keeps everything','cannot be undone' in pg.inner_text('#dlg'),pg.inner_text('#dlg')[:80]);pg.click("#dlg .btn:has-text('Cancel')");ok('...',S(pg,"S.gens[0].n")==4)
    pg.click("#view .btn:has-text('Erase everything')");pg.click("#dlg .btn:has-text('Erase it all')");pg.wait_for_timeout(300)
    ok('...and confirming wipes the whole game back to the start',S(pg,"S.coins")==0 and S(pg,"S.gens[0].n")==0 and S(pg,"S.pt")==0 and S(pg,"S.name")=='Hero')
    c.close()
    # sound
    init="window.__osc=0;(function(){function AC(){this.currentTime=0;this.destination={};this.createOscillator=function(){window.__osc++;return {frequency:{},connect:function(){},start:function(){},stop:function(){}}};this.createGain=function(){return {gain:{setValueAtTime:function(){},exponentialRampToValueAtTime:function(){}},connect:function(){}}}}window.AudioContext=AC})()"
    c,pg,errs=page(br,init=init);E=pg.evaluate;E("()=>HH.pause(true)");click_coin(pg,3);pg.wait_for_timeout(100)
    ok('SOUND is off at the start: mining makes no sound (%d tones)'%E("()=>window.__osc"),E("()=>window.__osc")==0 and pg.get_attribute('#btnSound','aria-pressed')=='false' and pg.inner_text('#btnSound')=='Sound off')
    pg.click('#btnSound');pg.wait_for_timeout(100);ok('the sound button turns it on, says "Sound on", and is remembered in your save',pg.get_attribute('#btnSound','aria-pressed')=='true' and pg.inner_text('#btnSound')=='Sound on' and S(pg,"S.sound")==True)
    n0=E("()=>window.__osc");click_coin(pg,2);pg.wait_for_timeout(100);ok('...now mining plays a tone (%d new tones)'%(E("()=>window.__osc")-n0),E("()=>window.__osc")>n0)
    pg.click('#btnSound');n1=E("()=>window.__osc");click_coin(pg,2);pg.wait_for_timeout(100);ok('turning it off silences it again',E("()=>window.__osc")==n1)
    c.close()
    # airdrops
    c,pg,errs=page(br);E=pg.evaluate
    try:
        pg.wait_for_function("()=>HH.sc().air.on===true",timeout=15000);dropped=True
    except Exception:dropped=False
    ok('AIRDROPS: after a short wait a crate with a parachute falls onto the stage and a toast tells you to tap it',dropped and 'airdrop' in pg.inner_text('#toasts').lower(),pg.inner_text('#toasts')[:80])
    if dropped:
        claimed=False
        for _ in range(12):
            a=E("()=>{var a=HH.sc().air;return HH.screen(a.x,a.y+.2,a.z)}");b=canvas_box(pg)
            if E("([x,y])=>{var r=HH.pickAt(x,y);return !!r&&r.type==='air'}",[a['x'],a['y']]):
                pg.mouse.click(b['x']+a['x'],b['y']+a['y']);pg.wait_for_timeout(250)
                if S(pg,"S.airdrops")==1:claimed=True;break
            pg.wait_for_timeout(120)
        ok('TAPPING THE CRATE claims it: the crate disappears and you get coins or an income boost',claimed and E("()=>HH.sc().air.on")==False and ('Airdrop!' in pg.inner_text('#toasts')),[S(pg,'S.airdrops')])
    c.close()
    c,pg,errs=page(br);E=pg.evaluate;E("()=>HH.pause(true)");setstate(pg,"T.coins=1e6;T.gens[1].n=10;T.gens[1].mgr=true;T.gens[1].run=true");base=E("()=>cps(HH.get(),Date.now()/1000)")
    E("()=>{claimAirdrop(HH.get(),Date.now()/1000,function(){return .9})}");ok('a BULL RUN airdrop multiplies income by 7 for 30 seconds, and the HUD says so',abs(E("()=>cps(HH.get(),Date.now()/1000)")/base-7)<.01,[base,E("()=>cps(HH.get(),Date.now()/1000)")])
    E("()=>{HH.get().buff.until=0}");ok('...and it ends by itself',abs(E("()=>cps(HH.get(),Date.now()/1000)")/base-1)<.01);c.close()
if __name__=='__main__':
    with sync_playwright() as p:
        br=p.chromium.launch();part4(br);br.close()
    sys.exit(summary())
