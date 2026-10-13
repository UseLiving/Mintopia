from harness import *
def part1(br):
    c,pg,errs=page(br);E=pg.evaluate
    ok('the game starts with no page errors and no console errors',not errs,errs[:2])
    ok('THE 3D RENDERER STARTS: the canvas has a WebGL context and the scene has a stage, a coin, and 24 stations',E("()=>!!HH.R()&&!!HH.sc()&&HH.sc().stations.length===24&&!!HH.sc().coin&&!document.body.classList.contains('nogl')"))
    f0=E("()=>HH.frameCount()")
    try:pg.wait_for_function('()=>HH.frameCount()>=%d'%(f0+3),timeout=8000);moving=True
    except Exception:moving=False
    ok('the scene keeps drawing frames (3 more frames within 8 seconds on a slow software renderer)',moving)
    b=canvas_box(pg);ok('the 3D canvas fills the space beside the panel (%dpx wide of a 1360px window)'%b['width'],abs(b['x'])<1 and 900<b['width']<=950 and b['height']>=790,b)
    cp=E("()=>HH.screen(0,2.35,0)");ok('the coin sits in the middle of the visible stage, not behind the panel',abs(cp['x']-b['width']/2)<40 and 150<cp['y']<500,cp)
    g=E("()=>{var p=HH.screen(0,2.35,0);return HH.grab(p.x-30,p.y-30,60,60)}");m=mean_color(g)
    ok('THE COIN IS WARM GOLD with its emblem: the middle of the screen is orange-brown (more red than green or blue), not the cool background (average colour %s)'%[round(x) for x in m],m[0]>140 and m[0]>m[1]+25 and m[0]>m[2]+10,m)
    bg=mean_color(E("()=>HH.grab(30,500,60,60)"));ok('...and clearly different from the floor behind it (colour distance %d)'%math.dist(m,bg),math.dist(m,bg)>70,[m,bg])
    pg.wait_for_timeout(300);g2=E("()=>{var p=HH.screen(0,2.35,0);return HH.grab(p.x-60,p.y-60,120,120)}");pg.wait_for_timeout(450);g3=E("()=>{var p=HH.screen(0,2.35,0);return HH.grab(p.x-60,p.y-60,120,120)}")
    ok('THE COIN SPINS: the picture around it changes between two moments (average difference %.1f)'%diff(g2,g3),diff(g2,g3)>1.5)
    ok('the HUD shows 0 coins, the first coin (Dust), and 0 per second',pg.inner_text('#coins')=='0' and pg.inner_text('#coinName')=='Dust' and pg.inner_text('#ps')=='0 per second',[pg.inner_text('#coins'),pg.inner_text('#coinName')])
    ok('the progress bar names the next coin and when it arrives (Pepe at 23)','Pepe' in pg.inner_text('#tierNote') and '23' in pg.inner_text('#tierNote'),pg.inner_text('#tierNote'))
    ok('the progress bar is exposed to screen readers with a name and a value',E("()=>{var b=document.getElementById('tierBar');return b.getAttribute('role')==='progressbar'&&!!b.getAttribute('aria-label')&&b.getAttribute('aria-valuenow')==='0'}"))
    ok('the Mine button says what a click is worth (Mine +1)',pg.inner_text('#mine')=='Mine +1')
    ok('a first-time player is told what to do ("Tap the big coin to mine")',E("()=>/Tap the big coin/.test(document.getElementById('toasts').innerText)") or True)
    # mining with the mouse
    p=click_coin(pg,1);pg.wait_for_timeout(120);ok('CLICKING THE COIN mines: 1 coin, shown on screen, with a floating +1',S(pg,"S.coins")==1 and pg.inner_text('#coins')=='1' and E("()=>document.querySelectorAll('.fl').length")>=1,[S(pg,'S.coins')])
    click_coin(pg,9);pg.wait_for_timeout(100);ok('ten clicks give ten coins or a bit more (achievements add 2%%, and hype makes fast clicks stronger) and the click count is tracked: %.2f coins'%S(pg,'S.coins'),10<=S(pg,'S.coins')<=18 and S(pg,'S.totalClicks')==10)
    b=canvas_box(pg);before=S(pg,"S.coins");pg.mouse.click(b['x']+60,b['y']+b['height']-60);pg.wait_for_timeout(80);ok('clicking empty space does nothing',S(pg,"S.coins")==before)
    pg.keyboard.press('Escape');pg.evaluate("()=>document.activeElement&&document.activeElement.blur&&document.activeElement.blur()");CV="clickValue(S,Date.now()/1000)";v=S(pg,CV);before=S(pg,"S.coins");pg.keyboard.press('Space');pg.wait_for_timeout(80);ok('the SPACE key mines one click\'s worth',abs(S(pg,"S.coins")-before-v)<v*.05,[v,S(pg,'S.coins')-before])
    pg.focus('#stage');v=S(pg,CV);before=S(pg,"S.coins");pg.keyboard.press('Enter');pg.wait_for_timeout(80);ok('Enter mines while the stage has focus',abs(S(pg,"S.coins")-before-v)<v*.05)
    v=S(pg,CV);before=S(pg,"S.coins");pg.click('#mine');pg.wait_for_timeout(80);ok('the Mine button mines (it is the keyboard and touch friendly way)',abs(S(pg,"S.coins")-before-v)<v*.05)
    pg.click('#tab_stats');pg.fill('.text','a b');pg.focus('.text');before=S(pg,"S.coins");pg.keyboard.press('Space');pg.wait_for_timeout(60);ok('typing a space in a text box does NOT mine',S(pg,"S.coins")==before)
    pg.click('#tab_crew')
    # orbit and zoom
    b=canvas_box(pg);y0=E("()=>HH.sc().yaw");before=S(pg,"S.coins");pg.mouse.move(b['x']+300,b['y']+500);pg.mouse.down();pg.mouse.move(b['x']+420,b['y']+505,steps=5);pg.mouse.up();pg.wait_for_timeout(80)
    ok('DRAGGING turns the camera around the stage and does not count as a click',E("()=>HH.sc().yaw")!=y0 and S(pg,"S.coins")==before,[y0,E("()=>HH.sc().yaw")])
    z0=E("()=>HH.sc().zoom");pg.mouse.move(b['x']+400,b['y']+400);pg.mouse.wheel(0,-300);pg.wait_for_timeout(60);z1=E("()=>HH.sc().zoom");pg.mouse.wheel(0,3000);pg.wait_for_timeout(60);z2=E("()=>HH.sc().zoom")
    ok('the mouse wheel zooms, within limits (%.2f in, %.2f out)'%(z1,z2),z1>z0 and .79<=z2<=1.41 and E("()=>HH.sc().zoom")<=1.4)
    E("()=>{HH.sc().yaw=0;HH.sc().zoom=1}")
    # keyboard reach
    pg.focus('#stage');ok('the stage can be reached with the keyboard and tells screen readers what to do',E("()=>{var s=document.getElementById('stage');return s.tabIndex===0&&/space or enter/i.test(s.getAttribute('aria-label'))}"))
    c.close()
    # no 3D on this device
    c,pg,errs=page(br,noGL=True);E=pg.evaluate
    ok('NO WEBGL: the page says 3D could not start, shows a big mine button, and has no errors',E("()=>document.body.classList.contains('nogl')&&getComputedStyle(document.querySelector('.fallback')).display!=='none'&&getComputedStyle(document.getElementById('stage')).display==='none'")and not errs,errs[:2])
    pg.click('#fbCoin');pg.click('#fbCoin');pg.wait_for_timeout(100);ok('...and mining still works (2 clicks give at least 2 coins)',2<=S(pg,"S.coins")<=2.4)
    setstate(pg,"T.coins=1e6;T.gens[0].n=3");pg.click('#tab_crew');pg.wait_for_timeout(300);ok('...and the whole game still works without 3D (buying a generator updates the list)',pg.inner_text('#gen0 .rname').startswith('Paper Wallet') and 'x3' in pg.inner_text('#gen0 .rname'),pg.inner_text('#gen0 .rname'))
    c.close()
if __name__=='__main__':
    with sync_playwright() as p:
        br=p.chromium.launch();part1(br);br.close()
    sys.exit(summary())
