# append stricter-sfx, caption-chunk and channel-observation sections to every breakdown (idempotent)
import glob,os,json,re
R='/workspace/video-learn'
OBS={
'tiktokintl-kanekallaway':"Split B-roll trên / mặt dưới, đường chia quanh y≈960px; caption 1–3 chữ đậm ở ngay đường chia (video 7645… màu cam vàng serif, video 7692… trắng sans) → màu caption đổi theo video; định kỳ full-face với MỘT chữ rất to (serif nghiêng 'future', sans 'humanity'), cao chữ 150–230px; PIP mặt tròn góc trái trên khi phần trên là UI/điện thoại; mockup điện thoại 3D nghiêng trên nền màu thương hiệu; thanh tiêu đề đỏ/đen trượt vào trong 1s đầu ở một số video.",
'tiktokintl-rileybrown.ai':"POV/quay màn hình bằng máy, ít cắt; ô tiêu đề đen bo góc chữ trắng ở trên cùng 0–10s ('Opus 5.5 is Insane'); caption IN HOA trắng đậm có bóng đen ở dưới (y≈1600–1700px), 1–3 chữ; mũi tên đỏ chỉ vào vật; selfie mở đầu với mặt sát camera.",
'tiktok-hungnpv':"Hook selfie mặt sát camera + ô trắng bo góc chữ đen 2–3 dòng ở giữa; sau đó quay màn hình laptop bằng điện thoại, ngón tay chỉ vào UI; nhãn bước ô trắng 'B1/B2/B4…' và ô chú thích trắng ở mép trên; KHÔNG có caption chạy theo lời; kết bằng selfie + ô 'Follow for more'.",
'tiktok-hieuanca':"Screen record nền tối có vân địa hình; mặt PIP nhỏ góc trái dưới (≈230px rộng, y≈1380–1650px); caption to trắng đậm viền, từ khoá vàng/lime, đặt cạnh PIP; khoanh tròn/mũi tên đỏ; pill lime #C0F030-ish chữ đen; ảnh minh hoạ kiểu truyện tranh AI ở đoạn cuối.",
'douyin-qiuzhi2046':"16:9 (bản YouTube); mặt trung cảnh trong studio neon tím; từ khoá Trung/Anh rất to màu vàng viền đen 3D ở giữa khung; phụ đề song ngữ trắng (Trung trên, Anh dưới) ở đáy y≈0,9H; PIP mặt tròn góc trái dưới trên UI; chip lime ở góc trái trên; thumbnail video cũ pop-in góc phải trên; end card logo '秋芝2046' nền đen.",
'douyin-chengxuyuanyupi':"Short dọc (bản YouTube): mặt toàn khung hoặc mặt ở nửa dưới với ảnh chụp màn hình/code ở nửa trên; tiêu đề phần trắng trên dải đen ở đỉnh ('让 AI 收集素材'); caption Trung trắng viền đen ở y≈0,68–0,75H, câu chỉ dẫn quan trọng màu vàng ở giữa; khung đỏ khoanh code, mũi tên đỏ viền; hiệu ứng biến dạng mặt/emoji ở cuối; kết bằng câu hỏi ('你学会了吗').",
'facebook-nguyentatkiem':"Screen record điện thoại toàn khung + PIP mặt vuông góc phải trên (≈210px rộng); caption IN HOA vàng đậm viền đen ở y≈0,62–0,72H; mũi tên đỏ chỉ nút; card listicle ở một số video; outro là clip talking head khác với nút FOLLOW xanh dương + con trỏ tay ở góc phải trên, caption vàng nhỏ ở dưới.",
'facebook-aisavvy':"(Proxy TikTok) 3 vùng: dải đen trên cùng có logo công cụ, clip 16:9 ở giữa-trên, thanh tiến trình đỏ 'TUTORIAL INCOMING', người nói ở nửa dưới (studio đèn LED lục giác); caption MỘT chữ cam #F09018-ish viền đen ở đường chia; pill cam 'openart.ai'/'LINK IN BIO'.",
}
for md in sorted(glob.glob(R+'/*/*_breakdown.md')):
    d=os.path.dirname(md); ch=os.path.basename(d); vid=os.path.basename(md)[:-len('_breakdown.md')]
    s=open(md).read(); s=s.split('\n## Bổ sung (vòng 2)')[0].rstrip()+'\n'
    add=['','## Bổ sung (vòng 2)','']
    hf=f'{d}/{vid}_audio_hf.json'
    if os.path.exists(hf):
        h=json.load(open(hf))
        add.append(f"- [ĐO/SUY] Ứng viên sfx CHẶT (năng lượng 4–10 kHz bật ≥10 dB, nghiêng phổ cao hơn giọng ≥6 dB, kéo dài ≥0,2s): {h['hits_per_min']}/phút · {h['pct_cuts_with_hit']}% điểm cắt (0,3) có hit trong ±0,25s · {h['pct_hits_on_cut']}% hit rơi vào điểm cắt · hit trong 0–3s: {h['hits_0_3s']} · thời điểm: {h['hf_hits'][:40]}")
    cc=f'{R}/capchunks/{vid}.json'
    if os.path.exists(cc):
        c=json.load(open(cc))
        add.append(f"- [ĐO/OCR 10fps] Cụm caption trong cửa sổ {c['win'][0]}–{c['win'][1]}s (dải y {c['band'][0]}–{c['band'][1]}H): {c['n']} cụm · thời lượng trung vị {c['dur_med']}s (≈{c['frames30_med']} frame @30fps), p10 {c['dur_p10']}s, p90 {c['dur_p90']}s · {c['gap_zero_pct']}% cụm nối liền không khoảng trống")
        add.append('  - Mẫu: '+' | '.join(f"{t}s +{dd}s \"{tx[:30]}\"" for t,dd,tx in c['chunks'][:10]))
    add.append(f"- [KHUNG – quan sát contact sheet, mức kênh] {OBS.get(ch,'')}")
    open(md,'w').write(s+'\n'.join(add)+'\n')
print('done')
