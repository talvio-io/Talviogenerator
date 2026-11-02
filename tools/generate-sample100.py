from PIL import Image, ImageDraw, ImageFont
import random, json, hashlib, pathlib, itertools

OUT = pathlib.Path("/home/hatch/workspace/your_files/talvio-generator/sample-100")
S=64; SCALE=16
random.seed(42)

BLACK=(5,5,8); WHITE=(245,246,250); GOLD=(255,196,0); CYAN=(0,229,255); PINK=(255,150,170)

BACKGROUNDS=[
 ("Midnight Black Dot",(5,5,8),(42,42,56),"dots"),
 ("Deep Navy Dot",(4,8,20),(35,54,94),"dots"),
 ("Purple Nebula Dot",(13,4,22),(59,35,88),"stars"),
 ("Emerald Dark Dot",(3,18,12),(23,63,44),"dots"),
 ("Crimson Dark Dot",(20,4,6),(87,31,42),"stars"),
 ("Charcoal Grid",(10,10,10),(38,38,38),"grid"),
 ("Starfield Black",(2,2,8),(70,72,88),"stars"),
 ("Sepia Dot",(18,12,4),(84,62,26),"dots"),
 ("Teal Abyss Dot",(2,16,18),(20,78,84),"dots"),
 ("Ghost Dot",(16,16,22),(210,212,220),"dots"),
]
FACES=[("Silver",(201,204,214)),("Pearl",(238,239,244)),("Aurum Tint",(246,201,76)),("Rose Tint",(243,183,196)),("Cyan Tint",(172,228,236)),("Mint",(178,232,199)),("Lavender",(199,183,240)),("Cream",(244,228,184)),("Sky",(168,203,244)),("Shadow Grey",(143,148,163))]
EARS=[("Gold",GOLD),("Silver",(190,193,204)),("Cyan",CYAN),("Pink",PINK),("Black",(22,22,28)),("White",WHITE)]
EYES=["Black Dot","Cross Dot","Star Dot","Wink","Happy","X Dot"]
ANTENNAS=["Black Dot Orb","Gold Dot Orb","Cyan Dot Orb","Star","Diamond","Halo"]
CORES=[("Gold Ring",GOLD),("Cyan Ring",CYAN),("Pink Ring",(255,110,150)),("Silver Ring",(210,213,224)),("White Ring",WHITE),("Emerald Ring",(40,220,140)),("Violet Ring",(170,110,255))]
MOUTHS=["Smile","Open Dot","Cat","Flat","Grin"]
EXTRAS=["Blush","Glasses","Bow","Star Cheek","None"]
AURAS=["Dotted Circle","Gold Ring","Cyan Ring","None"]
BODIES=[("Black",(18,18,24)),("Navy",(16,22,44)),("Purple",(34,18,52)),("Forest",(14,38,26)),("Maroon",(48,16,22)),("Charcoal",(34,34,40))]

# Build 100 unique combos: token 1 = original #0001 traits, rest shuffled unique
first = (0,0,0,0,0,0,0,0,0,0)  # indexes in order below
combos=set([first])
while len(combos)<100:
    combos.add(tuple(random.randrange(len(x)) for x in [BACKGROUNDS,FACES,EARS,EYES,ANTENNAS,CORES,MOUTHS,EXTRAS,AURAS,BODIES]))
combos=[first]+[c for c in combos if c!=first]
combos=combos[:100]

