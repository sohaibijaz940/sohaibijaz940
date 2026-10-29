"""Render honest profile metrics and reduced-motion calendars from GitHub's API."""
from datetime import datetime,timedelta,timezone,date
from pathlib import Path
from html import escape
import json,os,urllib.request

PALETTES={'dark':{'bg':'#111811','ink':'#eeeede','muted':'#aab7a0','accent':'#d5f477','line':'#3f5136','dots':['#202b20','#465b30','#708e43','#a0bd59','#d5f477']},'light':{'bg':'#f3f0e6','ink':'#24311d','muted':'#59664c','accent':'#4c6731','line':'#bdc9ac','dots':['#e2e7d8','#c6d5a6','#9fbf78','#739c4e','#4c6731']}}
def streaks(days,today):
 counts={d['date']:d['contributionCount'] for d in days if d['date']<=today.isoformat()};anchor=today if counts.get(today.isoformat(),0)>0 else today-timedelta(days=1);current=0;cursor=anchor
 while counts.get(cursor.isoformat(),0)>0:current+=1;cursor-=timedelta(days=1)
 longest=run=0;previous=None
 for day,count in sorted(counts.items()):
  current_date=date.fromisoformat(day)
  run=(run+1 if previous and current_date-previous==timedelta(days=1) else 1) if count>0 else 0
  longest=max(longest,run);previous=current_date
 return current,longest,anchor.isoformat() if current else None
def text(x,y,value,size,color,weight='400'):
 return f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial,sans-serif" font-size="{size}" font-weight="{weight}">{escape(str(value))}</text>'
def render(calendar,updated,owner,out):
 out.mkdir(parents=True,exist_ok=True);days=[d for w in calendar['weeks'] for d in w['contributionDays']];today=datetime.fromisoformat(updated).astimezone(timezone(timedelta(hours=5))).date();current,longest,through=streaks(days,today)
 metrics={'owner':owner,'source':'GitHub GraphQL contributionCalendar','window':'Last 12 months as reported by GitHub','updatedAt':updated,'totalContributions':calendar['totalContributions'],'currentStreakDays':current,'longestStreakDays':longest,'currentStreakThrough':through}
 (out/'activity.json').write_text(json.dumps(metrics,indent=2)+'\n',encoding='utf-8')
 levels=['NONE','FIRST_QUARTILE','SECOND_QUARTILE','THIRD_QUARTILE','FOURTH_QUARTILE']
 for theme,c in PALETTES.items():
  body=f'<rect width="1200" height="216" rx="12" fill="{c["bg"]}" stroke="{c["line"]}"/>'
  for i,(number,label,note) in enumerate([(calendar['totalContributions'],'CONTRIBUTIONS','Last 12 months'),(current,'CURRENT RUN',f'Through {through}' if through else 'No ongoing run'),(longest,'LONGEST RUN','Within this calendar window')]):
   x=34+i*400;body+=text(x,73,number,48,c['accent'],'600')+text(x,111,label,13,c['ink'],'600')+text(x,142,note,12,c['muted'])
   if i<2:body+=f'<path d="M{x+342} 30v123" stroke="{c["line"]}"/>'
  body+=text(34,190,'GITHUB CALENDAR / UPDATED '+updated[:10]+' / STREAK MAY CONTINUE THROUGH YESTERDAY',10,c['muted'])
  (out/f'activity-{theme}.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 216" role="img"><title>Actual GitHub contribution activity, last twelve months</title>'+body+'</svg>',encoding='utf-8')
  width=max(880,len(calendar['weeks'])*16+32);body=f'<rect width="{width}" height="164" fill="{c["bg"]}"/>'
  for column,week in enumerate(calendar['weeks']):
   for row,d in enumerate(week['contributionDays']):
    level=levels.index(d['contributionLevel']);x=16+column*16;y=18+row*16
    body+=f'<rect x="{x}" y="{y}" width="12" height="12" rx="2" fill="{c["dots"][level]}"><title>{escape(d["date"])}: {d["contributionCount"]} contributions</title></rect>'
  body+=text(16,153,'STATIC GITHUB CALENDAR / '+updated[:10],10,c['muted'])
  (out/f'calendar-{theme}-static.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 164" role="img"><title>Static contribution calendar for reduced motion</title>'+body+'</svg>',encoding='utf-8')
 return metrics
def main():
 owner=os.environ['GITHUB_REPOSITORY_OWNER'];token=os.environ['GITHUB_TOKEN'];now=datetime.now(timezone.utc);start=now-timedelta(days=365)
 query='query($owner:String!,$from:DateTime!,$to:DateTime!){user(login:$owner){contributionsCollection(from:$from,to:$to){contributionCalendar{totalContributions weeks{contributionDays{date contributionCount contributionLevel}}}}}}'
 payload=json.dumps({'query':query,'variables':{'owner':owner,'from':start.isoformat(),'to':now.isoformat()}}).encode()
 request=urllib.request.Request('https://api.github.com/graphql',data=payload,headers={'Authorization':'Bearer '+token,'User-Agent':'sohaib-profile-activity','Content-Type':'application/json'})
 with urllib.request.urlopen(request,timeout=45) as response:data=json.load(response)
 if data.get('errors') or not data.get('data',{}).get('user'):raise RuntimeError('GitHub did not return a usable contribution calendar; refusing to invent statistics.')
 calendar=data['data']['user']['contributionsCollection']['contributionCalendar']
 if not calendar['weeks']:raise RuntimeError('Empty calendar response; keeping existing artwork.')
 result=render(calendar,now.isoformat(),owner,Path('generated'));print(f"Rendered actual calendar for {owner}: {result['totalContributions']} contributions in the reported window.")
if __name__=='__main__':main()
