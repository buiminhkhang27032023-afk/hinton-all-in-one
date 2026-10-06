import re,html,sys
s=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
t=re.sub(r'<script.*?</script>|<style.*?</style>','',s,flags=re.S)
t=re.sub(r'<[^>]+>','\n',t); t=html.unescape(t)
lines=[l.strip() for l in t.split('\n') if l.strip()]
j='\n'.join(lines)
start=int(sys.argv[2]) if len(sys.argv)>2 else 0
print(j[start:start+int(sys.argv[3]) if len(sys.argv)>3 else start+10000])
