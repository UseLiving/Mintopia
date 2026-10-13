// ======== Hodl Heroes: the rules of the game (no drawing here, so it can be tested on its own) ========
var HH_VERSION=2,SAVE_KEY='mintopia_save_v1',OLD_SAVE_KEY='hodlheroes_save_v1';
var GEN=[
 {name:'Paper Wallet',cost:4,coef:1.07,rev:1,time:1,mgr:1e3,mgrName:'Penny Pocket',kind:'human'},
 {name:'Mining Rig',cost:60,coef:1.15,rev:60,time:3,mgr:1.5e4,mgrName:'Big Mo',kind:'human'},
 {name:'GPU Farm',cost:720,coef:1.14,rev:540,time:6,mgr:1e5,mgrName:'Dr. Volt',kind:'human'},
 {name:'Validator Node',cost:8640,coef:1.13,rev:4320,time:12,mgr:5e5,mgrName:'Grizzle',kind:'monster'},
 {name:'Exchange Desk',cost:103680,coef:1.12,rev:51840,time:24,mgr:1.2e7,mgrName:'Captain Sato',kind:'human'},
 {name:'DeFi Protocol',cost:1.24416e6,coef:1.11,rev:622080,time:96,mgr:1.3e8,mgrName:'Ogg the Ledger',kind:'monster'},
 {name:'Cross-Chain Bridge',cost:1.492992e7,coef:1.10,rev:7.46496e6,time:384,mgr:2.5e9,mgrName:'Zara Vault',kind:'human'},
 {name:'NFT Gallery',cost:1.7915904e8,coef:1.09,rev:8.957952e7,time:1536,mgr:2.5e10,mgrName:'Skully',kind:'monster'},
 {name:'DAO Treasury',cost:2.14990848e9,coef:1.08,rev:1.07495424e9,time:6144,mgr:2.5e11,mgrName:'Cyclo',kind:'monster'},
 {name:'Trading Bot Army',cost:2.579890176e10,coef:1.07,rev:1.289945088e10,time:36864,mgr:2.5e12,mgrName:'Imp Inc.',kind:'monster'},
 {name:'Metaverse Mint',cost:3.0958682112e11,coef:1.065,rev:1.5479341e11,time:221184,mgr:2.5e13,mgrName:'Madame Nova',kind:'human'},
 {name:'Whale Fund',cost:3.71504185e12,coef:1.06,rev:1.8575209e12,time:1327104,mgr:2.5e14,mgrName:'Lord Whale',kind:'monster'}];
