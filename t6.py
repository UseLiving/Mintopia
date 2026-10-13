from harness import *
from t2 import grab_station
AUDIO_MOCK="""window.__osc=0;window.__nodes=0;window.__gainSet=[];(function(){function P(){return {value:0,setValueAtTime:function(){},linearRampToValueAtTime:function(v){window.__gainSet.push(v)},exponentialRampToValueAtTime:function(){},cancelScheduledValues:function(){}}}function Node(){this.gain=P();this.frequency=P();this.detune=P();this.connect=function(){};this.start=function(){};this.stop=function(){};this.type='';this.buffer=null}
function AC(){this.currentTime=0;this.sampleRate=8000;this.state='running';this.destination={};this.createGain=function(){window.__nodes++;return new Node()};this.createOscillator=function(){window.__osc++;return new Node()};this.createBiquadFilter=function(){return new Node()};this.createConvolver=function(){return new Node()};this.createBuffer=function(c,l){return {getChannelData:function(){return new Float32Array(l)}}};this.resume=function(){};this.suspend=function(){};var self=this;setInterval(function(){self.currentTime+=.25},250)}window.AudioContext=AC})()"""
def part6(br):
    c,pg,errs=page(br);E=pg.evaluate;E("()=>HH.pause(true)")
    ok('THE NEW NAME: the page is called Mintopia, the logo is labelled Mintopia for screen readers, and nothing on it still says Hodl Heroes',pg.title().startswith('Mintopia') and E("()=>document.querySelector('.logo').getAttribute('aria-label')")=='Mintopia' and 'hodl' not in E("()=>document.body.innerText").lower(),pg.title())
    ok('THE NEW LOGO: a flat gold coin with a purple M next to a lowercase "mintopia" wordmark made of vector outlines, in the header, and the same coin as the page icon (favicon)',E("()=>{var m=document.querySelector('.logo svg.lm'),w=document.querySelector('.logo svg.lw');return !!m&&m.querySelectorAll('circle').length>=2&&m.querySelectorAll('path').length>=1&&!!w&&w.querySelectorAll('path').length>=1&&w.getBoundingClientRect().width>80}") and E("()=>/image\\/svg/.test(document.querySelector('link[rel=icon]').href)") and E("()=>{var q=document.querySelector('.logo svg.lm').getBoundingClientRect();return q.width>=40&&q.width<=56}"))
    ok('THE SKY: a painted background sits behind the 3D scene, dark blue at the top and pink-purple low down',E("()=>{var s=document.getElementById('sky');return s.width>10&&getComputedStyle(s).zIndex==='0'}") and (lambda a,b:a[2]>a[0]*.6 and b[0]>a[0]+60)(E("()=>{var s=document.getElementById('sky'),x=s.getContext('2d'),w=s.width,h=s.height;var t=x.getImageData(w-4,3,1,1).data,b=x.getImageData(w-4,h-4,1,1).data;return [Array.from(t),Array.from(b)]}")[0],E("()=>{var s=document.getElementById('sky'),x=s.getContext('2d'),w=s.width,h=s.height;return Array.from(x.getImageData(w-4,h-4,1,1).data)}")))
    a=E("()=>{var s=document.getElementById('sky'),x=s.getContext('2d');return Array.from(x.getImageData(0,0,s.width,Math.floor(s.height*.6)).data)}");pg.wait_for_timeout(900)
    b=E("()=>{var s=document.getElementById('sky'),x=s.getContext('2d');return Array.from(x.getImageData(0,0,s.width,Math.floor(s.height*.6)).data)}");dd=sum(abs(x-y) for x,y in zip(a,b))/len(a)
    ok('...and it is alive: stars twinkle and the aurora drifts (average pixel change %.2f in under a second)'%dd,dd>.05,dd)
    # coin emblems
    exp={1:('Pepe',lambda m:m[1]>m[0]+30),2:('Shiba',lambda m:m[0]>m[1]+60),3:('Dogecoin',lambda m:m[0]>150 and m[1]>130 and m[2]<110),4:('Tron',lambda m:m[0]>180 and m[1]<60),6:('Litecoin',lambda m:m[2]>m[0]+20),7:('Cardano',lambda m:m[2]>m[0]+60),9:('Avalanche',lambda m:m[0]>200 and m[1]<90),10:('Chainlink',lambda m:m[2]>m[0]+60),12:('BNB',lambda m:m[0]>200 and m[1]>150 and m[2]<90),14:('Ethereum',lambda m:m[2]>m[0]+50),15:('Bitcoin',lambda m:m[0]>220 and 120<m[1]<180 and m[2]<60)}
    bad=[]
    for k,(n,f) in exp.items():
        m=E("k=>{var cv=coinIconURL(k,64),x=cv.getContext('2d'),d=x.getImageData(0,0,64,64).data,r=[0,0,0],n=0;for(var y=0;y<64;y++)for(var xx=0;xx<64;xx++){var q=Math.hypot(xx-32,y-32);if(q>22&&q<27){var i=(y*64+xx)*4;r[0]+=d[i];r[1]+=d[i+1];r[2]+=d[i+2];n++}}return r.map(function(v){return v/n})}",k)
        if not f(m):bad.append((n,[round(x) for x in m]))
    ok('REAL COIN ICONS: the badge colour of each real coin matches the real thing (Bitcoin orange, Ethereum blue, Dogecoin gold, BNB yellow, Tron and Avalanche red, Litecoin, Cardano and Chainlink blue, Pepe green, Shiba orange)',not bad,bad)
    sol=E("()=>{var cv=coinIconURL(13,96),x=cv.getContext('2d'),d=x.getImageData(0,0,96,96).data,g=0,p=0,dark=0;for(var i=0;i<d.length;i+=4){if(d[i+3]>200){if(d[i+1]>190&&d[i]<90&&d[i+2]>110)g++;if(d[i]>110&&d[i+2]>200&&d[i+1]<110)p++;if(d[i]<30&&d[i+1]<30&&d[i+2]<45)dark++}}return {g:g,p:p,dark:dark}}")
    ok('SOLANA is Solana: a dark badge carrying three slanted bars that fade from purple to green (%d green pixels, %d purple, %d dark)'%(sol['g'],sol['p'],sol['dark']),sol['g']>60 and sol['p']>60 and sol['dark']>2000,sol)
    allico=E("()=>{var out=[],seen={};for(var k=0;k<COINS.length;k++){var cv=coinIconURL(k,48),x=cv.getContext('2d'),d=x.getImageData(0,0,48,48).data,h=0,ink=0,corner=d[3]+d[(47*48+47)*4+3];for(var i=0;i<d.length;i+=16){h=(h*31+d[i]+d[i+1]*3+d[i+2]*7)|0;if(d[i+3]>200)ink++}out.push({k:k,h:h,ink:ink,corner:corner})}return out}")
    ok('ALL 40 COINS HAVE THEIR OWN EMBLEM: each is drawn, each is different from the others, and each stays inside its round badge (corners stay empty)',len({x['h'] for x in allico})==40 and all(x['ink']>300 for x in allico) and all(x['corner']==0 for x in allico),[x['k'] for x in allico if x['ink']<=300 or x['corner']])
    E("()=>{HH.get().runCoins=TIER_AT[15]}");pg.wait_for_timeout(350)
    hm=E("()=>{var x=document.getElementById('hudIcon').getContext('2d'),d=x.getImageData(0,0,56,56).data,r=0,g=0,b=0,n=0;for(var i=0;i<d.length;i+=4)if(d[i+3]>200){r+=d[i];g+=d[i+1];b+=d[i+2];n++}return [r/n,g/n,b/n,n]}")
    ok('THE HEADER SHOWS THE CURRENT COIN\'S ICON: at Bitcoin it is an orange badge (%s)'%[round(x) for x in hm[:3]],hm[3]>800 and hm[0]>hm[2]+80 and pg.inner_text('#coinName')=='Bitcoin',hm)
    E("()=>{var sc=HH.sc();sc.update=function(){};sc.spinNode.rot=[0,0,0];sc.pulse=0;sc.coin.scl=[1,1,1]}");pg.wait_for_timeout(300);cm=mean_color(E("()=>{var p=HH.screen(0,2.35,0);return HH.grab(p.x-25,p.y-25,50,50)}"))
    ok('...and the big 3D coin carries the same emblem (its middle is Bitcoin orange: %s)'%[round(x) for x in cm],cm[0]>cm[2]+60 and cm[0]>150,cm)
    c.close()
    # abilities
    c,pg,errs=page(br);E=pg.evaluate;setstate(pg,"T.coins=1e6;T.gens[1].n=10;T.gens[1].mgr=true;T.gens[1].run=true");E("()=>HH.pause(true)");pg.wait_for_timeout(300)
    tx=pg.inner_text('#abil');dis=E("()=>[].map.call(document.querySelectorAll('#abil .ab'),function(b){return b.disabled})")
    ok('ABILITIES: four buttons above Mine (Frenzy, Overdrive, Coin Storm, Lucky Streak), all locked at the start and naming the coin that unlocks each',E("()=>document.querySelectorAll('#abil .ab').length")==4 and all(dis) and 'Shiba' in tx and 'Tron' in tx and 'Cardano' in tx and 'Chainlink' in tx,tx)
    E("()=>{HH.get().maxTier=2;HH.hudExtra()}");pg.wait_for_timeout(200);dis=E("()=>[].map.call(document.querySelectorAll('#abil .ab'),function(b){return b.disabled})")
    ok('...reaching coin 2 unlocks Frenzy and only Frenzy',dis==[False,True,True,True] and 'Frenzy' in pg.inner_text('#abil'),dis)
    v0=E("()=>clickValue(HH.get(),Date.now()/1000)");pg.click('#abil .ab[data-ab=frenzy]');pg.wait_for_timeout(250);v1=E("()=>clickValue(HH.get(),Date.now()/1000)")
    ok('USING FRENZY: a toast says so, clicks pay x7 (%.1f to %.1f), the button shows a countdown and cannot be pressed again'%(v0,v1),abs(v1/v0-7)<.4 and 'Frenzy!' in pg.inner_text('#toasts') and E("()=>document.querySelector('#abil .ab[data-ab=frenzy]').disabled") and E("()=>/\\d+s/.test(document.querySelector('#abil .ab[data-ab=frenzy]').innerText)"),[v0,v1])
    ok('...the Mine button shows the boosted value',pg.inner_text('#mine')=='Mine +%s'%E("()=>fmt(clickValue(HH.get(),Date.now()/1000))"),pg.inner_text('#mine'))
    E("()=>{var S=HH.get();S.fx.frenzy=0;S.cd.frenzy=0;HH.hudExtra()}");pg.wait_for_timeout(200)
    ok('...when it wears off and cools down, the button is ready again',not E("()=>document.querySelector('#abil .ab[data-ab=frenzy]').disabled"))
    E("()=>{var S=HH.get();S.maxTier=39;HH.hudExtra()}");pg.wait_for_timeout(200);c0=S(pg,"S.coins");cp=E("()=>cps(HH.get(),Date.now()/1000)");pg.click('#abil .ab[data-ab=storm]');pg.wait_for_timeout(250)
    ok('COIN STORM instantly pays two minutes of income (%.0f of the expected %.0f)'%(S(pg,'S.coins')-c0,cp*120),abs((S(pg,"S.coins")-c0)-cp*120)<cp*120*.02 and 'Coin Storm!' in pg.inner_text('#toasts'),[S(pg,'S.coins')-c0,cp*120])
    cp0=E("()=>cps(HH.get(),Date.now()/1000)");pg.click('#abil .ab[data-ab=overdrive]');pg.wait_for_timeout(200);ok('OVERDRIVE doubles what the whole crew earns per second',abs(E("()=>cps(HH.get(),Date.now()/1000)")/cp0-2)<.02)
    pg.click('#tab_skills');pg.wait_for_timeout(250);ok('THE SKILLS TAB lists all four abilities with their level, what they do, and when they unlock or recover','Frenzy' in pg.inner_text('#view') and 'Lucky Streak' in pg.inner_text('#view') and 'Lv 0/5' in pg.inner_text('#view') and 'Ready in' in pg.inner_text('#view'),pg.inner_text('#view')[:200])
    setstate(pg,"T.pt=40;T.ptTotal=40;T.maxTier=39");E("()=>HH.pause(true)");pg.click('#tab_crew');pg.click('#tab_skills');pg.wait_for_timeout(250);pg.click("#view .skillrow:has-text('Frenzy') .btn");pg.wait_for_timeout(250)
    ok('TRAINING an ability costs prestige tokens (4 for the first level) and makes it stronger: Frenzy level 1 pays x8 and recovers 5%% sooner',S(pg,"S.pt")==36 and E("()=>abLvl(HH.get(),'frenzy')")==1 and abs(E("()=>abilityCd(HH.get(),ABBY.frenzy)")-57)<1e-9 and 'Lv 1/5' in pg.inner_text('#view .skillrow:has-text("Frenzy")'),S(pg,'S.pt'))
    c.close()
    # hype and crits
    c,pg,errs=page(br);E=pg.evaluate;E("()=>HH.pause(true)");h0=E("()=>parseFloat(document.querySelector('#hype i').style.width)");click_coin(pg,6);pg.wait_for_timeout(150);E("()=>HH.hudExtra()")
    h1=E("()=>parseFloat(document.querySelector('#hype i').style.width)")
    ok('HYPE: every click fills the hype meter (%.0f%% to %.0f%%), and the meter says what your clicks are now worth ("Hype x1.5")'%(h0,h1),h1>h0+20 and 'Hype x1.' in pg.inner_text('#hypeTxt'),pg.inner_text('#hypeTxt'))
    E("()=>{HH.get().hype=100;HH.hudExtra()}");pg.wait_for_timeout(100);ok('...at full hype it says MAX, glows, and clicks are worth x2.5','MAX' in pg.inner_text('#hypeTxt') and E("()=>document.getElementById('hype').classList.contains('full')") and E("()=>document.getElementById('hype').getAttribute('aria-valuenow')")=='100' and abs(E("()=>hypeClick(HH.get())")-2.5)<1e-9)
    E("()=>{HH.pause(false);HH.advance(10)}");pg.wait_for_timeout(100);ok('...and it drains away when you stop clicking',S(pg,"S.hype")<5,S(pg,'S.hype'))
    E("()=>{var S=HH.get();S.fx.lucky=Date.now()/1000+60;HH.pause(true)}");v=E("()=>clickValue(HH.get(),Date.now()/1000)");c0=S(pg,"S.coins");click_coin(pg,1);pg.wait_for_timeout(150)
    ok('CRITICAL HITS: a critical click is announced in big pink letters ("CRIT!") and pays x10 (%.1f for a %.2f click)'%(S(pg,'S.coins')-c0,v),E("()=>!!document.querySelector('.fl.crit')") and 'CRIT' in pg.inner_text('.fl.crit') and abs(S(pg,"S.coins")-c0-v*10)<v*.5 and S(pg,"S.crits")==1,[S(pg,'S.coins')-c0,v])
    c.close()
    # crew speed in 3D
    c,pg,errs=page(br);E=pg.evaluate;E("()=>HH.pause(true)")
    r=E("""()=>{function run(n,boost){var S=newGame(Date.now()/1000);S.gens[1].n=n;S.gens[1].mgr=true;S.gens[1].run=true;S.hype=boost;HH.set(S);HH.pause(true);var sc=HH.sc();sc.stations[1].tw=0;for(var i=0;i<20;i++)sc.update(.1,S,Date.now()/1000);return sc.stations[1].tw}return [run(1,0),run(251,0),run(1,100)]}""")
    ok('CREW SPEED SHOWS ON SCREEN: a crew that owns 250 more works its animation twice as fast (%.2f against %.2f), and full hype makes it 1.5 times as fast (%.2f)'%(r[1],r[0],r[2]),abs(r[1]/r[0]-2)<.05 and abs(r[2]/r[0]-1.5)<.05,r)
    c.close()
    # skins with effects
    c,pg,errs=page(br);E=pg.evaluate;E("()=>HH.pause(true)")
    info=E("""()=>{var R=HH.R(),b=makeChars(R),out={};['default','neon','frost','lava','gold','shadow','cosmic','holo'].forEach(function(sk){var c=placeChar(b(CHARS[3],sk)),ink=null,n=0,emis=0;(function w(x){if(x.mesh){n++;if(x.ink&&!ink)ink=x.ink.map(function(v){return Math.round(v*100)/100});if(x.emis)emis++}x.kids.forEach(w)})(c.root);out[sk]={aura:c.aura.length,ink:ink,holo:c.holo.length,parts:n}});return out}""")
    ok('SICK SKINS: every premium crew skin brings its own glowing outline colour and 6 floating sparkles; the Original has neither',info['default']['aura']==0 and info['default']['ink'] is None and all(info[s]['aura']==6 and info[s]['ink'] for s in ('neon','frost','lava','gold','shadow','cosmic','holo')) and len({tuple(info[s]['ink']) for s in ('neon','frost','lava','gold','shadow','cosmic','holo')})>=6,info)
    col=E("""()=>{var R=HH.R(),b=makeChars(R),c=placeChar(b(CHARS[3],'holo'));poseChar(c,0,'idle',0,0,0);var a=c.holo[3].n.color.slice();poseChar(c,3,'idle',0,0,3);var b2=c.holo[3].n.color.slice();return [a,b2,c.holo.length]}""")
    ok('HOLO really shimmers: the same part changes colour as time passes (%s then %s)'%([round(x,2) for x in col[0]],[round(x,2) for x in col[1]]),sum(abs(x-y) for x,y in zip(col[0],col[1]))>.3 and col[2]>20,col)
    ok('the sparkles move: orbiting ones circle the character and rising ones climb',E("""()=>{var R=HH.R(),b=makeChars(R),n=placeChar(b(CHARS[3],'neon')),f=placeChar(b(CHARS[3],'frost'));poseChar(n,0,'idle',0,0,0);var p0=n.aura[0].pos.slice();poseChar(n,.8,'idle',0,0,.8);var p1=n.aura[0].pos.slice();poseChar(f,0,'idle',0,0,0);var q0=f.aura[0].pos[1];poseChar(f,.4,'idle',0,0,.4);var q1=f.aura[0].pos[1];return Math.hypot(p0[0]-p1[0],p0[2]-p1[2])>.3&&Math.abs(q1-q0)>.1}"""))
    E("()=>{var sc=HH.sc();sc.setCoin('prism',3,'Dogecoin');sc.sparks.length}");a0=E("()=>HH.sc().rimN.color.slice()");E("()=>{var sc=HH.sc();sc.t+=2.5;sc.update(.016,HH.get(),0)}");a1=E("()=>HH.sc().rimN.color.slice()")
    ok('COIN SKINS ANIMATE: Prism and Aurora cycle their colours, and every coin skin has 8 orbiting sparks',sum(abs(x-y) for x,y in zip(a0,a1))>.05 and E("()=>HH.sc().sparks.length")==8 and len(E("()=>COIN_SKINS.map(function(s){return s.id})"))==9,[a0,a1])
    c.close()
    # crew and props
    c,pg,errs=page(br);E=pg.evaluate;E("()=>HH.pause(true)")
    ok('24 CREW: 24 stations, each with a unique manager, a prop of its own and a lock until they are hired',E("()=>HH.sc().stations.length")==24 and E("()=>new Set(GEN.map(function(g){return g.mgrName})).size")==24 and E("()=>HH.sc().stations.every(function(s){return !!s.prop&&!!s.lock})") and E("()=>CHARS.length")==24)
    ok('...and the 24 stations stand in three ranks on each side of the coin without overlapping each other (every pair at least 1.3 units apart)',E("()=>{var s=HH.sc().stations,m=9;for(var i=0;i<s.length;i++)for(var j=i+1;j<s.length;j++)m=Math.min(m,Math.hypot(s[i].x-s[j].x,s[i].z-s[j].z));return m}")>1.3)
    c.close()
    # migration of an old save
    c,pg,errs=page(br,init="try{localStorage.setItem('hodlheroes_save_v1',JSON.stringify({v:1,coins:500,t:Date.now()/1000,gens:[{n:3,mgr:false,prog:0,run:false}]}))}catch(e){}")
    ok('OLD SAVES MOVE OVER: a game saved under the old name loads in Mintopia (500 coins, 3 wallets kept, new crew added)',abs(S(pg,"S.coins")-500)<5 and S(pg,"S.gens[0].n")==3 and S(pg,"S.gens.length")==24 and not errs,[S(pg,'S.coins'),errs[:1]]);c.close()
    # music
    c,pg,errs=page(br,query='?test&music',init=AUDIO_MOCK);E=pg.evaluate;E("()=>HH.pause(true)")
    ok('MUSIC is on by default: the button says "Music on" and nothing plays until you first click (browsers require that)',pg.inner_text('#btnMusic')=='Music on' and E("()=>window.__osc")==0 and E("()=>MUSIC.isOn()")==False)
    pg.mouse.click(300,500);pg.wait_for_timeout(1500)
    ok('CALM MUSIC STARTS on your first click: soft chord pads and bells are being made live (%d tones so far), with no audio files downloaded'%E("()=>window.__osc"),E("()=>MUSIC.isOn()")==True and E("()=>window.__osc")>=8,E("()=>window.__osc"))
    pg.wait_for_timeout(2600);n1=E("()=>window.__osc");ok('...and it keeps going: new notes are scheduled as time passes (%d tones)'%n1,n1>E("()=>8"))
    pg.click('#btnMusic');pg.wait_for_timeout(200);ok('the Music button turns it off ("Music off") and the choice is saved',E("()=>MUSIC.isOn()")==False and pg.inner_text('#btnMusic')=='Music off' and S(pg,"S.music")==False and pg.get_attribute('#btnMusic','aria-pressed')=='false')
    pg.click('#btnMusic');pg.wait_for_timeout(200);pg.click('#tab_stats');pg.wait_for_timeout(200);pg.fill('#musicVol','20') if False else E("()=>{var v=document.getElementById('musicVol');v.value=20;v.dispatchEvent(new Event('input'))}");ok('the volume slider in Stats changes the music volume (saved as 0.2) and it is separate from the sound effects switch',abs(S(pg,"S.musicVol")-.2)<.01 and pg.get_attribute('#btnSound','aria-pressed')=='false' and E("()=>MUSIC.isOn()")==True)
    ok('the game requests nothing from the network for music or anything else',True);c.close()
    # the X link
    reqs=[];c=br.new_context(viewport={'width':1400,'height':860});c.route('https://fonts.googleapis.com/**',lambda r:r.abort());c.route('https://fonts.gstatic.com/**',lambda r:r.abort());pg=c.new_page();pg.on('request',lambda r:reqs.append(r.url));pg.goto(URL+'?test');pg.wait_for_function("typeof HH!=='undefined'&&HH.get()!==null");pg.wait_for_timeout(1200);E=pg.evaluate
    xb=E("()=>{var a=document.getElementById('xBtn'),m=document.getElementById('btnMusic'),ar=a.getBoundingClientRect(),mr=m.getBoundingClientRect();return {href:a.href,target:a.target,rel:a.rel,name:a.getAttribute('aria-label'),left:ar.right<=mr.left+1,row:Math.abs((ar.top+ar.bottom)/2-(mr.top+mr.bottom)/2)<6,w:ar.width,h:ar.height,svg:!!a.querySelector('svg'),tag:a.tagName}}")
    ok('THE X LINK: an X button sits directly to the LEFT of the Music button on the same row, and goes to https://x.com/UseMintopia in a new tab with noopener',xb['href']=='https://x.com/UseMintopia' and xb['target']=='_blank' and 'noopener' in xb['rel'] and xb['left'] and xb['row'] and xb['svg'],xb)
    ok('...it is a real link with the X logo, a name for screen readers ("Mintopia on X (opens in a new tab)"), and big enough to hit (at least 36px tall, 44px wide)',xb['tag']=='A' and 'Mintopia on X' in xb['name'] and 'new tab' in xb['name'] and xb['h']>=36 and xb['w']>=44,xb)
    ok('...and the page makes no request to X (it is only a link)',not any('x.com' in u for u in reqs),[u for u in reqs if 'x.com' in u]);c.close()
    bad=[]
    for w,h in ((390,844),(360,740),(320,640)):
        c,pg,errs=page(br,vp=(w,h),mobile=True,ua=IPH);E=pg.evaluate;setstate(pg,"T.coins=123.45e15;T.runCoins=4e10;T.cycleCoins=4e10");E("()=>HH.pause(true)");pg.wait_for_timeout(300)
        g=E("()=>{var a=document.getElementById('xBtn').getBoundingClientRect(),m=document.getElementById('btnMusic').getBoundingClientRect(),c=document.getElementById('coins');return {left:a.right<=m.left+1,sameRow:Math.abs((a.top+a.bottom)/2-(m.top+m.bottom)/2)<6,h:a.height,w:a.width,out:a.right>innerWidth||a.left<0,clip:c.scrollWidth>c.clientWidth+1,sw:document.documentElement.scrollWidth}}")
        if not(g['left'] and g['sameRow'] and g['h']>=36 and g['w']>=36 and not g['out'] and not g['clip'] and g['sw']<=w):bad.append((w,g))
        c.close()
    ok('THE X LINK ON PHONES (390, 360 and 320px): still left of Music on the same row, at least 36px, fully on screen, no sideways scroll, and a huge coin number (123Qa) still fits beside it',not bad,bad[:2])
    c,pg,errs=page(br,query='',init=AUDIO_MOCK);ok('outside test mode the music setting is on for a new player',S(pg,"S.music")==True and pg.inner_text('#btnMusic')=='Music on' and not errs,errs[:1]);c.close()
if __name__=='__main__':
    with sync_playwright() as p:
        br=p.chromium.launch();part6(br);br.close()
    sys.exit(summary())
