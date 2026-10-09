# Evaluasi CER beberapa metode enhancement pada area nomor ijazah.
# Ground truth diisi manual dari ijazah. Jalankan: python eval_cer.py
import cv2, numpy as np, pytesseract, re, json
IMG='01_HighQuality_Enhanced.jpg'   # ganti dengan file ijazah Anda
GT_NUM='571012022000056'; GT_LINE='Nomor ijazah: 571012022000056'
ROI=(0.04,0.90,0.32,0.97)
def lev(a,b):
    d=list(range(len(b)+1))
    for i,ca in enumerate(a,1):
        p=d[:]; d[0]=i
        for j,cb in enumerate(b,1):
            d[j]=min(p[j]+1,d[j-1]+1,p[j-1]+(ca!=cb))
    return d[-1]
def cer(h,r): return lev(h,r)/len(r)
def crop(i):
    h,w=i.shape[:2];x1,y1,x2,y2=ROI;return i[int(y1*h):int(y2*h),int(x1*w):int(x2*w)]
def pad(b): return cv2.copyMakeBorder(b,20,20,20,20,cv2.BORDER_CONSTANT,value=255)
def up(r,f=2): return cv2.resize(r,None,fx=f,fy=f,interpolation=cv2.INTER_CUBIC)
clahe=cv2.createCLAHE(2.0,(8,8))
def m_none(g): return pad(g)
def m_upscale(g): return pad(up(g))
def m_clahe(g): return pad(up(clahe.apply(cv2.GaussianBlur(g,(3,3),0))))
def m_otsu(g): return pad(cv2.threshold(up(g),0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1])
def m_adapt(g): return pad(cv2.adaptiveThreshold(up(g),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,31,15))
def m_clahe_otsu(g):
    e=clahe.apply(cv2.GaussianBlur(g,(3,3),0)); return pad(cv2.threshold(up(e),0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1])
def m_sharp_otsu(g):
    u=up(g); b=cv2.GaussianBlur(u,(0,0),3); s=cv2.addWeighted(u,1.8,b,-0.8,0)
    return pad(cv2.threshold(s,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1])
def m_median_otsu(g):
    u=cv2.medianBlur(up(g),5); return pad(cv2.threshold(u,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1])
methods={'Tanpa enhancement (gray)':m_none,'Upscale 2x':m_upscale,'CLAHE':m_clahe,'Otsu':m_otsu,'Adaptive threshold':m_adapt,'CLAHE + Otsu (notebook)':m_clahe_otsu,'Sharpen + Otsu':m_sharp_otsu,'Median blur + Otsu':m_median_otsu}
def parse(t):
    t=t.strip().replace('\n',' ')
    m=re.search(r":\s*([A-Za-z0-9\-\./]{6,})",t)
    return m.group(1).upper() if m else (max(re.findall(r"[A-Za-z0-9\-\./]{8,}",t),key=len).upper() if re.findall(r"[A-Za-z0-9\-\./]{8,}",t) else '')
img=cv2.imread(IMG); g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
rng=np.random.default_rng(0)
def degr(g):
    out={'Asli':g}
    out['Resolusi 0.4x']=cv2.resize(cv2.resize(g,None,fx=.4,fy=.4,interpolation=cv2.INTER_AREA),(g.shape[1],g.shape[0]))
    out['Noise Gauss s=25']=np.clip(g.astype(float)+rng.normal(0,25,g.shape),0,255).astype(np.uint8)
    out['Blur k=7']=cv2.GaussianBlur(g,(7,7),0)
    out['Kontras rendah']=(g*0.45+110).astype(np.uint8)
    ok,enc=cv2.imencode('.jpg',g,[cv2.IMWRITE_JPEG_QUALITY,12]); out['JPEG q=12']=cv2.imdecode(enc,0)
    return out
res={}; detail={}
for dn,gd in degr(g).items():
    roi=crop(gd)
    for mn,f in methods.items():
        raw=pytesseract.image_to_string(f(roi),config='--oem 3 --psm 7').strip()
        num=parse(raw)
        res.setdefault(mn,{})[dn]=(cer(raw,GT_LINE),cer(num,GT_NUM))
        detail[(mn,dn)]=(raw,num)
conds=list(next(iter(res.values())).keys())
print('CER BARIS PENUH (teks OCR mentah vs "Nomor ijazah: 571012022000056")')
print('| Metode | '+' | '.join(conds)+' | Rata-rata |')
for mn in methods:
    v=[res[mn][c][0] for c in conds]; print(f'| {mn} | '+' | '.join(f'{x:.3f}' for x in v)+f' | {np.mean(v):.3f} |')
print('\nCER NOMOR SAJA (hasil parsing vs 571012022000056)')
print('| Metode | '+' | '.join(conds)+' | Rata-rata |')
for mn in methods:
    v=[res[mn][c][1] for c in conds]; print(f'| {mn} | '+' | '.join(f'{x:.3f}' for x in v)+f' | {np.mean(v):.3f} |')
print('\nDETAIL OCR (Asli):')
for mn in methods: print(mn,detail[(mn,'Asli')])
