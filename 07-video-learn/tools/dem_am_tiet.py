import re,sys
W={'the':1,'australian':4,'chatgpt':4,'adn':3,'alphafold':3,'google':2,'calendar':3,'email':2,'agent':2,'ai':2,'rosie':2,'paul':1,'new':1,'south':1,'wales':1,'gemini':3,'claude':1,'openai':4,'notebooklm':5,'gpt':3,'cursor':2,'sora':2,'veo':2}
def count(t):
    n=0
    for w in re.findall(r'[\wÀ-ỹ]+',t.replace('-',' ')):
        n+=W.get(w.lower(),1)
    return n
for f in sys.argv[1:]:
    t=open(f).read(); n=count(t); print(f,n,'âm tiết nói;', round(n/4.35,1),'s @4,35 âm tiết/s')