(function(){var N=[['Hacker Den','Aria Hex','human'],['Block Bakery','Chef Nako','human'],['Merkle Library','Prof. Merkle','human'],['Staking Saloon','Sheriff Stakes','human'],['Nonce Dojo','Ninja Nonce','human'],['Orbital Exchange','Captain Orbit','human'],['Cold Storage','Frostbite','monster'],['Dragon Hoard','Embera','monster'],['Bot Foundry','Bolt-9','monster'],['Pharaoh Vault','Mummy Midas','monster'],['Wolf Street','Fang','monster'],['Alien Mint','Zorp','monster']],L=GEN[GEN.length-1],c=L.cost,r=L.rev,m=L.mgr;N.forEach(function(x,k){c*=14;r*=12;m*=10;GEN.push({name:x[0],cost:c,coef:1.058-k*.002,rev:r,time:1.5e6+k*2e5,mgr:m,mgrName:x[1],kind:x[2]})})})();
var MILESTONES=[25,50,100,200,300,400,500,600,700,800,900,1000,1250,1500,2000];
var COINS=['Dust','Pepe','Shiba','Dogecoin','Tron','Stellar','Litecoin','Cardano','Polkadot','Avalanche','Chainlink','Ripple','BNB','Solana','Ethereum','Bitcoin','Moonrock','Marscoin','Galaxy','Nebula','Quasar','Pulsar','Hypernova','Singularity','Multiverse','Omniverse','Infinity','Beyond','Eternity','Genesis','Aether','Void','Prism','Zenith','Apex','Nirvana','Alpha','Omega','Cosmos','Mintopia'];
var TICKERS=['DUST','PEPE','SHIB','DOGE','TRX','XLM','LTC','ADA','DOT','AVAX','LINK','XRP','BNB','SOL','ETH','BTC','MOON','MARS','GLXY','NEBU','QSR','PLSR','HNOV','SING','MULT','OMNI','INF','BYND','ETRN','GEN','AETH','VOID','PRSM','ZNTH','APEX','NRVN','ALPH','OMEG','COSM','MINT'];
var TIER_AT=COINS.map(function(c,k){return k===0?0:Math.pow(10,k*.85+.5)});
var ENDCAP=1e300;
// ---- one-time upgrades: three per generator, click boosts, and global boosts
var UPS=[];
(function(){var i,k,rq=[10,50,150,300,600],mul=[120,6000,3.6e5,2.5e7,2e9],nm=['Overclock','Turbo Boost','Quantum Tune','Hyper Drive','Singularity Core'];
 for(i=0;i<GEN.length;i++)for(k=0;k<5;k++)UPS.push({id:'g'+i+'_'+k,kind:'gen',gen:i,need:rq[k],cost:GEN[i].cost*mul[k],name:GEN[i].name+' '+nm[k],desc:GEN[i].name+' earns x3 and works 10% faster'});
 var cn=['Fast','Steel','Golden','Diamond','Mythic','Godly','Cosmic','Eternal','Infinite','Absolute'],cc=[100,500,1e4,1e5,1e7,1e9,1e11,1e13,1e15,1e18];cn.forEach(function(n,j){UPS.push({id:'c'+j,kind:'click',cost:cc[j],name:n+' Fingers',desc:'Clicks earn x2',need:0})});
 [['cp0','Power Tap',5e3,.01],['cp1','Mega Tap',5e6,.02],['cp2','Giga Tap',5e9,.05],['cp3','Tera Tap',5e13,.1]].forEach(function(u){UPS.push({id:u[0],kind:'clickpct',cost:u[2],pct:u[3],name:u[1],desc:'Each click also earns '+Math.round(u[3]*100)+'% of your income per second',need:0})});
 [['ch0','Lucky Fingers',800],['ch1','Fortune Fingers',5e5],['ch2','Destiny Fingers',5e8]].forEach(function(u){UPS.push({id:u[0],kind:'crit',cost:u[2],chance:.05,name:u[1],desc:'+5% chance that a click is a critical hit (x10)',need:0})});
 [['cm0','Critical Power',5e4],['cm1','Critical Mass',5e10]].forEach(function(u){UPS.push({id:u[0],kind:'critmult',cost:u[2],add:5,name:u[1],desc:'Critical hits earn 5 times more',need:0})});
 var gn=['Bull Market','Hype Cycle','Institutional Money','Mass Adoption','Moon Mission','Cosmic Hodl','Diamond Hands','Whale Season','Golden Age','Stellar Rally','Infinite Bloom','Mintopia Boom'];gn.forEach(function(n,j){UPS.push({id:'m'+j,kind:'global',cost:5e3*Math.pow(1000,j),mult:1.25,name:n,desc:'All income x1.25',need:0})});
 var sn=['Coffee Break','Energy Drinks','Better Chairs','Team Spirit','Hustle Culture','Rocket Fuel'];sn.forEach(function(n,j){UPS.push({id:'s'+j,kind:'speed',cost:2e5*Math.pow(1000,j),mult:1.1,name:n,desc:'Your whole crew works 10% faster',need:0})})})();
var UPBY={},UPGEN=[],UPK={speed:[],crit:[],critmult:[],clickpct:[],click:[],global:[]};UPS.forEach(function(u){UPBY[u.id]=u;if(u.kind==='gen'){(UPGEN[u.gen]=UPGEN[u.gen]||[]).push(u.id)}else UPK[u.kind].push(u.id)});
// ---- shops
var PSHOP=[
 {id:'p_click',name:'Golden Finger',desc:'Clicks earn x2 per level',max:10,base:3,grow:1.8},
 {id:'p_disc',name:'Bulk Discount',desc:'Everything costs 3% less per level',max:15,base:5,grow:1.6},
 {id:'p_auto',name:'Auto-Miner',desc:'Mines automatically: 2 clicks a second per level',max:10,base:10,grow:1.7},
 {id:'p_start',name:'Head Start',desc:'Each level hires one more manager for free after a prestige',max:12,base:8,grow:1.6},
 {id:'p_speed',name:'Turbo Cycles',desc:'All cycles run 10% faster per level',max:10,base:12,grow:1.7},
 {id:'p_boost',name:'Token Boost',desc:'Prestige tokens are 20% stronger per level',max:10,base:20,grow:1.8},
 {id:'p_off',name:'Night Shift',desc:'Offline earnings +20% per level',max:5,base:6,grow:2},
 {id:'p_air',name:'Airdrop Radar',desc:'Airdrops appear sooner and pay more',max:5,base:15,grow:1.9}];
