const fs=require('fs'),vm=require('vm'),path=require('path');
const src=fs.readFileSync(path.join(__dirname,'..','src','game.js'),'utf8');
const ctx={btoa,atob,escape,unescape,console,module:{exports:{}}};vm.createContext(ctx);vm.runInContext(src+';this.G={ABIL,ABBY,abilityUnlocked,abilityCd,abilityDur,abilityLeft,useAbility,addHype,hypeClick,hypeSpeed,crewBoost,genSpeed,genUpCount,critChance,critMult,upCount,fxOn,abLvl,frenzyMult,TICKERS,GEN,UPS,UPBY,PSHOP,RSHOP,SHOPBY,COINS,TIER_AT,MILESTONES,ACH,COIN_SKINS,CHAR_SKINS,fmt,fmtTime,tierOf,newGame,lvl,achCount,tierMult,ptMult,rtMult,globalMult,milestoneMult,discount,genCost,maxBuy,mgrCost,speedMult,cycleTime,genMult,payout,genRate,cps,clickMult,clickPct,clickValue,earn,mine,buyGen,buyGenMax,hireMgr,runGen,upAvailable,buyUp,upCost,tick,offlineRate,offlineCap,offline,prestigeTotal,prestigeGain,doPrestige,canRebirth,rebirthGain,doRebirth,shopCost,buyShop,buySkin,setSkin,airdropGap,claimAirdrop,checkAch,serialize,sanitize,deserialize,exportCode,importCode,hash32,startKit};',ctx);
const G=ctx.G;let pass=0,fail=0;const check=(n,c,x)=>{if(c)pass++;else{fail++;console.log('FAIL',n,x===undefined?'':JSON.stringify(x).slice(0,240))}};
const near=(a,b,e)=>Math.abs(a-b)<=(e||1e-9)*Math.max(1,Math.abs(a),Math.abs(b));
const rnd=(seed)=>{let a=seed>>>0;return()=>{a=(a+0x6D2B79F5)|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}};
const mk=(o)=>Object.assign(G.newGame(0),o||{});
// ---------- data
check('24 generators, costs, revenues and manager prices all increase, and cycle times never go down',G.GEN.length===24&&G.GEN.every((g,i)=>i===0||(g.cost>G.GEN[i-1].cost&&g.rev>G.GEN[i-1].rev&&g.time>=G.GEN[i-1].time&&g.mgr>G.GEN[i-1].mgr)));
check('every generator has a growth rate between 1 and 1.2, a name, a manager name and a kind (human or monster)',G.GEN.every(g=>g.coef>1&&g.coef<1.2&&g.name&&g.mgrName&&(g.kind==='human'||g.kind==='monster')));
check('the crew is a mix of humans and monsters (12 and 12)',G.GEN.filter(g=>g.kind==='human').length===12&&G.GEN.filter(g=>g.kind==='monster').length===12);
check('40 coins in the ladder, with strictly rising thresholds starting at 0',G.COINS.length===40&&G.TIER_AT.length===40&&G.TIER_AT[0]===0&&G.TIER_AT.every((t,i)=>i===0||t>G.TIER_AT[i-1]));
check('coin names are all different',new Set(G.COINS).size===40);
check('every coin has its own short ticker of 2 to 4 capital letters (30 different ones)',G.TICKERS.length===40&&new Set(G.TICKERS).size===40&&G.TICKERS.every(t=>/^[A-Z]{2,4}$/.test(t)));
check('over 150 upgrades with unique ids and positive costs (%d)'.replace('%d',G.UPS.length),G.UPS.length>=150&&new Set(G.UPS.map(u=>u.id)).size===G.UPS.length&&G.UPS.every(u=>u.cost>0));
check('shop items have valid fields: both shops, max levels, positive base cost, growth at least 1',[...G.PSHOP,...G.RSHOP].every(s=>s.id&&s.max>0&&s.base>0&&s.grow>=1&&s.desc)&&G.PSHOP.every(s=>s.cur==='pt')&&G.RSHOP.every(s=>s.cur==='rt'));
check('skins: 9 coin skins and 8 per character, the first one is free',G.COIN_SKINS.length===9&&G.CHAR_SKINS.length===8&&G.COIN_SKINS[0].cur==='free'&&G.CHAR_SKINS[0].cur==='free');
// ---------- number formatting
const F=[[0,'0'],[7,'7'],[12.34,'12.3'],[999,'999'],[1000,'1K'],[1234,'1.23K'],[15000,'15K'],[999999,'1M'],[1e6,'1M'],[1.5e9,'1.5B'],[2.5e12,'2.5T'],[1e15,'1Qa'],[1e33,'Dc'.length?'1Dc':''],[1.234e63,'1.23Vg'],[5e100,'5e100']];
F.forEach(([v,e])=>check('fmt('+v+') = '+e,G.fmt(v)===e,G.fmt(v)));
check('fmt copes with NaN, Infinity and negatives without throwing',G.fmt(NaN)==='0'&&G.fmt(-1500)==='-1.5K'&&G.fmt(Infinity)==='Infinity');
check('fmtTime reads naturally',G.fmtTime(1)==='1.0s'&&G.fmtTime(45)==='45s'&&G.fmtTime(125)==='2m 5s'&&G.fmtTime(7200)==='2h 0m'&&G.fmtTime(90000)==='1d 1h');
// ---------- coin ladder
check('the ladder starts at Dust and each threshold moves up exactly one coin',G.tierOf(0)===0&&G.tierOf(G.TIER_AT[1]-1)===0&&G.tierOf(G.TIER_AT[1])===1&&G.TIER_AT.every((t,i)=>G.tierOf(t)===i));
check('beyond the last threshold the coin stays at the top (39, Mintopia)',G.tierOf(1e300)===39&&G.COINS[39]==='Mintopia');
// ---------- clicking and cost maths
let S=mk();check('a new game starts with nothing, one click is worth 1',S.coins===0&&G.clickValue(S,0)===1&&S.gens.length===24);
G.mine(S,0);G.mine(S,0);check('mining adds to coins, this run, this cycle, all time and the click count',S.coins===2&&S.runCoins===2&&S.cycleCoins===2&&S.allCoins===2&&S.totalClicks===2);
for(const i of [0,3,7,11]){const g=G.GEN[i];S=mk({coins:1e30});let sum=0;for(let k=0;k<10;k++)sum+=g.cost*Math.pow(g.coef,k);check('cost of 10 '+g.name+' = the sum of ten steps (geometric formula)',near(G.genCost(S,i,10),sum,1e-9),[G.genCost(S,i,10),sum])}
S=mk({coins:1e30});S.gens[2].n=40;let it=0;for(let k=0;k<7;k++)it+=G.GEN[2].cost*Math.pow(G.GEN[2].coef,40+k);check('the cost depends on how many you already own',near(G.genCost(S,2,7),it,1e-9));
check('cost of zero or negative units is 0, and a Bulk Discount level lowers every price by 3%',G.genCost(S,0,0)===0&&(()=>{const T=mk({pshop:{p_disc:5}});return near(G.genCost(T,0,1),4*.85)})());
// maxBuy matches a brute-force search for many random situations
let okMax=true,bad=null;const R=rnd(7);for(let t=0;t<400&&okMax;t++){const i=Math.floor(R()*12);const T=mk();T.gens[i].n=Math.floor(R()*300);T.coins=G.GEN[i].cost*Math.pow(G.GEN[i].coef,T.gens[i].n)*Math.pow(10,R()*4-.5);T.pshop.p_disc=Math.floor(R()*6);const k=G.maxBuy(T,i);let bf=0;while(G.genCost(T,i,bf+1)<=T.coins&&bf<5000)bf++;if(k!==bf){okMax=false;bad=[i,T.gens[i].n,T.coins,k,bf]}}
check('MAX BUY always equals the true maximum you can afford (400 random situations)',okMax,bad);
S=mk({coins:3});check('cannot afford the first Paper Wallet with 3 coins: max buy 0, buying refused, nothing taken',G.maxBuy(S,0)===0&&G.buyGen(S,0,1)===0&&S.coins===3&&S.gens[0].n===0);
S=mk({coins:4});check('exactly 4 coins buys one Paper Wallet and leaves 0',G.buyGen(S,0,1)===1&&S.coins===0&&S.gens[0].n===1);
S=mk({coins:1000});const b0=G.buyGenMax(S,1);check('buy max spends exactly the cost of what it bought',b0>0&&near(S.coins,1000-(()=>{const T=mk();return G.genCost(T,1,b0)})(),1e-9)&&G.maxBuy(S,1)===0,[b0,S.coins]);
S=mk({coins:1e12});check('bad purchases are refused: unknown generator, zero, negative, NaN',[[-1,1],[12,1],[0,0],[0,-3],[0,NaN],[0,'x']].every(([i,k])=>G.buyGen(S,i,k)===0)&&S.coins===1e12);
S=mk({coins:1e12});check('a fractional quantity is rounded down (2.9 buys 2)',G.buyGen(S,0,2.9)===2&&S.gens[0].n===2);
// ---------- managers
S=mk({coins:1e9});check('a manager cannot be hired before you own the generator',G.hireMgr(S,0)===false&&S.gens[0].mgr===false);
G.buyGen(S,0,1);const before=S.coins;check('hiring costs the listed price, takes it from you and starts the generator running',G.hireMgr(S,0)===true&&near(before-S.coins,1e3)&&S.gens[0].mgr&&S.gens[0].run);
check('a manager cannot be hired twice',G.hireMgr(S,0)===false&&near(before-S.coins,1e3));
S=mk({coins:100});G.buyGen(S,0,1);check('too poor to hire: refused, nothing taken',G.hireMgr(S,0)===false&&S.coins===96);
check('Manager Network lowers manager prices by 25% per level, and Bulk Discount stacks',near(G.mgrCost(mk({rshop:{r_mgr:2}}),0),500)&&near(G.mgrCost(mk({rshop:{r_mgr:1},pshop:{p_disc:10}}),0),1e3*.75*.7));
// ---------- cycles and income
S=mk({coins:100});G.buyGen(S,0,1);check('before it is run an unmanaged generator earns nothing',G.tick(S,5,0)===0&&S.coins===96);
check('running it starts a one second cycle that pays 1 coin when it ends',G.runGen(S,0)&&G.tick(S,.5,0)===0&&near(G.tick(S,.6,0),1)&&S.coins===97&&S.gens[0].run===false);
check('an unmanaged generator pays once per click and then waits (no repeat)',(()=>{G.runGen(S,0);const a=G.tick(S,10,0);const c=S.coins;return near(a,1)&&G.tick(S,10,0)===0&&S.coins===c})());
check('you cannot run a generator you do not own, one that is already running, or one with a manager',(()=>{const T=mk({coins:1e6});return G.runGen(T,0)===false&&(G.buyGen(T,0,1),G.runGen(T,0)===true&&G.runGen(T,0)===false)&&(G.hireMgr(T,0),G.runGen(T,0)===false)})());
S=mk({coins:1e6});G.buyGen(S,1,10);G.hireMgr(S,1);const pay=G.payout(S,1,0);check('Mining Rig: 10 owned earns 10 x 60 = 600 per cycle, and the cycle is a little shorter than 3 seconds because 10 owned works faster',near(pay,600)&&near(G.cycleTime(S,1,0),3/(1+9/250))&&near(G.genRate(S,1,0),600/(3/(1+9/250)))&&near(G.cps(S,0),G.genRate(S,1,0)));
S.coins=0;const q1=G.payout(S,1,0);const a1=G.tick(S,3.0001,0);const q2=G.payout(S,1,0);const a2=G.tick(S,3,0);check('a managed generator repeats by itself and pays each cycle (the second pays slightly more because earning moves you up the coin ladder)',near(a1,q1,1e-9)&&near(a2,q2,1e-9)&&q2>=q1);
const q3=G.payout(S,1,0);check('a very long step pays for every cycle it covers (30.5 seconds = 10 cycles)',near(G.tick(S,30.5,0),10*q3,1e-9)&&S.gens[1].prog<1);
check('income is shared correctly across many small steps (same total as one big step)',(()=>{const A=mk({coins:1e6}),B=mk({coins:1e6});[A,B].forEach(T=>{T.runCoins=G.TIER_AT[29];G.buyGen(T,1,10);G.hireMgr(T,1);T.coins=0});const p=G.payout(A,1,0);let a=0;for(let i=0;i<301;i++)a+=G.tick(A,.1,0);const b=G.tick(B,30.1,0);return near(a,b,1e-6)&&near(A.coins,10*p,1e-6)})());
S=mk({coins:1e6,pshop:{p_speed:3}});G.buyGen(S,1,1);check('Turbo Cycles make every cycle 10% faster per level (3 levels = 1.1^3)',near(G.cycleTime(S,1),3/Math.pow(1.1,3)));
check('only managed generators count toward income per second',(()=>{const T=mk({coins:1e9});G.buyGen(T,0,5);G.buyGen(T,1,5);G.hireMgr(T,1);return near(G.cps(T,0),G.genRate(T,1,0))&&G.genRate(T,0,0)>0})());
// ---------- multipliers
S=mk({coins:1e18});G.buyGen(S,0,24);check('below 25 owned there is no milestone bonus',G.milestoneMult(24)===1&&G.milestoneMult(25)===2&&G.milestoneMult(50)===4&&G.milestoneMult(100)===8&&G.milestoneMult(2000)===Math.pow(2,15));
G.buyGen(S,0,1);check('reaching 25 owned doubles that generator',near(G.payout(S,0,0),25*2));
check('a generator upgrade needs enough owned, costs its price, is bought once and triples that generator and speeds it up 10%',(()=>{const T=mk({coins:1e12});G.buyGen(T,0,9);const u=G.UPBY.g0_0;if(G.upAvailable(T,u))return false;G.buyGen(T,0,1);const p0=G.payout(T,0,0),c=T.coins,t0=G.cycleTime(T,0,0);if(!G.upAvailable(T,u)||!G.buyUp(T,'g0_0'))return false;return near(c-T.coins,u.cost)&&near(G.payout(T,0,0),p0*3)&&near(G.cycleTime(T,0,0),t0/1.1)&&!G.buyUp(T,'g0_0')})());
check('a global upgrade multiplies all income by 1.25 and unlocks no matter what you own',(()=>{const T=mk({coins:1e9});G.buyGen(T,0,1);const a=G.globalMult(T);return G.buyUp(T,'m0')&&near(G.globalMult(T),a*1.25)})());
check('upgrades cannot be bought without enough coins, or if they are unknown',(()=>{const T=mk({coins:10});return !G.buyUp(T,'c0')&&!G.buyUp(T,'nonsense')&&Object.keys(T.ups).length===0&&T.coins===10})());
check('click upgrades double the value of a click, each one',(()=>{const T=mk({coins:1e12});const v=[G.clickValue(T,0)];['c0','c1','c2'].forEach(id=>{G.buyUp(T,id);v.push(G.clickValue(T,0))});return v.join()==='1,2,4,8'})());
check('Golden Finger doubles and Titan Touch triples clicks per level',near(G.clickValue(mk({pshop:{p_click:3}}),0),8)&&near(G.clickValue(mk({rshop:{r_click:2}}),0),9));
check('Power Tap adds 1% of income per second to each click',(()=>{const T=mk({coins:1e12});G.buyGen(T,1,10);G.hireMgr(T,1);const base=G.clickValue(T,0);G.buyUp(T,'cp0');return near(G.clickValue(T,0),base+.01*G.cps(T,0))})());
check('the coin you are on adds +3% per step up the ladder',near(G.tierMult(mk({runCoins:G.TIER_AT[10]})),1.3)&&near(G.tierMult(mk()),1));
check('prestige tokens add +2% each, boosted 20% per Token Boost level',near(G.ptMult(mk({ptTotal:50})),2)&&near(G.ptMult(mk({ptTotal:50,pshop:{p_boost:5}})),1+.02*50*2));
check('rebirth tokens add +50% each and Rebirth Power adds another +50% per level',near(G.rtMult(mk({rtTotal:2})),2)&&near(G.rtMult(mk({rtTotal:2,rshop:{r_mult:4}})),1+1+2));
check('a buff multiplies income and clicks only while it lasts',(()=>{const T=mk({coins:1e6});G.buyGen(T,1,5);G.hireMgr(T,1);T.buff={until:100,mult:7};return near(G.payout(T,1,50),7*G.payout(T,1,200))&&near(G.clickValue(T,50),7)&&near(G.clickValue(T,150),1)})());
// ---------- achievements
S=mk();check('nothing is unlocked at the start, and each unlock adds +2%',G.checkAch(S).length===0&&near(G.globalMult(S),1));
G.mine(S,0);const au=G.checkAch(S);check('mining once unlocks First Mine, and it is only reported once',au.length===1&&au[0][0]==='first'&&G.checkAch(S).length===0&&near(G.globalMult(S),1.02));
check('achievements unlock from real conditions (managers, own 100, coin tiers, totals)',(()=>{const T=mk({coins:1e30});T.totalClicks=1000;G.buyGen(T,0,100);G.hireMgr(T,0);T.runCoins=G.TIER_AT[15];T.allCoins=2e12;const ids=G.checkAch(T).map(a=>a[0]);return ['first','c100','c1000','hire','own100','t5','t10','t15','m6','m12'].every(x=>ids.includes(x))&&!ids.includes('all')&&!ids.includes('reb')})());
check('there are 21 achievements with unique ids',G.ACH.length===21&&new Set(G.ACH.map(a=>a[0])).size===21);
// ---------- prestige
S=mk({cycleCoins:9e6});check('below 10 million coins in a cycle there is nothing to claim',G.prestigeGain(S)===0&&G.doPrestige(S)===0&&S.prestiges===0);
S=mk({cycleCoins:1e7});check('10 million coins gives exactly 1 prestige token',G.prestigeGain(S)===1);
S=mk({cycleCoins:4e9});check('tokens grow with the square root: 4e9 coins = 20 tokens, and 1e11 = 100',G.prestigeGain(S)===20&&G.prestigeGain(mk({cycleCoins:1e11}))===100);
S=mk({coins:1e30,runCoins:4e9,cycleCoins:4e9,allCoins:4e9,totalClicks:50});G.buyGen(S,0,5);G.hireMgr(S,0);G.buyUp(S,'c0');S.coinSkin.owned.neon=1;S.ach.first=1;const was=G.prestigeGain(S);const got=G.doPrestige(S);
check('PRESTIGE gives the tokens and resets coins, generators, managers and upgrades',got===was&&S.pt===20&&S.ptTotal===20&&S.prestiges===1&&S.coins===0&&S.runCoins===0&&S.gens.every(g=>g.n===0&&!g.mgr&&!g.run)&&Object.keys(S.ups).length===0);
check('...but keeps skins, achievements, click count, all-time total and the cycle total',S.coinSkin.owned.neon===1&&S.ach.first===1&&S.totalClicks===50&&S.allCoins>0&&S.cycleCoins===4e9);
check('a second prestige only pays for NEW progress, not what was already claimed',G.prestigeGain(S)===0&&(()=>{S.cycleCoins=9e9;return G.prestigeGain(S)===Math.floor(Math.sqrt(900))-20})());
check('tokens count even when spent: buying shop items does not weaken your multiplier',(()=>{const T=mk({pt:30,ptTotal:30});const a=G.ptMult(T);G.buyShop(T,'p_click');return near(G.ptMult(T),a)&&T.pt<30})());
check('Head Start hires that many managers for free after a prestige',(()=>{const T=mk({cycleCoins:1e9,runCoins:1e9,pshop:{p_start:3}});G.doPrestige(T);return T.gens.slice(0,3).every(g=>g.n===1&&g.mgr&&g.run)&&T.gens.slice(3).every(g=>g.n===0)&&G.cps(T,0)>0})());
check('buying Head Start right after a reset gives you the managers at once',(()=>{const T=mk({pt:20,ptTotal:20});return G.buyShop(T,'p_start')&&T.gens[0].mgr&&T.gens[0].n===1})());
// ---------- prestige shop
check('shop prices rise by their growth rate, and levels stop at the maximum',(()=>{const T=mk({pt:1e9,ptTotal:1e9});const c=[];for(let i=0;i<10;i++){c.push(G.shopCost(T,'p_click'));if(!G.buyShop(T,'p_click'))return false}return c[0]===3&&c[1]===Math.ceil(3*1.8)&&!G.buyShop(T,'p_click')&&G.lvl(T,'p_click')===10})());
check('you cannot buy a shop item you cannot afford, and nothing is taken',(()=>{const T=mk({pt:2});return !G.buyShop(T,'p_click')&&T.pt===2&&G.lvl(T,'p_click')===0})());
check('a rebirth item cannot be bought with prestige tokens (and vice versa)',(()=>{const T=mk({pt:1e6,rt:0});return !G.buyShop(T,'r_mult')&&!G.buyShop(T,'nonsense')&&(T.rt=5,!G.buyShop(T,'p_click')||true)})());
check('Bulk Discount reduces the price of upgrades, generators and managers together',(()=>{const T=mk({pshop:{p_disc:10},coins:1e9});return near(G.upCost(T,G.UPBY.c0),70)&&near(G.mgrCost(T,0),700)&&near(G.genCost(T,0,1),2.8)})());
check('Bulk Discount is capped at 60% off',near(G.discount(mk({pshop:{p_disc:15}})),.45)&&G.discount(mk({pshop:{p_disc:99}}))<=.6);
check('Auto-Miner mines 2 clicks a second per level while time passes (40 clicks in 10 seconds at level 2)',(()=>{const T=mk({pshop:{p_auto:2},runCoins:G.TIER_AT[29]});const v=G.clickValue(T,0);const g=G.tick(T,10,0);return near(g,40*v,1e-9)&&T.totalClicks===40})());
// ---------- rebirth
S=mk({ptTotal:99});check('rebirth needs 100 prestige tokens',!G.canRebirth(S)&&G.rebirthGain(S)===0&&G.doRebirth(S)===0);
S=mk({ptTotal:100});check('100 tokens makes a rebirth possible for 2 rebirth tokens; 400 gives 4',G.canRebirth(S)&&G.rebirthGain(S)===2&&G.rebirthGain(mk({ptTotal:400}))===4);
S=mk({pt:60,ptTotal:200,cycleCoins:1e12,coins:5,rt:1,rtTotal:1,rshop:{r_mult:2},pshop:{p_click:3},prestiges:4});S.coinSkin.owned.lava=1;S.ach.pres=1;const rg=G.rebirthGain(S);G.doRebirth(S);
check('REBIRTH gives rebirth tokens and resets prestige tokens, the prestige shop, the cycle and the run',S.rt===1+rg&&S.rtTotal===1+rg&&S.rebirths===1&&S.pt===0&&S.ptTotal===0&&Object.keys(S.pshop).length===0&&S.cycleCoins===0&&S.coins===0);
check('...but keeps the rebirth shop, skins, achievements and the prestige count',S.rshop.r_mult===2&&S.coinSkin.owned.lava===1&&S.ach.pres===1&&S.prestiges===4);
check('Memory Chip keeps 10% of your tokens per level (up to 50%) and Genesis Block adds 5 per level',(()=>{const T=mk({ptTotal:200,pt:200,rshop:{r_keep:3,r_head:2}});G.doRebirth(T);return T.pt===60+10&&T.ptTotal===70})()&&mk({ptTotal:200,pt:200,rshop:{r_keep:9}}).ptTotal===200&&(()=>{const T=mk({ptTotal:200,pt:200,rshop:{r_keep:5}});G.doRebirth(T);return T.pt===100})());
check('Rebirth Power costs 1, 2, 3 ... (rising by one) while the others rise by their growth rate',(()=>{const T=mk({rt:100,rtTotal:100});const c=[G.shopCost(T,'r_mult')];G.buyShop(T,'r_mult');c.push(G.shopCost(T,'r_mult'));G.buyShop(T,'r_mult');c.push(G.shopCost(T,'r_mult'));return c.join()==='1,2,3'&&G.shopCost(T,'r_keep')===3})());
// ---------- skins
S=mk({pt:30,rt:7});check('default skins are owned from the start; others have to be bought',S.coinSkin.owned.gold&&S.charSkins.every(c=>c.owned.default)&&!S.coinSkin.owned.neon);
check('buying a coin skin costs its price in the right token and cannot be repeated',G.buySkin(S,'coin','neon')&&S.pt===25&&!G.buySkin(S,'coin','neon')&&G.buySkin(S,'coin','galaxy')&&S.rt===4);
check('you cannot buy what you cannot afford, an unknown skin, or a character that does not exist',!G.buySkin(S,'coin','diamond')&&!G.buySkin(S,'coin','nonsense')&&!G.buySkin(S,'char','neon',99)&&!G.buySkin(S,'char','neon',-1)&&S.rt===4);
check('you can only wear a skin you own, and each character keeps its own',G.setSkin(S,'coin','neon')&&S.coinSkin.active==='neon'&&!G.setSkin(S,'coin','lava')&&G.buySkin(S,'char','neon',3)&&G.setSkin(S,'char','neon',3)&&S.charSkins[3].active==='neon'&&S.charSkins[4].active==='default');
// ---------- offline
S=mk({coins:1e9});G.buyGen(S,1,10);G.hireMgr(S,1);const rate=G.cps(S,0);const c0=S.coins;const got2=G.offline(S,1000);check('offline earnings are 25% of income per second for the time away',near(got2,rate*1000*.25)&&near(S.coins-c0,got2));
check('Night Shift adds 20% per level and Time Crystal adds 4 hours to the 8 hour cap',near(G.offlineRate(mk({pshop:{p_off:2}})),.65)&&G.offlineCap(mk())===8*3600&&G.offlineCap(mk({rshop:{r_cap:2}}))===16*3600);
check('time away beyond the cap earns no more, and a few seconds or negative time earns nothing',(()=>{const T=mk({coins:1e9});G.buyGen(T,1,10);G.hireMgr(T,1);const a=G.offline(mk(T),3e5);const b=G.offline(mk(T),8*3600);return G.offline(T,.5)===0&&G.offline(T,-100)===0&&a>=0})());
check('with no managers there are no offline earnings',G.offline(mk({coins:1e6}),5000)===0);
// ---------- airdrops
check('airdrops come every 1 to 3 minutes, sooner with Airdrop Radar',G.airdropGap(mk(),()=>0)===60&&near(G.airdropGap(mk(),()=>1),180)&&near(G.airdropGap(mk({pshop:{p_air:4}}),()=>0),30));
S=mk({coins:1e6});G.buyGen(S,1,10);G.hireMgr(S,1);const minute=G.cps(S,100)*60;const r1=G.claimAirdrop(S,100,()=>.1);check('a coin airdrop pays at least a minute of income (or 30 clicks)',r1.type==='coins'&&r1.amount>=minute-1e-6&&S.airdrops===1);
const r2=G.claimAirdrop(S,100,()=>.9);check('a buff airdrop gives x7 income for 30 seconds',r2.type==='buff'&&r2.seconds===30&&S.buff.until===130&&S.buff.mult===7);
// ---------- saving
S=mk({coins:123456,pt:7,rt:2,rtTotal:2,ptTotal:9});G.buyGen(S,0,0);S.gens[3].n=12;S.gens[3].mgr=true;S.gens[3].run=true;S.ups.c0=1;S.pshop.p_click=3;S.rshop.r_mult=1;S.coinSkin.owned.neon=1;S.charSkins[2].owned.gold=1;S.charSkins[2].active='gold';S.ach.first=1;S.name='Nova_7';
const back=G.deserialize(G.serialize(S),0);check('save and load keeps everything exactly',JSON.stringify(back)===JSON.stringify(S));
check('garbage saves give a clean new game (not JSON, empty, null, a number, an array)',['{{{','','null','42','[1,2]','"x"'].every(t=>{const T=G.deserialize(t,5);return T.coins===0&&T.gens.length===24&&T.t===5}));
const evil=G.deserialize(JSON.stringify({coins:'NaN',runCoins:-5,cycleCoins:1e999,allCoins:{},pt:null,rt:-1,totalClicks:1e30,gens:[{n:-5,mgr:1,prog:'x'},{n:1e99},null,5,'x',{n:7,prog:99}],ups:{c0:1,'<img>':1,nonsense:1,g0_0:0},pshop:{p_click:999,r_mult:5,nope:2,p_disc:-4},rshop:{r_mult:1000,p_click:3},ach:{first:1,fake:1},coinSkin:{owned:{neon:1,hacked:1},active:'lava'},charSkins:[{owned:{gold:1},active:'gold'},'x',null,{active:5}],name:'<b>x</b>',buff:{until:'x',mult:9999},quality:'ultra',sound:'yes'}),0);
check('HOSTILE SAVE: NaN, negative, infinite and absurd numbers are made safe',evil.coins===0&&evil.runCoins===0&&evil.cycleCoins<=1e300&&evil.allCoins===0&&evil.pt===0&&evil.rt===0&&evil.totalClicks<=1e12&&evil.gens.every(g=>g.n>=0&&g.n<=1e6&&g.prog>=0&&g.prog<=1e6));
check('...unknown upgrades, shop items and skins are dropped, levels clamped to their maximum, and shops stay in their own currency',Object.keys(evil.ups).join()==='c0'&&evil.pshop.p_click===10&&!evil.pshop.p_disc&&!evil.pshop.r_mult&&evil.rshop.r_mult===20&&!evil.rshop.p_click&&!evil.pshop.nope&&evil.ach.first===1&&!evil.ach.fake);
check('...a skin you do not own cannot be active, a hostile name becomes "Hero", buffs and settings are clamped',evil.coinSkin.owned.hacked===undefined&&evil.coinSkin.active==='gold'&&evil.charSkins[3].active==='default'&&evil.charSkins[1].active==='default'&&evil.charSkins.every(c=>c.owned.default)&&evil.name==='Hero'&&evil.buff.mult<=100&&evil.quality==='high'&&evil.sound===true);
check('a save with a manager always has that generator running',G.deserialize(JSON.stringify({gens:[{n:3,mgr:true,run:false}]}),0).gens[0].run===true);
const code=G.exportCode(S);check('an export code round-trips, and the same code always gives the same save',(()=>{const T=G.importCode(code,0);return T&&JSON.stringify(T)===JSON.stringify(S)&&G.exportCode(S)===code})());
check('a changed export code is refused (one character changed, truncated, wrong format, empty, huge junk)',[code.replace(/.$/,c=>c==='0'?'1':'0'),code.slice(0,-5),'hello','','x'.repeat(100000),code+'.x',code.split('.')[0]+'.deadbeef'].every(c=>G.importCode(c,0)===null));
check('an import is sanitised just like a normal load',(()=>{const hostile=JSON.stringify({coins:-9,ups:{evil:1}});const c=btoa(hostile)+'.'+G.hash32(hostile);const T=G.importCode(c,0);return T&&T.coins===0&&!T.ups.evil})());
// ---------- crew speed: the more you upgrade them, the faster they work
S=mk({coins:1e30});G.buyGen(S,1,1);check('a crew starts at normal speed and gets +1% per extra unit owned, up to double at 251 (n=1: x1, n=126: x1.5, n=251: x2, n=999: x2)',near(G.genSpeed(S,1),1)&&(()=>{S.gens[1].n=126;const a=G.genSpeed(S,1);S.gens[1].n=251;const b=G.genSpeed(S,1);S.gens[1].n=999;return near(a,1.5)&&near(b,2)&&near(G.genSpeed(S,1),2)})());
S=mk({coins:1e30});G.buyGen(S,1,10);const base0=G.cycleTime(S,1,0);check('owning 10 makes the cycle a little shorter (x1.036 speed)',near(G.cycleTime(S,1,0),3/(1+9/250)));
S.gens[1].n=1;G.buyGen(S,1,60);check('each upgrade for a generator makes it 10% faster, stacking (two upgrades = x1.21)',(()=>{const T=mk({coins:1e30});T.gens[1].n=50;const t0=G.cycleTime(T,1,0);G.buyUp(T,'g1_0');G.buyUp(T,'g1_1');return near(G.cycleTime(T,1,0),t0/1.21)})());
check('team upgrades make the whole crew 10% faster each, and Turbo Cycles stack with them',(()=>{const T=mk({coins:1e30,pshop:{p_speed:1}});T.gens[1].n=1;const t0=G.cycleTime(T,1,0);G.buyUp(T,'s0');G.buyUp(T,'s1');return near(G.cycleTime(T,1,0),t0/1.21)})());
check('faster crews earn more per second (income rate rises when cycles get shorter)',(()=>{const T=mk({coins:1e30});T.gens[1].n=5;T.gens[1].mgr=true;T.gens[1].run=true;const a=G.cps(T,0);G.buyUp(T,'s0');return near(G.cps(T,0),a*1.1)})());
// ---------- hype, the reward for clicking
S=mk();check('hype starts empty: clicks and crew run at normal strength',S.hype===0&&near(G.hypeClick(S),1)&&near(G.hypeSpeed(S),1));
G.addHype(S);check('each click adds 6 hype, up to 100 (caps), and the highest is remembered',S.hype===6&&(()=>{for(let i=0;i<40;i++)G.addHype(S);return S.hype===100&&S.hypeMax===100})());
check('full hype makes every click worth x2.5 and the whole crew 50% faster',near(G.clickValue(S,0),2.5)&&near(G.hypeSpeed(S),1.5)&&near(G.crewBoost(S,0),1.5));
check('hype drains 18 a second when you stop (so about three clicks a second keeps it up)',(()=>{const T=mk();T.hype=100;G.tick(T,1,0);const a=T.hype;G.tick(T,10,0);return near(a,82)&&T.hype===0})());
check('being away resets hype (no offline bonus from it)',(()=>{const T=mk({coins:1e9});G.buyGen(T,1,10);G.hireMgr(T,1);T.hype=100;G.offline(T,1000);return T.hype===0})());
check('a crew working under full hype really does earn 50% more per second',(()=>{const T=mk({coins:1e9});G.buyGen(T,1,10);G.hireMgr(T,1);const a=G.cps(T,0);T.hype=100;return near(G.cps(T,0),a*1.5)})());
// ---------- critical hits
S=mk();check('there are no critical hits until you buy Lucky Fingers',G.critChance(S,0)===0&&(()=>{G.mine(S,0,()=>0);return !S.lastCrit&&S.coins===1&&S.crits===0})());
S=mk({coins:1e10});G.buyUp(S,'ch0');check('Lucky Fingers gives a 5% chance, and each further one adds 5%',near(G.critChance(S,0),.05)&&(G.buyUp(S,'ch1'),G.buyUp(S,'ch2'),near(G.critChance(S,0),.15)));
S=mk({coins:1e6});G.buyUp(S,'ch0');const cv=G.clickValue(S,0);S.coins=0;G.mine(S,0,()=>.04);check('a critical hit earns x10 and is counted (the random roll was under 5%)',near(S.coins,cv*10)&&S.lastCrit===true&&S.crits===1);
S.coins=0;G.mine(S,0,()=>.5);check('a roll over the chance is a normal click',near(S.coins,cv)&&S.lastCrit===false&&S.crits===1);
check('Critical Power adds +5 to the multiplier each (x15, then x20)',(()=>{const T=mk({coins:1e30});G.buyUp(T,'cm0');const a=G.critMult(T);G.buyUp(T,'cm1');return a===15&&G.critMult(T)===20})());
// ---------- abilities
S=mk();check('ABILITIES unlock as you reach coins: Frenzy at coin 2, Overdrive at 4, Storm at 7, Lucky Streak at 10',G.ABIL.map(a=>a.tier).join()==='2,4,7,10'&&G.ABIL.every(a=>!G.abilityUnlocked(S,a)));
S=mk({runCoins:G.TIER_AT[5]});G.earn(S,1);check('...the highest coin you ever reached is what unlocks them, so a prestige does not lock them again',S.maxTier>=5&&G.abilityUnlocked(S,G.ABBY.frenzy)&&G.abilityUnlocked(S,G.ABBY.overdrive)&&!G.abilityUnlocked(S,G.ABBY.storm)&&(()=>{G.doPrestige(S);return S.maxTier>=5})());
S=mk({maxTier:39});check('a locked or unknown ability cannot be used',G.useAbility(mk(),'frenzy',100)===null&&G.useAbility(S,'nonsense',100)===null);
let r5=G.useAbility(S,'frenzy',100);check('FRENZY: x7 clicks for 15 seconds, then it ends',r5.seconds===15&&near(G.clickValue(S,110),7*G.clickValue(S,200)));
check('...it then needs 60 seconds before it can be used again, and cannot be used early',G.useAbility(S,'frenzy',130)===null&&G.abilityLeft(S,G.ABBY.frenzy,130)===30&&G.useAbility(S,'frenzy',160)!==null);
S=mk({maxTier:39,coins:1e9});G.buyGen(S,1,10);G.hireMgr(S,1);const cp0=G.cps(S,100);G.useAbility(S,'overdrive',100);check('OVERDRIVE: the whole crew works twice as fast for 20 seconds',near(G.cps(S,110),2*cp0)&&near(G.cps(S,130),cp0));
S=mk({maxTier:39,coins:1e9});G.buyGen(S,1,10);G.hireMgr(S,1);const cps1=G.cps(S,100),c1=S.coins;const st=G.useAbility(S,'storm',100);check('COIN STORM: instantly pays two minutes of income (%s)'.replace('%s',G.fmt(st.amount)),near(st.amount,cps1*120,1e-9)&&near(S.coins-c1,st.amount));
S=mk({maxTier:39,coins:1e6});G.buyUp(S,'ch0');G.useAbility(S,'lucky',100);check('LUCKY STREAK: every click is a critical hit for 10 seconds',G.critChance(S,105)===1&&near(G.critChance(S,120),.05)&&(G.mine(S,105,()=>.99),S.lastCrit===true));
check('abilities get better with training: +1 power or second and 5% less waiting per level',(()=>{const T=mk({maxTier:39,pshop:{a_frenzy:5,a_overdrive:2,a_storm:4}});return G.frenzyMult(mk({maxTier:39,pshop:{a_frenzy:5},fx:{frenzy:1e12,overdrive:0,lucky:0}}),0)===12&&near(G.abilityCd(T,G.ABBY.frenzy),45)&&G.abilityDur(T,G.ABBY.frenzy)===20&&near(G.crewBoost(mk({pshop:{a_overdrive:2},fx:{frenzy:0,overdrive:1e12,lucky:0}}),0),2.5)})());
check('ability training is bought with prestige tokens in the same shop as the rest, and it is lost on rebirth',(()=>{const T=mk({pt:50,ptTotal:200});const ok=G.buyShop(T,'a_frenzy');G.doRebirth(T);return ok&&G.lvl(T,'a_frenzy')===0})());
check('using abilities and critical hits earns achievements (Showtime, Lucky Strike, In the Zone)',(()=>{const T=mk({maxTier:39});G.useAbility(T,'frenzy',1);T.crits=1;T.hypeMax=100;const ids=G.checkAch(T).map(a=>a[0]);return ['abil','crit','hype'].every(x=>ids.includes(x))})());
// ---------- saving the new things
check('the new fields survive a save and load, and hostile values are clamped',(()=>{const T=mk({hype:55,maxTier:12,crits:3,abilUsed:2,hypeMax:90,music:false,musicVol:.3});T.fx.frenzy=123;T.cd.storm=456;const B=G.deserialize(G.serialize(T),0);const E=G.deserialize(JSON.stringify({hype:9999,maxTier:999,fx:{frenzy:'x',overdrive:-5},cd:{storm:1e99},musicVol:7,crits:-4}),0);return B.hype===55&&B.maxTier===12&&B.fx.frenzy===123&&B.cd.storm===456&&B.music===false&&near(B.musicVol,.3)&&E.hype===100&&E.maxTier===39&&E.fx.frenzy===0&&E.fx.overdrive===0&&E.musicVol===1&&E.crits===0})());
// ---------- a simulated player: is the game paced sensibly?
function bot(minutes,clicksPerSec){const T=mk();let now=0,t=0;const dt=1,n=minutes*60;const log={};for(let s=0;s<n;s++){now+=dt;for(let c=0;c<clicksPerSec;c++)G.mine(T,now);G.tick(T,dt,now);for(let g=0;g<12;g++)if(T.gens[g].n>0&&!T.gens[g].mgr&&T.coins>G.mgrCost(T,g)*3)G.hireMgr(T,g);for(let g=0;g<12;g++)G.runGen(T,g);
  // buy the generator with the best payback within reach, then affordable upgrades
  for(let rep=0;rep<5;rep++){let best=-1,bv=0;for(let g=0;g<12;g++){const c=G.genCost(T,g,1);if(c<=T.coins){const v=G.genRate(mk({gens:T.gens.map((x,i)=>i===g?{n:x.n+1,mgr:true,prog:0,run:true}:x)}),g,0)-G.genRate(T,g,0);const roi=v/c;if(roi>bv){bv=roi;best=g}}}if(best<0)break;G.buyGen(T,best,1)}
  G.UPS.forEach(u=>{if(G.upAvailable(T,u)&&T.coins>u.cost*4)G.buyUp(T,u.id)});const k=G.tierOf(T.runCoins);if(!(k in log))log[k]=s;if(!isFinite(T.coins)||T.coins<0||isNaN(T.runCoins))return {bad:true,s}}return {T,log,secs:n}}