def draw_token(idx, c):
    bi,fi,ei,eyi,ai,ci,mi,xi,ui,boi = c
    bgname,bg,dot,pattern = BACKGROUNDS[bi]
    facename,face = FACES[fi]
    earname,ear = EARS[ei]
    bodyname,body = BODIES[boi]
    corename,core = CORES[ci]
    img=Image.new("RGB",(S,S),bg); d=ImageDraw.Draw(img)
    rng=random.Random(1000+idx)
    # background pattern
    if pattern=="dots":
        for y in range(0,S,4):
            for x in range(0,S,4): d.rectangle([x+1,y+1,x+1,y+1],fill=dot)
    elif pattern=="grid":
        for i in range(0,S,6):
            d.line([(i,0),(i,S)],fill=dot); d.line([(0,i),(S,i)],fill=dot)
    if pattern=="stars":
        for y in range(0,S,4):
            for x in range(0,S,4): d.point((x+1,y+1),fill=dot)
        for _ in range(45):
            x=rng.randrange(S); y=rng.randrange(S); d.point((x,y),fill=WHITE if rng.random()<.4 else dot)
    # aura
    aura=AURAS[ui]
    if aura=="Dotted Circle":
        for y in range(10,39,3):
            for x in range(18,47,3): d.point((x,y),fill=dot)
        d.ellipse([14,6,50,42],outline=dot,width=1)
    elif aura in ("Gold Ring","Cyan Ring"):
        d.ellipse([13,5,51,43],outline=GOLD if aura=="Gold Ring" else CYAN,width=2)
    def rect(x,y,w,h,col): d.rectangle([x,y,x+w-1,y+h-1],fill=col)
    # waving arm (right)
    rect(50,14,5,9,face); rect(52,11,2,4,face); rect(55,13,2,3,face); rect(49,12,2,3,face)
    rect(48,22,4,12,body)
    # left arm
    rect(11,36,5,10,body); rect(10,44,5,4,face)
    # legs/feet
    rect(24,52,7,6,body); rect(36,52,7,6,body); rect(21,57,11,3,face); rect(35,57,11,3,face)
    # body suit with dots
    rect(20,38,24,15,body); d.rectangle([20,38,43,52],outline=WHITE)
    for (x,y) in [(23,41),(29,44),(36,41),(41,46),(25,49),(34,50),(40,42)]:
        d.point((x,y),fill=WHITE)
    # core
    if ci<5:
        d.ellipse([28,41,36,49],fill=BLACK,outline=WHITE,width=1)
        d.ellipse([30,43,34,47],fill=BLACK,outline=core,width=1); d.point((32,45),fill=CYAN)
    elif corename=="Emerald Ring":
        rect(28,41,9,9,BLACK); d.rectangle([28,41,36,49],outline=core); d.point((32,45),fill=core)
    else:
        d.polygon([(32,41),(37,49),(27,49)],fill=BLACK,outline=core); d.point((32,46),fill=CYAN)
    # neck + head
    rect(29,35,6,3,(90,90,105))
    rect(19,14,26,22,face); d.rectangle([19,14,44,35],outline=BLACK)
    rect(19,14,26,3,WHITE)
    rect(16,23,3,7,ear); rect(45,23,3,7,ear)
    # antenna
    ant=ANTENNAS[ai]
    if ant!="Halo": rect(31,7,2,7,(90,90,105))
    if "Orb" in ant:
        col=BLACK if ant.startswith("Black") else (GOLD if ant.startswith("Gold") else CYAN)
        d.ellipse([28,2,36,10],fill=BLACK if col==BLACK else col,outline=WHITE,width=1); d.point((31,5),fill=WHITE)
    elif ant=="Star":
        for (x,y) in [(32,2),(32,3),(32,4),(30,4),(31,4),(33,4),(34,4),(31,5),(33,5)]: d.point((x,y),fill=GOLD)
    elif ant=="Diamond":
        d.polygon([(32,1),(36,5),(32,10),(28,5)],fill=CYAN,outline=WHITE)
    elif ant=="Halo":
        d.ellipse([26,1,38,7],outline=GOLD,width=2)
    # eyes
    eye=EYES[eyi]
    def eye_dot(cx,cy):
        d.ellipse([cx-3,cy-3,cx+2,cy+2],fill=BLACK); d.point((cx-2,cy-2),fill=WHITE)
    def eye_cross(cx,cy):
        for dx,dy in [(0,-3),(0,3),(-3,0),(3,0),(0,0),(-2,0),(2,0),(0,-2),(0,2)]: d.point((cx+dx,cy+dy),fill=BLACK)
    def eye_star(cx,cy):
        eye_cross(cx,cy); d.point((cx-2,cy-2),fill=BLACK); d.point((cx+2,cy+2),fill=BLACK); d.point((cx-2,cy+2),fill=BLACK); d.point((cx+2,cy-2),fill=BLACK)
    def eye_x(cx,cy):
        for k in range(-2,3): d.point((cx+k,cy+k),fill=BLACK); d.point((cx+k,cy-k),fill=BLACK)
    def eye_happy(cx,cy):
        for dx,dy in [(-3,1),(-2,-1),(-1,-2),(0,-2),(1,-2),(2,-1),(3,1)]: d.point((cx+dx,cy+dy),fill=BLACK)
    draw_eye={"Black Dot":eye_dot,"Cross Dot":eye_cross,"Star Dot":eye_star,"X Dot":eye_x,"Happy":eye_happy}.get(eye)
    if eye=="Wink": eye_dot(26,24); rect(36,24,6,1,BLACK)
    else: draw_eye(26,24); draw_eye(38,24)
    # mouth
    m=MOUTHS[mi]
    if m=="Smile": rect(29,30,6,1,BLACK); rect(30,31,4,1,BLACK)
    elif m=="Open Dot": d.ellipse([30,29,34,33],fill=BLACK)
    elif m=="Cat": rect(28,30,3,1,BLACK); rect(33,30,3,1,BLACK); rect(30,31,4,1,BLACK)
    elif m=="Flat": rect(29,31,6,1,BLACK)
    elif m=="Grin": rect(28,29,8,4,WHITE); d.rectangle([28,29,35,32],outline=BLACK)
    # extra
    ex=EXTRAS[xi]
    if ex in ("Blush","Star Cheek"):
        col=PINK if ex=="Blush" else GOLD
        rect(22,30,3,2,col); rect(39,30,3,2,col)
    if ex=="Glasses":
        d.rectangle([22,20,30,28],outline=BLACK); d.rectangle([34,20,42,28],outline=BLACK); rect(30,23,4,1,BLACK)
    if ex=="Bow":
        d.polygon([(42,12),(47,9),(47,15)],fill=PINK); d.polygon([(42,12),(37,9),(37,15)],fill=PINK); d.point((42,12),fill=GOLD)
    return img.resize((S*SCALE,S*SCALE),Image.NEAREST), {
        "Background":bgname,"Face":facename,"Ears":earname,"Eyes":eye,"Antenna":ant,
        "Chest Core":corename,"Mouth":m,"Extra":ex,"Aura":aura,"Body":bodyname}