var RSHOP=[
 {id:'r_mult',name:'Rebirth Power',desc:'All income +50% per level',max:20,base:1,grow:1.35,lin:1},
 {id:'r_keep',name:'Memory Chip',desc:'Keep 10% more of your prestige tokens when you rebirth',max:5,base:3,grow:1.5},
 {id:'r_head',name:'Genesis Block',desc:'Start every rebirth with 5 prestige tokens per level',max:10,base:2,grow:1.4},
 {id:'r_mgr',name:'Manager Network',desc:'Managers cost 25% less per level',max:3,base:4,grow:1.8},
 {id:'r_cap',name:'Time Crystal',desc:'Offline earnings last 4 hours longer per level',max:5,base:3,grow:1.7},
 {id:'r_click',name:'Titan Touch',desc:'Clicks earn x3 per level',max:5,base:3,grow:1.8}];
var ABIL=[{id:'frenzy',name:'Frenzy',desc:'Clicks earn x7 for 15 seconds',tier:2,cd:60,dur:15},{id:'overdrive',name:'Overdrive',desc:'Your whole crew works twice as fast for 20 seconds',tier:4,cd:90,dur:20},{id:'storm',name:'Coin Storm',desc:'Instantly earn two minutes of your income',tier:7,cd:150,dur:0},{id:'lucky',name:'Lucky Streak',desc:'Every click is a critical hit for 10 seconds',tier:10,cd:75,dur:10}],ABBY={};
ABIL.forEach(function(a){ABBY[a.id]=a;PSHOP.push({id:'a_'+a.id,name:a.name+' training',desc:'Stronger and ready sooner: +1 power, 5% less waiting per level',max:5,base:4,grow:1.7,ability:true})});
var SHOPBY={};PSHOP.forEach(function(s){SHOPBY[s.id]=s;s.cur='pt'});RSHOP.forEach(function(s){SHOPBY[s.id]=s;s.cur='rt'});
// ---- skins
var COIN_SKINS=[{id:'gold',name:'Classic Gold',cur:'free',cost:0},{id:'neon',name:'Neon Pulse',cur:'pt',cost:5},{id:'lava',name:'Lava Core',cur:'pt',cost:12},{id:'pixel',name:'Pixel Coin',cur:'pt',cost:25},{id:'aurora',name:'Aurora',cur:'pt',cost:60},{id:'galaxy',name:'Galaxy',cur:'rt',cost:3},{id:'diamond',name:'Diamond',cur:'rt',cost:6},{id:'void',name:'Void',cur:'rt',cost:8},{id:'prism',name:'Prism',cur:'rt',cost:12}];
var CHAR_SKINS=[{id:'default',name:'Original',cur:'free',cost:0},{id:'neon',name:'Neon',cur:'pt',cost:10},{id:'frost',name:'Frost',cur:'pt',cost:25},{id:'lava',name:'Inferno',cur:'pt',cost:40},{id:'gold',name:'Golden',cur:'rt',cost:2},{id:'shadow',name:'Shadow',cur:'rt',cost:3},{id:'cosmic',name:'Cosmic',cur:'rt',cost:4},{id:'holo',name:'Holo',cur:'rt',cost:6}];
// ---- achievements (each adds +2% to everything)
var ACH=[
 ['first','First Mine','Mine your first coin',function(S){return S.totalClicks>=1}],['c100','Finger Workout','Click 100 times',function(S){return S.totalClicks>=100}],['c1000','Click Machine','Click 1,000 times',function(S){return S.totalClicks>=1000}],
 ['hire','Boss Mode','Hire your first manager',function(S){return S.gens.some(function(g){return g.mgr})}],['all','Full Crew','Hire your whole crew',function(S){return S.gens.every(function(g){return g.mgr})}],
 ['own100','Hoarder','Own 100 of any generator',function(S){return S.gens.some(function(g){return g.n>=100})}],['ups10','Upgrader','Buy 10 upgrades',function(S){return Object.keys(S.ups).length>=10}],
 ['t5','Meme Money','Reach coin 5: Stellar',function(S){return tierOf(S.runCoins)>=5}],['t10','Blue Chip','Reach coin 10: Chainlink',function(S){return tierOf(S.runCoins)>=10}],['t15','Digital Gold','Reach coin 15: Bitcoin',function(S){return tierOf(S.runCoins)>=15}],['t20','Off World','Reach coin 20: Nebula',function(S){return tierOf(S.runCoins)>=20}],['t25','Beyond','Reach coin 25: Omniverse',function(S){return tierOf(S.runCoins)>=25}],
 ['abil','Showtime','Use an ability',function(S){return S.abilUsed>=1}],['crit','Lucky Strike','Land a critical hit',function(S){return S.crits>=1}],['hype','In the Zone','Fill the hype meter',function(S){return S.hypeMax>=100}],['t30','Mintopian','Reach coin 30: Aether',function(S){return tierOf(S.runCoins)>=30}],['pres','Born Again','Prestige for the first time',function(S){return S.prestiges>=1}],['reb','Reborn','Rebirth for the first time',function(S){return S.rebirths>=1}],
 ['m6','Millionaire','Earn 1 million coins in total',function(S){return S.allCoins>=1e6}],['m12','Trillionaire','Earn 1 trillion coins in total',function(S){return S.allCoins>=1e12}],['m24','Septillionaire','Earn 1 septillion coins in total',function(S){return S.allCoins>=1e24}]];
