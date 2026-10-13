import os,sys,re
HERE=os.path.dirname(os.path.abspath(__file__))
def rd(n):return open(os.path.join(HERE,n),encoding='utf-8').read()
out=sys.argv[1] if len(sys.argv)>1 else os.path.join(HERE,'..','public','index.html') if os.path.isdir(os.path.join(HERE,'..','public')) else os.path.join(HERE,'hodl-heroes.html')
head=rd('head.html')
js='\n'.join(rd(f) for f in ['game.js','icons.js','engine.js','chars.js','bg.js','music.js','scene.js','ui.js'])
assert '</script' not in js
html=head+'<script>\n'+js+'\nHH.boot();\n</script>\n</body></html>\n'
open(out,'w',encoding='utf-8').write(html);print('built',len(html),'bytes ->',out)