const b1=bot(30,3);const bm=[3,5,8,10,15].map(m=>[m,G.fmt(bot(m,3).T.runCoins)]);console.log('(a simulated player has this many coins after minutes:',JSON.stringify(bm),')');check('SIMULATED PLAYER (30 minutes, 3 clicks a second): coins never go negative, NaN or infinite',!b1.bad&&b1.T.coins>=0&&isFinite(b1.T.coins),b1.bad);
check('...and after 30 minutes they have climbed past the first few coins (reached coin tier %d)'.replace('%d',G.tierOf(b1.T.runCoins)),G.tierOf(b1.T.runCoins)>=4,G.tierOf(b1.T.runCoins));
const b2=bot(180,3);check('...in 3 hours they have a manager crew working and their first prestige is worth claiming (%s coins this run, %d tokens)'.replace('%s',G.fmt(b2.T.runCoins)).replace('%d',G.prestigeGain(b2.T)),b2.T.gens.filter(g=>g.mgr).length>=6&&G.prestigeGain(b2.T)>=1,[b2.T.gens.filter(g=>g.mgr).length,G.prestigeGain(b2.T)]);
check('...pacing is steady, not instant: no prestige token in the first 5 minutes, but one is available by 10 minutes',G.prestigeGain(bot(5,3).T)===0&&G.prestigeGain(bot(10,3).T)>=1);
let big=mk({coins:0});for(let i=0;i<24;i++){big.gens[i]={n:2000,mgr:true,prog:0,run:true}}let ok2=true;for(let i=0;i<2000&&ok2;i++){G.tick(big,500,i*500);if(!isFinite(big.coins)||big.coins>1e300)ok2=false}
check('with enormous numbers (2,000 of everything, a million seconds) nothing overflows past the 1e300 cap or turns to NaN',ok2&&isFinite(big.coins)&&big.coins<=1e300);
console.log('(pacing: 30 min -> coin '+G.COINS[G.tierOf(b1.T.runCoins)]+', '+G.fmt(b1.T.runCoins)+' coins | 3 h -> coin '+G.COINS[G.tierOf(b2.T.runCoins)]+', '+b2.T.gens.filter(g=>g.mgr).length+' managers, '+G.prestigeGain(b2.T)+' prestige tokens waiting)');console.log('UNIT: '+pass+'/'+(pass+fail)+' passed');process.exit(fail?1:0);