// ---- numbers
var SUF=['','K','M','B','T','Qa','Qi','Sx','Sp','Oc','No','Dc','Ud','Dd','Td','Qad','Qid','Sxd','Spd','Ocd','Nod','Vg','Uvg','Dvg','Tvg','Qavg','Qivg','Sxvg','Spvg','Ocvg','Novg','Tg'];
function fmt(v,d){if(!isFinite(v))return v>0?'Infinity':'0';if(v<0)return '-'+fmt(-v,d);d=d==null?2:d;if(v<1000)return (v>=100?v.toFixed(0):v>=10?v.toFixed(Math.min(d,1)):v.toFixed(d)).replace(/\.0+$/,'').replace(/(\.\d*[1-9])0+$/,'$1');var e=Math.floor(Math.log10(v)/3),m;if(e>=SUF.length)return v.toExponential(2).replace(/\.?0+e/,'e').replace('e+','e');m=v/Math.pow(1000,e);if(m>=999.995){m=1;e++}return m.toFixed(m>=100?0:m>=10?1:2).replace(/\.0+$/,'').replace(/(\.\d*[1-9])0+$/,'$1')+SUF[e]}
function fmtTime(s){if(!isFinite(s))return '-';if(s<10)return s.toFixed(1)+'s';if(s<60)return Math.round(s)+'s';if(s<3600)return Math.floor(s/60)+'m '+Math.round(s%60)+'s';if(s<86400)return Math.floor(s/3600)+'h '+Math.floor((s%3600)/60)+'m';return Math.floor(s/86400)+'d '+Math.floor((s%86400)/3600)+'h'}
function tierOf(c){var k=0;while(k+1<TIER_AT.length&&c>=TIER_AT[k+1])k++;return k}
function nz(v,d,a,b){v=+v;return isFinite(v)?Math.min(b,Math.max(a,v)):d}
// ---- the state of a game
function newGame(now){var S={v:HH_VERSION,coins:0,runCoins:0,cycleCoins:0,allCoins:0,totalClicks:0,gens:[],ups:{},pt:0,ptTotal:0,pshop:{},rt:0,rtTotal:0,rshop:{},prestiges:0,rebirths:0,ach:{},coinSkin:{owned:{gold:1},active:'gold'},charSkins:[],buff:{until:0,mult:1},t:now||0,airdrops:0,autoAcc:0,name:'Hero',sound:false,music:true,musicVol:.5,quality:'high',hype:0,fx:{frenzy:0,overdrive:0,lucky:0},cd:{frenzy:0,overdrive:0,storm:0,lucky:0},maxTier:0,crits:0,abilUsed:0,hypeMax:0};for(var i=0;i<GEN.length;i++){S.gens.push({n:0,mgr:false,prog:0,run:false});S.charSkins.push({owned:{default:1},active:'default'})}return S}
function lvl(S,id){return (SHOPBY[id].cur==='pt'?S.pshop:S.rshop)[id]||0}
function achCount(S){var c=0;for(var k in S.ach)if(S.ach[k])c++;return c}
function tierMult(S){return 1+.03*tierOf(S.runCoins)}
function ptMult(S){return 1+.02*S.ptTotal*(1+.2*lvl(S,'p_boost'))}
function rtMult(S){return 1+.5*S.rtTotal*(1+.5*lvl(S,'r_mult')*0)+.5*lvl(S,'r_mult')}
function globalMult(S){var m=(1+.02*achCount(S))*tierMult(S)*ptMult(S)*rtMult(S);UPS.forEach(function(u){if(u.kind==='global'&&S.ups[u.id])m*=u.mult});return m}
function buffMult(S,now){return S.buff.until>now?S.buff.mult:1}
function milestoneMult(n){var c=0;for(var i=0;i<MILESTONES.length;i++)if(n>=MILESTONES[i])c++;return Math.pow(2,c)}
function discount(S){return Math.min(.6,.03*lvl(S,'p_disc'))}
function genCost(S,i,k){var g=GEN[i],n=S.gens[i].n;if(k<1)return 0;return Math.min(ENDCAP,g.cost*Math.pow(g.coef,n)*(Math.pow(g.coef,k)-1)/(g.coef-1)*(1-discount(S)))}
function maxBuy(S,i){var g=GEN[i],n=S.gens[i].n,base=g.cost*Math.pow(g.coef,n)*(1-discount(S));if(S.coins<base)return 0;var k=Math.floor(Math.log(1+S.coins*(g.coef-1)/base)/Math.log(g.coef)+1e-9);while(k>0&&genCost(S,i,k)>S.coins)k--;while(genCost(S,i,k+1)<=S.coins&&k<1e5)k++;return Math.max(0,k)}
function mgrCost(S,i){return GEN[i].mgr*(1-.25*lvl(S,'r_mgr'))*(1-discount(S))}
function upCount(S,kind){var c=0,a=UPK[kind];for(var k=0;k<a.length;k++)if(S.ups[a[k]])c++;return c}
function speedMult(S){return Math.pow(1.1,lvl(S,'p_speed'))*Math.pow(1.1,upCount(S,'speed'))}
function nowS(n){return n==null?Date.now()/1000:n}
function fxOn(S,id,now){return S.fx[id]>nowS(now)}
function abLvl(S,id){return lvl(S,'a_'+id)}
function hypeSpeed(S){return 1+.5*S.hype/100}
function crewBoost(S,now){return hypeSpeed(S)*(fxOn(S,'overdrive',now)?2+.25*abLvl(S,'overdrive'):1)}
function genSpeed(S,i){return (1+Math.min(1,Math.max(0,S.gens[i].n-1)/250))*Math.pow(1.1,genUpCount(S,i))}
function cycleTime(S,i,now){return GEN[i].time/(speedMult(S)*genSpeed(S,i)*crewBoost(S,now))}
function genUpCount(S,i){var c=0,a=UPGEN[i];for(var k=0;k<a.length;k++)if(S.ups[a[k]])c++;return c}
function genMult(S,i){return milestoneMult(S.gens[i].n)*Math.pow(3,genUpCount(S,i))}
function payout(S,i,now){return Math.min(ENDCAP,S.gens[i].n*GEN[i].rev*genMult(S,i)*globalMult(S)*buffMult(S,now||0))}
function genRate(S,i,now){return S.gens[i].n>0?payout(S,i,now)/cycleTime(S,i,now):0}
function cps(S,now){var s=0;for(var i=0;i<GEN.length;i++)if(S.gens[i].mgr)s+=genRate(S,i,now);return s}
function clickMult(S){var m=Math.pow(2,lvl(S,'p_click'))*Math.pow(3,lvl(S,'r_click'));UPS.forEach(function(u){if(u.kind==='click'&&S.ups[u.id])m*=2});return m}
function clickPct(S){var p=0;UPS.forEach(function(u){if(u.kind==='clickpct'&&S.ups[u.id])p+=u.pct});return p}
function hypeClick(S){return 1+1.5*S.hype/100}
function frenzyMult(S,now){return fxOn(S,'frenzy',now)?7+abLvl(S,'frenzy'):1}
function critChance(S,now){var c=.05*upCount(S,'crit');if(fxOn(S,'lucky',now))c=1;return Math.min(1,c)}
function critMult(S){return 10+5*upCount(S,'critmult')}
function clickValue(S,now){return Math.min(ENDCAP,clickMult(S)*globalMult(S)*buffMult(S,now||0)*frenzyMult(S,now)*hypeClick(S)+clickPct(S)*cps(S,now))}
function earn(S,v){if(!(v>0))return;S.coins=Math.min(ENDCAP,S.coins+v);S.runCoins=Math.min(ENDCAP,S.runCoins+v);while(S.maxTier+1<TIER_AT.length&&S.runCoins>=TIER_AT[S.maxTier+1])S.maxTier++;S.cycleCoins=Math.min(ENDCAP,S.cycleCoins+v);S.allCoins=Math.min(ENDCAP,S.allCoins+v)}
function mine(S,now,rnd){var v=clickValue(S,now),cc=critChance(S,now);S.lastCrit=false;if(cc>0&&(rnd||Math.random)()<cc){v=Math.min(ENDCAP,v*critMult(S));S.lastCrit=true;S.crits++}earn(S,v);S.totalClicks++;return v}
function addHype(S,n){S.hype=Math.min(100,S.hype+(n==null?6:n));if(S.hype>S.hypeMax)S.hypeMax=S.hype}
function buyGen(S,i,k){if(i<0||i>=GEN.length||!(k>=1))return 0;k=Math.floor(k);var c=genCost(S,i,k);if(S.coins<c||c<=0)return 0;S.coins-=c;S.gens[i].n+=k;return k}
function buyGenMax(S,i){var k=maxBuy(S,i);return k>0?buyGen(S,i,k):0}
function hireMgr(S,i){if(i<0||i>=GEN.length||S.gens[i].mgr||S.gens[i].n<1)return false;var c=mgrCost(S,i);if(S.coins<c)return false;S.coins-=c;S.gens[i].mgr=true;S.gens[i].run=true;return true}
function runGen(S,i){var g=S.gens[i];if(!g||g.n<1||g.mgr||g.run)return false;g.run=true;g.prog=0;return true}
function upAvailable(S,u){return !S.ups[u.id]&&(u.kind!=='gen'||S.gens[u.gen].n>=u.need)}
function buyUp(S,id){var u=UPBY[id];if(!u||!upAvailable(S,u)||S.coins<u.cost*(1-discount(S)))return false;S.coins-=u.cost*(1-discount(S));S.ups[id]=1;return true}
function upCost(S,u){return u.cost*(1-discount(S))}
// ---- time passes: cycles finish and pay out
var LAST={paid:[]};
function tick(S,dt,now){LAST.paid=[];if(!(dt>0))return 0;var gained=0,i,g,T,pr,done;now=now||0;S.hype=Math.max(0,S.hype-18*dt);
 var ac=lvl(S,'p_auto')*2;if(ac>0){S.autoAcc+=ac*dt;var n=Math.floor(S.autoAcc);if(n>0){S.autoAcc-=n;for(i=0;i<Math.min(n,50);i++)gained+=mine(S,now)}}
 for(i=0;i<GEN.length;i++){g=S.gens[i];if(g.n<1||!g.run)continue;T=cycleTime(S,i,now);g.prog+=dt/T;if(g.prog>=1){done=Math.floor(g.prog);pr=payout(S,i,now);LAST.paid.push(i);if(g.mgr){g.prog-=done;earn(S,pr*done);gained+=pr*done}else{g.prog=0;g.run=false;earn(S,pr);gained+=pr}}}
 return gained}
