from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math,textwrap,os
R=Path(__file__).resolve().parents[1];A=R/'assets';A.mkdir(exist_ok=True)
P=Path(os.environ.get('PORTFOLIO_SOURCE','../sohaib-engineering-portfolio')).resolve()/'public/previews'
F=Path(os.environ.get('PROFILE_FONT_DIR',str(Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts')))
def font(n,b=False,serif=False):return ImageFont.truetype(str(F/('georgiai.ttf' if serif else 'arialbd.ttf' if b else 'arial.ttf')),n)
themes={'dark':{'bg':'#111811','panel':'#1b251b','ink':'#eeeede','muted':'#aab7a0','line':'#3f5136','accent':'#d5f477'},'light':{'bg':'#f3f0e6','panel':'#e6e9d9','ink':'#24311d','muted':'#59664c','line':'#bdc9ac','accent':'#4c6731'}}
def text(d,x,y,s,n=20,fill='#eeeede',b=False,serif=False):d.text((x,y),s,font=font(n,b,serif),fill=fill)
roles=['Building useful software.','Exploring machine learning.','Documenting the engineering.']
for name,c in themes.items():
 frames=[]
 for frame in range(120):
  im=Image.new('RGB',(1280,360),c['bg']);d=ImageDraw.Draw(im);d.line((48,52,1232,52),fill=c['line']);d.line((48,309,1232,309),fill=c['line']);text(d,49,26,'SOHAIB IJAZ / ENGINEERING & CURIOSITY',13,c['accent']);text(d,48,76,'Curiosity.',75,c['ink'],b=True);text(d,48,151,'Made useful.',75,c['accent'],serif=True)
  which=frame//40;t=frame%40;phrase=roles[which];count=min(len(phrase),max(0,int((t-1)*len(phrase)/14))) if t<30 else max(0,len(phrase)-int((t-30)*len(phrase)/9))
  text(d,51,258,phrase[:count],23,c['muted']);
  if t<30:
   box=d.textbbox((0,0),phrase[:count],font=font(23));x=51+box[2];d.line((x+7,259,x+7,282),fill=c['accent'],width=2)
  cx,cy=1088,174;r=70;d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=c['line'],width=2)
  for k in range(8):
   a=k*math.pi/4+frame/120*math.pi/4;d.line((cx+math.cos(a)*18,cy+math.sin(a)*18,cx+math.cos(a)*90,cy+math.sin(a)*90),fill=c['accent'],width=2)
  text(d,49,329,'BUILD / VERIFY / DOCUMENT / ITERATE',12,c['muted']);text(d,1005,329,'LAHORE, PAKISTAN',12,c['muted']);frames.append(im)
 # Static counterpart always has a complete role line, never a half-typed phrase.
 static=frames[20].copy();static.save(A/f'header-{name}-static.png',optimize=True)
 palette=static.quantize(colors=80);frames=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
 frames[0].save(A/f'header-{name}.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=True,disposal=1)
 projects=[('trustmart','TrustMart','A clearer electronics marketplace.','Supplier records, comparable sample prices and disclosures.','REACT / TYPESCRIPT / FLASK'),('travel','Travel Estimator','Make the whole budget visible.','Explained costs, provider quotes and private group planning.','NEXT.JS / TYPESCRIPT / SQLITE'),('careindex','CareIndex','One slot. One correct outcome.','Synthetic clinic workflows, transactions and a visible AVL lab.','NEXT.JS / SQLITE / ALGORITHMS'),('word-search','Word Search Studio','Classic logic. A playable browser.','Seeded puzzles, achievable targets and step-by-step search.','REACT / TYPESCRIPT / C++ ROOTS')]
 for i,(id,title,line,detail,stack) in enumerate(projects):
  im=Image.new('RGB',(760,570),c['bg']);d=ImageDraw.Draw(im);d.rounded_rectangle((1,1,758,568),radius=15,outline=c['line'],width=2);text(d,26,22,f'0{i+1} / PROJECT STUDY',14,c['accent']);text(d,655,20,'SOURCE /',13,c['muted'])
  shot=Image.open(P/f'{id}.webp').convert('RGB');shot.thumbnail((704,320));canvas=Image.new('RGB',(704,285),'#131912');canvas.paste(shot,((704-shot.width)//2,0));im.paste(canvas,(28,60));d=ImageDraw.Draw(im)
  text(d,28,365,title,34,c['ink'],b=True);text(d,29,410,line,23,c['accent']);
  for j,s in enumerate(textwrap.wrap(detail,57)):text(d,29,449+j*26,s,21,c['muted'])
  d.line((28,518,730,518),fill=c['line']);text(d,29,536,stack,13,c['muted']);text(d,651,530,'VIEW >',16,c['accent']);im.save(A/f'project-{id}-{name}.png',optimize=True)
 # Evidence is verifiable project scope; dynamic activity statistics are separate.
 im=Image.new('RGB',(1280,140),c['panel']);d=ImageDraw.Draw(im)
 for i,(num,label) in enumerate([('04','WORKING PROJECT DEMOS'),('06','ILLUSTRATED STORIES'),('04','CAPTIONED EXPLAINERS')]):
  x=38+i*420;text(d,x,25,num,48,c['accent'],b=True);text(d,x+95,55,label,13,c['muted']);
  if i<2:d.line((x+365,27,x+365,113),fill=c['line'])
 im.save(A/f'evidence-{name}.png',optimize=True)
 groups=[('BUILDING WITH',[('TS','TypeScript'),('R','React / Next.js'),('PY','Python / Flask'),('SQL','SQLite / SQL'),('C++','C++'),('GIT','Git')]),('CURRENTLY LEARNING',[('ML','Machine learning'),('CV','Computer vision'),('NLP','Language systems'),('EVAL','Model evaluation')])]
 im=Image.new('RGB',(1280,300),c['bg']);d=ImageDraw.Draw(im)
 for row,(title,items) in enumerate(groups):
  y=20+row*140;text(d,20,y,title,13,c['accent']);
  for i,(abbr,label) in enumerate(items):
   x=20+i*(205 if row==0 else 305);d.rounded_rectangle((x,y+35,x+(192 if row==0 else 292),y+109),radius=9,fill=c['panel'],outline=c['line']);text(d,x+12,y+49,abbr,15,c['accent'],b=True);text(d,x+12,y+77,label,16,c['ink'])
 im.save(A/f'skills-{name}.png',optimize=True)
print('Rendered dark/light animated headers, eight project cards, skills and evidence strips.')