all_meta=[]; hashes=set()
for n,c in enumerate(combos, start=1):
    img, traits = draw_token(n,c)
    fn=f"{n:04d}.png"; img.save(OUT/"images"/fn)
    hashes.add(hashlib.sha256(img.tobytes()).hexdigest())
    # rarity: simple score from rare traits
    score=sum([traits["Face"]=="Aurum Tint", traits["Antenna"]=="Halo", traits["Eyes"]=="X Dot", traits["Chest Core"]=="Violet Ring", traits["Aura"]=="Gold Ring", traits["Extra"]=="Bow"] )
    rarity="Legendary" if score>=3 else ("Epic" if score==2 else ("Rare" if score==1 else "Common"))
    meta={"name":f"Talvio Generator #{n:04d} — Black Dot","description":"Sample variation of Talvio Generator — Black Dot robot collection. Pixel robot waving hello, generated from the #0001 main character trait system.","image":fn,
          "attributes":[{"trait_type":k,"value":v} for k,v in traits.items()]+[{"trait_type":"Rarity","value":rarity}]}
    (OUT/"metadata"/f"{n:04d}.json").write_text(json.dumps(meta,indent=2,ensure_ascii=False))
    all_meta.append(meta)
(OUT/"traits-all-100.json").write_text(json.dumps(all_meta,indent=2,ensure_ascii=False))
print("tokens:",len(all_meta),"unique image hashes:",len(hashes),"unique combos:",len(set(combos)))
from collections import Counter
print("rarity:",Counter(m["attributes"][-1]["value"] for m in all_meta))