function offlineRate(S){return .25+.2*lvl(S,'p_off')}
function offlineCap(S){return (8+4*lvl(S,'r_cap'))*3600}
function offline(S,seconds){seconds=Math.min(Math.max(0,seconds),offlineCap(S));if(seconds<1)return 0;S.hype=0;var g=cps(S,0)*seconds*offlineRate(S);earn(S,g);for(var i=0;i<GEN.length;i++)if(S.gens[i].mgr)S.gens[i].prog=0;return g}
// ---- prestige and rebirth
function prestigeTotal(S){return Math.floor(Math.sqrt(S.cycleCoins/1e7))}
function prestigeGain(S){return Math.max(0,prestigeTotal(S)-S.ptTotal)}
function startKit(S){var L=Math.min(GEN.length,lvl(S,'p_start'));for(var i=0;i<L;i++){S.gens[i].n=1;S.gens[i].mgr=true;S.gens[i].run=true}}
function doPrestige(S){var g=prestigeGain(S);if(g<1)return 0;S.pt+=g;S.ptTotal+=g;S.prestiges++;S.coins=0;S.runCoins=0;S.ups={};S.buff={until:0,mult:1};S.autoAcc=0;for(var i=0;i<GEN.length;i++)S.gens[i]={n:0,mgr:false,prog:0,run:false};startKit(S);return g}
function canRebirth(S){return S.ptTotal>=100}
function rebirthGain(S){return canRebirth(S)?Math.max(1,Math.floor(Math.sqrt(S.ptTotal/25))):0}
function doRebirth(S){if(!canRebirth(S))return 0;var g=rebirthGain(S),keep=Math.min(.5,.1*lvl(S,'r_keep')),kept=Math.floor(S.ptTotal*keep),head=5*lvl(S,'r_head');S.rt+=g;S.rtTotal+=g;S.rebirths++;S.pshop={};S.pt=kept+head;S.ptTotal=kept+head;S.cycleCoins=0;S.coins=0;S.runCoins=0;S.ups={};S.buff={until:0,mult:1};S.autoAcc=0;for(var i=0;i<GEN.length;i++)S.gens[i]={n:0,mgr:false,prog:0,run:false};return g}
// ---- shops
function shopCost(S,id){var s=SHOPBY[id],l=lvl(S,id);return Math.ceil(s.lin?s.base+l:s.base*Math.pow(s.grow,l))}
function buyShop(S,id){var s=SHOPBY[id];if(!s)return false;var l=lvl(S,id);if(l>=s.max)return false;var c=shopCost(S,id),cur=s.cur;if(S[cur]<c)return false;S[cur]-=c;(cur==='pt'?S.pshop:S.rshop)[id]=l+1;if(id==='p_start'&&S.runCoins===0&&S.gens.every(function(g){return g.n===0}))startKit(S);return true}
// ---- skins
function skinCost(kind,id){var l=(kind==='coin'?COIN_SKINS:CHAR_SKINS).filter(function(s){return s.id===id})[0];return l||null}
function buySkin(S,kind,id,idx){var sk=skinCost(kind,id);if(!sk)return false;var box=kind==='coin'?S.coinSkin:S.charSkins[idx];if(!box||box.owned[id])return false;if(sk.cur!=='free'){if(S[sk.cur]<sk.cost)return false;S[sk.cur]-=sk.cost}box.owned[id]=1;return true}
function setSkin(S,kind,id,idx){var box=kind==='coin'?S.coinSkin:S.charSkins[idx];if(!box||!box.owned[id])return false;box.active=id;return true}
// ---- abilities
function abilityUnlocked(S,a){return S.maxTier>=a.tier}
function abilityCd(S,a){return a.cd*(1-.05*abLvl(S,a.id))}
function abilityDur(S,a){return a.dur>0?a.dur+abLvl(S,a.id):0}
function abilityLeft(S,a,now){return Math.max(0,S.cd[a.id]-nowS(now))}
function useAbility(S,id,now){var a=ABBY[id];now=nowS(now);if(!a||!abilityUnlocked(S,a)||S.cd[id]>now)return null;S.cd[id]=now+abilityCd(S,a);S.abilUsed++;if(id==='storm'){var v=Math.max(cps(S,now)*120*(1+.25*abLvl(S,'storm')),clickValue(S,now)*60);earn(S,v);return {id:id,amount:v}}S.fx[id]=now+abilityDur(S,a);return {id:id,seconds:abilityDur(S,a)}}
// ---- airdrops and achievements
function airdropGap(S,rnd){return (60+120*rnd())/(1+.25*lvl(S,'p_air'))}
function claimAirdrop(S,now,rnd){S.airdrops++;if(rnd()<.5){var v=Math.max(clickValue(S,now)*30,cps(S,now)*60*(1+.2*lvl(S,'p_air')));earn(S,v);return {type:'coins',amount:v}}S.buff={until:now+30+5*lvl(S,'p_air'),mult:7};return {type:'buff',seconds:30+5*lvl(S,'p_air')}}
function checkAch(S){var out=[];ACH.forEach(function(a){if(!S.ach[a[0]]&&a[3](S)){S.ach[a[0]]=1;out.push(a)}});return out}
// ---- saving, loading and sharing
function serialize(S){return JSON.stringify(S)}
function sanitize(r,now){var S=newGame(now),i,k;if(!r||typeof r!=='object')return S;
 ['coins','runCoins','cycleCoins','allCoins','pt','ptTotal','rt','rtTotal'].forEach(function(f){S[f]=nz(r[f],0,0,ENDCAP)});
 S.totalClicks=Math.floor(nz(r.totalClicks,0,0,1e12));S.prestiges=Math.floor(nz(r.prestiges,0,0,1e6));S.rebirths=Math.floor(nz(r.rebirths,0,0,1e6));S.airdrops=Math.floor(nz(r.airdrops,0,0,1e9));
 if(Array.isArray(r.gens))for(i=0;i<GEN.length;i++){var g=r.gens[i];if(g&&typeof g==='object')S.gens[i]={n:Math.floor(nz(g.n,0,0,1e6)),mgr:!!g.mgr,prog:nz(g.prog,0,0,1e6),run:!!g.run||!!g.mgr}}
 if(r.ups&&typeof r.ups==='object')for(k in r.ups)if(UPBY[k]&&r.ups[k])S.ups[k]=1;
 [[r.pshop,S.pshop,'pt'],[r.rshop,S.rshop,'rt']].forEach(function(p){if(p[0]&&typeof p[0]==='object')for(var id in p[0])if(SHOPBY[id]&&SHOPBY[id].cur===p[2]){var l=Math.floor(nz(p[0][id],0,0,SHOPBY[id].max));if(l>0)p[1][id]=l}});
 if(r.ach&&typeof r.ach==='object')ACH.forEach(function(a){if(r.ach[a[0]])S.ach[a[0]]=1});
 function skinBox(src,list,box){if(!src||typeof src!=='object')return;var own=src.owned&&typeof src.owned==='object'?src.owned:{};list.forEach(function(s){if(own[s.id]||s.cur==='free')box.owned[s.id]=1});if(box.owned[src.active])box.active=src.active}
 skinBox(r.coinSkin,COIN_SKINS,S.coinSkin);if(Array.isArray(r.charSkins))for(i=0;i<GEN.length;i++)skinBox(r.charSkins[i],CHAR_SKINS,S.charSkins[i]);
 if(r.buff&&typeof r.buff==='object')S.buff={until:nz(r.buff.until,0,0,1e15),mult:nz(r.buff.mult,1,1,100)};
 if(r.fx&&typeof r.fx==='object')['frenzy','overdrive','lucky'].forEach(function(k){S.fx[k]=nz(r.fx[k],0,0,1e15)});if(r.cd&&typeof r.cd==='object')['frenzy','overdrive','storm','lucky'].forEach(function(k){S.cd[k]=nz(r.cd[k],0,0,1e15)});S.hype=nz(r.hype,0,0,100);S.maxTier=Math.floor(nz(r.maxTier,0,0,TIER_AT.length-1));S.crits=Math.floor(nz(r.crits,0,0,1e12));S.abilUsed=Math.floor(nz(r.abilUsed,0,0,1e12));S.hypeMax=nz(r.hypeMax,0,0,100);S.music=r.music!==false;S.musicVol=nz(r.musicVol,.5,0,1);S.t=nz(r.t,now||0,0,1e15);S.autoAcc=nz(r.autoAcc,0,0,1e3);S.name=typeof r.name==='string'&&/^[A-Za-z0-9 _-]{1,16}$/.test(r.name)?r.name:'Hero';S.sound=!!r.sound;S.quality=r.quality==='low'?'low':'high';return S}
function deserialize(txt,now){var r=null;try{r=JSON.parse(txt)}catch(e){}return sanitize(r,now)}
function hash32(s){var x=2166136261;for(var i=0;i<s.length;i++){x^=s.charCodeAt(i);x=Math.imul(x,16777619)}return (x>>>0).toString(16)}
function exportCode(S){var j=serialize(S);return btoa(unescape(encodeURIComponent(j)))+'.'+hash32(j)}
function importCode(code,now){try{var p=String(code).trim().split('.');if(p.length!==2)return null;var j=decodeURIComponent(escape(atob(p[0])));if(hash32(j)!==p[1])return null;var r=JSON.parse(j);if(!r||typeof r!=='object')return null;return sanitize(r,now)}catch(e){return null}}
if(typeof module!=='undefined')module.exports={ABIL:ABIL,TICKERS:TICKERS,GEN:GEN,UPS:UPS,PSHOP:PSHOP,RSHOP:RSHOP,COINS:COINS,TIER_AT:TIER_AT,MILESTONES:MILESTONES,ACH:ACH,COIN_SKINS:COIN_SKINS,CHAR_SKINS:CHAR_SKINS};
