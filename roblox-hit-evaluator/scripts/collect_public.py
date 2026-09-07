#!/usr/bin/env python3
"""Read-only, one-shot Roblox / optional YouTube collection. Python 3.10+ stdlib.
This is NOT a complete gameplay researcher or a scheduler. Internet required.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime,timedelta,timezone
from pathlib import Path

UTC=timezone.utc

def now(): return datetime.now(UTC).isoformat().replace('+00:00','Z')

def write(path,obj):
    with path.open('x',encoding='utf-8',newline='\n') as f:
        json.dump(obj,f,ensure_ascii=False,indent=2); f.write('\n')

class Reader:
    def __init__(self,out:Path):
        self.out=out; self.log=[]; self.n=0
        (out/'raw').mkdir()
    def get(self,url:str,secret:str|None=None):
        self.n+=1
        safe=url
        if secret: safe=safe.replace(urllib.parse.quote(secret,safe=''),'REDACTED').replace(secret,'REDACTED')
        path=self.out/'raw'/f'{self.n:03}.json'
        entry={'url':safe,'started_at':now(),'status':'failed','artifact':str(path.relative_to(self.out))}
        for attempt in range(3):
            try:
                req=urllib.request.Request(url,headers={'User-Agent':'QiluHitEvaluator/0.1 public-data-research',
                                                        'Accept':'application/json'})
                with urllib.request.urlopen(req,timeout=20) as resp:
                    payload=resp.read(8_000_001)
                    if len(payload)>8_000_000: raise ValueError('Response exceeds 8 MB limit')
                    data=json.loads(payload.decode('utf-8'))
                    entry.update(status='success',http_status=resp.status,collected_at=now(),attempts=attempt+1)
                    entry['data_sha256']=hashlib.sha256(json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
                    write(path,{'request':entry.copy(),'data':data})
                    self.log.append(entry); time.sleep(.4); return data,entry
            except urllib.error.HTTPError as exc:
                entry['http_status']=exc.code
                entry['error']=f'HTTP {exc.code}'
                if exc.code in (429,500,502,503,504) and attempt<2:
                    retry=exc.headers.get('Retry-After','')
                    delay=min(30,max(2**(attempt+1),int(retry))) if retry.isdigit() else 2**(attempt+1)
                    time.sleep(delay); continue
                break
            except (urllib.error.URLError,TimeoutError,ValueError,OSError) as exc:
                msg=str(exc)
                if secret: msg=msg.replace(secret,'REDACTED')
                entry['error']=msg[:300]
                # DNS/offline is not fixed by endless retries.
                break
        entry['finished_at']=now(); self.log.append(entry); write(path,entry)
        return None,entry


def positive_id(value):
    s=str(value)
    if not s.isdigit() or int(s)<=0: raise ValueError('Expected a positive numeric ID')
    return s


def place_id(url):
    p=urllib.parse.urlparse(url)
    if p.scheme!='https' or p.hostname not in {'roblox.com','www.roblox.com'}:
        raise ValueError('Use a canonical HTTPS roblox.com/games/<placeId> URL, or --universe-id')
    m=re.match(r'^/games/(\d+)(?:/|$)',p.path)
    if not m: raise ValueError('No place_id in canonical game URL; resolve share links with the agent first')
    return positive_id(m.group(1))


def roblox(args, reader):
    uid=args.universe_id
    input_place=None
    if args.url:
        input_place=place_id(args.url)
        response,_=reader.get(f'https://apis.roblox.com/universes/v1/places/{input_place}/universe')
        if not response or not response.get('universeId'):
            raise ValueError('Place-to-universe lookup unavailable. Use browser verification; never treat place_id as universe_id.')
        uid=str(response['universeId'])
    uid=positive_id(uid)
    games,gsource=reader.get(f'https://games.roblox.com/v1/games?universeIds={uid}')
    items=games.get('data',[]) if isinstance(games,dict) else []
    game=next((x for x in items if str(x.get('id'))==uid),None)
    if game is None:
        raise ValueError('Game details missing / wrong universe; do not turn failure into zero players')
    favorites,fsource=reader.get(f'https://games.roblox.com/v1/games/{uid}/favorites/count')
    votes,vsource=reader.get(f'https://games.roblox.com/v1/games/votes?universeIds={uid}')
    vote_items=votes.get('data',[]) if isinstance(votes,dict) else []
    vote=next((x for x in vote_items if str(x.get('id'))==uid),{})
    fav=favorites.get('favoritesCount') if isinstance(favorites,dict) else None
    observed=gsource['collected_at']
    snapshot={'universe_id':uid,'root_place_id':str(game.get('rootPlaceId','')),
              'input_place_id':input_place,'name':game.get('name'),'creator':game.get('creator'),
              'description':game.get('description'),'created_at':game.get('created'),'updated_at':game.get('updated'),
              'playing':game.get('playing'),'visits':game.get('visits'),'favorites':fav,
              'upvotes':vote.get('upVotes'),'downvotes':vote.get('downVotes'),
              'observed_at':observed,'collected_at':now(),'source':'roblox_public_api',
              'field_observed_at':{'playing':observed,'visits':observed,
                                   'favorites':fsource.get('collected_at'),'votes':vsource.get('collected_at')},
              'raw_refs':[e['artifact'] for e in reader.log],
              'identity_status':'API_ID_RESOLVED_AGENT_MUST_CONFIRM_NAME_AND_CREATOR',
              'warning':'created_at is resource creation, not necessarily public launch; votes/favorites are not retention.'}
    write(reader.out/'snapshot.json',snapshot)
    with (reader.out/'snapshot.jsonl').open('x',encoding='utf-8') as f:
        f.write(json.dumps(snapshot,ensure_ascii=False)+'\n')
    if args.badges:
        reader.get(f'https://badges.roblox.com/v1/universes/{uid}/badges?limit=100&sortOrder=Asc')
    return {'status':'SNAPSHOT_COLLECTED','universe_id':uid,
            'missing_fields':[k for k in ('playing','visits','favorites','upvotes','downvotes') if snapshot[k] is None],
            'next':'Agent must still collect history, gameplay, updates, creators and community evidence.'}


def youtube(args,reader):
    key=os.environ.get('YOUTUBE_API_KEY')
    if not key:
        return {'status':'NOT_CONFIGURED','reason':'YOUTUBE_API_KEY not set. Use available browser/search tools; do not stop the whole assessment.'}
    cutoff=datetime.now(UTC)
    videos={}; window_records=[]
    for start_days,end_days in ((14,7),(7,0)):
        start=cutoff-timedelta(days=start_days); end=cutoff-timedelta(days=end_days)
        cursor=None; ids=set(); pages=0; failed=False
        for page in range(args.max_pages_per_window):
            params={'part':'snippet','type':'video','q':args.query,'order':'date','maxResults':50,
                    'publishedAfter':start.isoformat().replace('+00:00','Z'),
                    'publishedBefore':end.isoformat().replace('+00:00','Z'),
                    'relevanceLanguage':args.language,'regionCode':args.region,'key':key}
            if cursor: params['pageToken']=cursor
            data,_=reader.get('https://www.googleapis.com/youtube/v3/search?'+urllib.parse.urlencode(params),key)
            pages+=1
            if not data:
                failed=True; break
            for item in data.get('items',[]):
                vid=item.get('id',{}).get('videoId')
                if vid:
                    ids.add(vid)
                    videos[vid]={'video_id':vid,'search_snippet':item.get('snippet',{}),
                                 'relevance_status':'UNREVIEWED','format':'UNKNOWN'}
            cursor=data.get('nextPageToken')
            if not cursor: break
        window_records.append({'start':start.isoformat(),'end':end.isoformat(),'query':args.query,
                               'observed_video_ids':sorted(ids),'pages':pages,'failed':failed,
                               'truncated':bool(cursor),'scope':'API_SEARCH_SAMPLE_NOT_PLATFORM_CENSUS'})
    keys=sorted(videos)
    for i in range(0,len(keys),50):
        params={'part':'snippet,statistics,contentDetails','id':','.join(keys[i:i+50]),'key':key}
        details,entry=reader.get('https://www.googleapis.com/youtube/v3/videos?'+urllib.parse.urlencode(params),key)
        for item in (details or {}).get('items',[]):
            videos[item['id']].update(api_details=item,observed_at=entry.get('collected_at'),raw_ref=entry['artifact'])
    write(reader.out/'youtube_sample.json',{'query':args.query,'cutoff_at':cutoff.isoformat(),
          'collected_at':now(),'region':args.region,'language':args.language,'windows':window_records,
          'videos':list(videos.values()),'warning':'Relevance review required. Current views cannot recreate first-24h views. Duration alone does not identify Shorts.'})
    return {'status':'SAMPLE_COLLECTED','videos':len(videos),'next':'Verify game identity, deduplicate channels, remove reposts and compare matching windows.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='kind',required=True)
    rb=sub.add_parser('roblox'); g=rb.add_mutually_exclusive_group(required=True)
    g.add_argument('--url'); g.add_argument('--universe-id')
    rb.add_argument('--badges',action='store_true'); rb.add_argument('--out',required=True)
    yt=sub.add_parser('youtube'); yt.add_argument('--query',required=True)
    yt.add_argument('--language',default='en'); yt.add_argument('--region',default='US')
    yt.add_argument('--max-pages-per-window',type=int,default=2); yt.add_argument('--out',required=True)
    args=parser.parse_args()
    try:
        if args.kind=='youtube' and not 1<=args.max_pages_per_window<=5:
            raise ValueError('max-pages-per-window must be 1..5; increasing it spends quota')
        out=Path(args.out); out.mkdir(parents=True,exist_ok=False)
        reader=Reader(out)
        try:
            result=roblox(args,reader) if args.kind=='roblox' else youtube(args,reader)
        except Exception as exc:
            secret=os.environ.get('YOUTUBE_API_KEY','')
            text=str(exc)
            if secret: text=text.replace(secret,'REDACTED')
            result={'status':'UNAVAILABLE','reason':text[:400]}
        write(out/'collection_log.json',{'finished_at':now(),'result':result,'requests':reader.log})
        print(json.dumps({'out':str(out.resolve()),**result},ensure_ascii=False))
        return 0 if result['status'] in {'SNAPSHOT_COLLECTED','SAMPLE_COLLECTED'} else 2
    except (ValueError,OSError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr); return 2

if __name__=='__main__': raise SystemExit(main())
