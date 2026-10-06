import asyncio, json, sys
from playwright.async_api import async_playwright
OUT='/workspace/video-jobs/HM-106/lam-viec/assets/raw/'
PAGES={'openai':'https://openai.com/index/new-chatgpt-ads-format-and-measurement/',
       'techcrunch':'https://techcrunch.com/2026/10/05/openai-launches-visual-ads-that-appear-alongside-image-generation-results/'}
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36'
async def main():
    log={}
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',headless=True,args=['--disable-blink-features=AutomationControlled','--no-sandbox'])
        for name,url in PAGES.items():
            ctx=await b.new_context(viewport={'width':1100,'height':1400},device_scale_factor=2,user_agent=UA,locale='en-US')
            pg=await ctx.new_page()
            try:
                r=await pg.goto(url,wait_until='domcontentloaded',timeout=60000)
                await pg.wait_for_timeout(8000)
                # scroll to trigger lazy load
                for y in range(0,12000,700):
                    await pg.evaluate(f'window.scrollTo(0,{y})'); await pg.wait_for_timeout(250)
                await pg.evaluate('window.scrollTo(0,0)'); await pg.wait_for_timeout(1500)
                title=await pg.title()
                await pg.screenshot(path=OUT+f'{name}_viewport.png')
                await pg.screenshot(path=OUT+f'{name}_fullpage.png',full_page=True)
                # dump text-block bounding boxes for crops
                boxes=await pg.evaluate('''()=>{const out=[];document.querySelectorAll('h1,h2,p,li,time,figure,img,figcaption,blockquote').forEach(e=>{const r=e.getBoundingClientRect();if(r.width>20&&r.height>8)out.push({tag:e.tagName,x:r.x+scrollX,y:r.y+scrollY,w:r.width,h:r.height,text:(e.innerText||e.alt||'').slice(0,160)})});return out}''')
                json.dump(boxes,open(OUT+f'{name}_boxes.json','w'),indent=1,ensure_ascii=False)
                log[name]={'status':r.status if r else None,'title':title,'ok':True}
            except Exception as ex:
                log[name]={'ok':False,'error':str(ex)[:300]}
            await ctx.close()
        await b.close()
    json.dump(log,open(OUT+'capture_log.json','w'),indent=1)
    print(json.dumps(log,indent=1))
asyncio.run(main())
