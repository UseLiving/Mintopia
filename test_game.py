import sys,os,time,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from harness import *
import harness
from t1 import part1
from t2 import part2
from t3 import part3
from t4 import part4
from t5 import part5
from t6 import part6
if __name__=='__main__':
    t0=time.time()
    r=subprocess.run(['node',os.path.join(HERE,'unit.js')],capture_output=True,text=True,timeout=120);m=re.search(r'UNIT: (\d+)/(\d+) passed',r.stdout)
    ok('THE GAME RULES pass their own checks (%s): costs, cycles, managers, coins, prestige, rebirth, shops, skins, saves, offline, balance'%(m.group(0) if m else r.stdout[-100:]),r.returncode==0 and m and m.group(1)==m.group(2) and int(m.group(2))>=110,r.stdout[-200:])
    with sync_playwright() as p:
        br=p.chromium.launch()
        for name,fn in (('part1',part1),('part2',part2),('part3',part3),('part4',part4),('part5',part5),('part6',part6)):
            try:fn(br)
            except Exception as e:
                import traceback;harness.FAIL+=1;print('FAIL SECTION CRASHED:',name,'|',traceback.format_exc()[-400:].replace('\n',' / '))
        br.close()
    print('(took %.0f seconds)'%(time.time()-t0));sys.exit(summary())
