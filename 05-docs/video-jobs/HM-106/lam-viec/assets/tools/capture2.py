import asyncio, json
from playwright.async_api import async_playwright
A='/workspace/video-jobs/HM-106/lam-viec/assets/'
OUT=A+'src/'
DSF=3
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36'
PAGES={
 'openai':('https://openai.com/index/new-chatgpt-ads-format-and-measurement/',[
   ('oa_headline_date',['October 5, 2026','Building advertising for the way people use AI','A new visual ad format helps'],['October 5, 2026','Building advertising for the way people use AI']),
   ('oa_hero_figure',['@img:Two ChatGPT mobile screens'],[]),
   ('oa_labeled_noinfluence',['Initially, we\'ll test this new ad format'],['Ads will be clearly labeled','advertising does not influence the answers ChatGPT provides']),
   ('oa_us_test',['Testing will begin later this month'],['later this month in the US','initial group of advertisers']),
   ('oa_labeled_us_test',['Initially, we\'ll test this new ad format','Testing will begin later this month'],['Ads will be clearly labeled','advertising does not influence the answers ChatGPT provides','later this month in the US','initial group of advertisers']),
   ('oa_1_2b',['ChatGPT reaches 1.2 billion people'],['ChatGPT reaches 1.2 billion people each week']),
   ('oa_measurement',['@h2:Measuring the impact of ChatGPT Ads','Our measurement philosophy for ChatGPT Ads'],['Measuring the impact of ChatGPT Ads','expanding our measurement tools and partner ecosystem']),
   ('oa_partners',['We now support leading attribution partners'],['AppsFlyer','Triple Whale','Adjust','Branch']),
   ('oa_brand_safety',['developing brand suitability evaluation pilots with DoubleVerify'],['brand suitability evaluation pilots','DoubleVerify (DV)','Integral Ad Science (IAS)']),
 ], 14000),
 'techcrunch':('https://techcrunch.com/2026/10/05/openai-launches-visual-ads-that-appear-alongside-image-generation-results/',[
   ('tc_header',['@img:ChatGPT','@h1:OpenAI launches visual ads'],['OpenAI launches visual ads that appear alongside image generation results','October 5, 2026']),
   ('tc_headline_date',['@h1:OpenAI launches visual ads','@time:October 5, 2026'],['OpenAI launches visual ads that appear alongside image generation results','October 5, 2026']),
   ('tc_lede',['ChatGPT is getting more ads'],['ads will appear alongside images that users ask ChatGPT to generate']),
   ('tc_us_test',['The new ads will begin to appear later this month'],['later this month in the U.S. only for now','initial test group of advertisers','clearly labeled and won\'t influence the answers ChatGPT provides']),
   ('tc_muse',['The move follows the launch of Meta'],['Meta\'s Muse','a growing competitor for leading AI chatbots, like ChatGPT']),
   ('tc_timeline',['OpenAI introduced ads earlier this year'],['introduced ads earlier this year','expanded them to India in August']),
   ('tc_1_2b',['Eventually, those ads will allow'],['ChatGPT\'s 1.2 billion weekly users','once they roll out globally']),
   ('tc_partners',['Alongside the display ads, OpenAI said'],['AppsFlyer','Triple Whale','Adjust','Branch']),
   ('tc_brand_safety',['brand suitability evaluation pilots with help'],['DoubleVerify (DV)','Integral Ad Science (IAS)']),
 ], 2700),
}
JS=r'''
([blocks, phrases]) => {
  const norm = s => s.replace(/[\u2018\u2019]/g,"'").replace(/\u00a0/g,' ');
  const cands=[...document.querySelectorAll('h1,h2,p,time,img,figure')];
  const found=[]; const miss=[];
  for(const b of blocks){
    let el=null;
    if(b.startsWith('@')){
      const [tag,txt]=[b.slice(1).split(':')[0], b.slice(b.indexOf(':')+1)];
      el=[...document.querySelectorAll(tag)].find(e=>{const r=e.getBoundingClientRect(); return r.width>40 && norm(tag=='img'?(e.alt||''):e.innerText).includes(txt)});
    } else {
      el=cands.filter(e=>!['IMG','FIGURE'].includes(e.tagName)).find(e=>{const r=e.getBoundingClientRect(); return r.width>40 && norm(e.innerText).includes(b)});
    }
    if(el){const r=el.getBoundingClientRect(); found.push({b, x:r.x+scrollX,y:r.y+scrollY,w:r.width,h:r.height, el});} else miss.push(b);
  }
  const prs=[];
  for(const ph of phrases){
    let hit=null;
    for(const f of found){
      if(f.el.tagName=='IMG') continue;
      const walker=document.createTreeWalker(f.el,NodeFilter.SHOW_TEXT);
      const nodes=[];let full='';let n;
      while(n=walker.nextNode()){nodes.push([n,full.length]);full+=norm(n.nodeValue);}
      const i=full.indexOf(ph); if(i<0) continue;
      const j=i+ph.length;
      const loc=(k)=>{for(let q=nodes.length-1;q>=0;q--){if(nodes[q][1]<=k) return [nodes[q][0],k-nodes[q][1]];}};
      const [sn,so]=loc(i); const [en,eo]=loc(j-1);
      const rg=document.createRange(); rg.setStart(sn,so); rg.setEnd(en,eo+1);
      const rects=[...rg.getClientRects()].filter(r=>r.width>1).map(r=>({x:r.x+scrollX,y:r.y+scrollY,w:r.width,h:r.height}));
      hit={phrase:ph,rects}; break;
    }
    prs.push(hit||{phrase:ph,rects:[],missing:true});
  }
  return {blocks:found.map(f=>({b:f.b,x:f.x,y:f.y,w:f.w,h:f.h,tag:f.el.tagName})), miss, phrases:prs};
}
'''
async def main():
    res={}
    async with async_playwright() as p:
        br=await p.chromium.launch(executable_path='/usr/bin/google-chrome',headless=True,args=['--disable-blink-features=AutomationControlled','--no-sandbox'])
        for name,(url,targets,maxscroll) in PAGES.items():
            ctx=await br.new_context(viewport={'width':1100,'height':1400},device_scale_factor=DSF,user_agent=UA,locale='en-US')
            pg=await ctx.new_page()
            r=await pg.goto(url,wait_until='domcontentloaded',timeout=60000)
            await pg.wait_for_timeout(7000)
            for y in range(0,maxscroll,600):
                await pg.evaluate(f'window.scrollTo(0,{y})'); await pg.wait_for_timeout(300)
            await pg.evaluate('window.scrollTo(0,0)'); await pg.wait_for_timeout(2000)
            page_info={'url':url,'final_url':pg.url,'http_status':r.status,'title':await pg.title(),'targets':{}}
            if name=='openai':
                await pg.screenshot(path=OUT+'openai_fullpage.png',full_page=True)
            else:
                await pg.screenshot(path=OUT+'techcrunch_fullpage_article.png',full_page=True,clip={'x':0,'y':0,'width':1100,'height':2650})
            for tid,blocks,phrases in targets:
                info=await pg.evaluate(JS,[blocks,phrases])
                if not info['blocks']:
                    page_info['targets'][tid]={'ok':False,'miss':info['miss']}; continue
                pad=24
                x0=min(b['x'] for b in info['blocks'])-pad; y0=min(b['y'] for b in info['blocks'])-pad
                x1=max(b['x']+b['w'] for b in info['blocks'])+pad; y1=max(b['y']+b['h'] for b in info['blocks'])+pad
                if tid=='tc_header': x0,x1=0,1100
                x0=max(0,x0)
                clip={'x':x0,'y':y0,'width':x1-x0,'height':y1-y0}
                await pg.screenshot(path=OUT+tid+'.png',full_page=True,clip=clip)
                phr=[]
                for ph in info['phrases']:
                    phr.append({'phrase':ph['phrase'],'missing':ph.get('missing',False),
                       'rects_px':[[round((q['x']-x0)*DSF),round((q['y']-y0)*DSF),round(q['w']*DSF),round(q['h']*DSF)] for q in ph['rects']]})
                page_info['targets'][tid]={'ok':True,'miss':info['miss'],'clip_css':clip,'size_px':[round(clip['width']*DSF),round(clip['height']*DSF)],'phrases':phr}
            res[name]=page_info
            await ctx.close()
        await br.close()
    json.dump(res,open(OUT+'capture_meta.json','w'),indent=1,ensure_ascii=False)
    for n,v in res.items():
        print(n,v['http_status'],v['final_url'],v['title'][:60])
        for t,i in v['targets'].items(): print('  ',t,i.get('ok'),i.get('size_px'),i.get('miss'),[ (p['phrase'][:25],len(p['rects_px'])) for p in i.get('phrases',[])])
asyncio.run(main())
