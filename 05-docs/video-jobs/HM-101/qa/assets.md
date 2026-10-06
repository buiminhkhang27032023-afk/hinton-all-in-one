# HM-101 v2 — assets.md

All editorial stills under `source/assets/`. India Today blocked (403/Access Denied); Muse Home Link + gadget visuals taken from gadgets.muse.ai + GitHub README instead.

| File | Source | Notes |
|---|---|---|
| img01_meta_hero.png | https://research.meta.ai/articles/math-papers/hero/math-papers-hero-light-v1.webp (og/hero of Meta Research blog) | Hero network viz |
| img02_fig1_ellipsoid.png | Meta blog Figure 1 via hyperframes capture `gaussian-ellipsoid-threshold-v2.webp` · https://research.meta.ai/blog/solving-open-research-problems-together | Fig 1 ellipsoid threshold |
| img03_fig2_blowup.png | Meta blog Figure 2 · `biharmonic-nls-blow-up-v3.webp` | Wave blow-up sequence |
| img04_fig3_384group.png | Meta blog Figure 3 · `semiabelian-galois-group-v2.webp` | Order-384 counterexample |
| img05_fig4_relaxation.png | Meta blog Figure 4 · `cycle-based-relaxation-v2.webp` | Approximation region |
| img06_fig5_mumford.png | Meta blog Figure 5 · `genus-two-mumford-curve-v2.webp` | Mumford curve graph |
| img08_meta_blog_title.png | Chrome headless screenshot of Meta blog (crop title/hero) | Blog title card |
| img09_muse_gadgets_hero.png | Chrome screenshot https://gadgets.muse.ai/ | Muse Gadgets hero |
| img10_muse_home_link.png | Crop from gadgets.muse.ai (Home Link puck + claim CTA) | Muse Home Link device |
| img11_muse_project_ideas.png | Crop from gadgets.muse.ai Project Ideas gallery | ESP32 / Pi / e-ink |
| img12_github_readme.png | Chrome screenshot https://github.com/facebookincubator/muse-gadget-sdk | README + board row |
| img13_github_boards.png | Crop of GitHub README hardware strip | ESP32 boards |
| img14_alexandr_announce.png | Crop https://twiscan.com/en/x/alexandr_wang/2106113742266089526 | Muse Gadgets announce visual |
| img15_meta_research_home.png | Chrome screenshot https://research.meta.ai/ | Meta Research home |
| img16_meta_logo.png | Designed brand card (Meta × Muse Spark) citing Meta Research | Editorial wordmark |
| img17–img22 paper cards | Designed title cards citing Meta blog / arXiv abs IDs from blog links | 6 paper covers |
| img23–img27 arxiv_abs.png | Chrome screenshots arxiv.org/abs/{2608.10184,2608.12415,2608.27372,2507.12831,2609.25023} | Paper abs pages |
| img28_muse_device_row.png | Crop gadgets.muse.ai hero device row | Device strip |

**Also captured (not all used as primary scene BG):** full Meta blog PNG, HF capture package under `lam-viec/capture_tmp/hf_meta/`, India Today AMP blocked.

**Voice:** reused v1 `/workspace/video-jobs/HM-101/output/voice_storytelling.wav` (no TTS / no OmniVoice).

---

# HM-101 v3 — assets (style remake theo ref 2026-10-05)

**Video mẫu** `/workspace/video-learn/ref-20261005/ref.mp4`: CHỈ học phong cách — không dùng footage, logo hay lưới ô đỏ của kênh mẫu.
**Voice:** dùng lại v1 `output/voice_storytelling.wav` (md5 c0293440…), **không TTS lại**.

## Ảnh biên tập (dùng lại 27 ảnh v2, nguồn như bảng v2 ở trên)
Mỗi ảnh được zoom/crop + nền blur của chính ảnh, xuất ra `lam-viec/v3_shots/*.jpg` (không có ảnh bên thứ ba mới).
Dùng trong v3: img01–img06, img08–img27 (26/27; img28_muse_device_row không dùng).

## Đồ họa tự thiết kế cho v3 (HTML/CSS trong `lam-viec/hf_v3/index.html`, không dùng ảnh ngoài)
| Asset | Ghi chú |
|---|---|
| Thẻ hook "AI GIẢI 5 BÀI TOÁN MỞ" | Template Hinton (vàng/đỏ trên xanh đậm/đen), nền hero Meta (img01) làm mờ → `v3_shots/claim_bg.jpg` |
| Template số Hinton ×5 | 6 bài báo · 5 Olympiad (huy chương vẽ bằng CSS) · 384 phần tử · 2015 · 5.000 Muse Home Link — bộ đếm kinetic + khung đỏ tự vẽ |
| Thẻ "KHÔNG CÓ CHÌA ĐÁP ÁN" | Chữ + gạch đỏ |
| Mockup chat meta.ai | Minh họa (pill "Minh họa · meta.ai"), không phải ảnh chụp màn hình thật |
| Sơ đồ Người dẫn dắt → AI cộng sự → Nhóm thẩm định | Đồ họa HTML |
| Phương trình "Chuyên gia + AI chat thường = Kết quả cấp nghiên cứu" | Đồ họa HTML |
| Thẻ câu hỏi outro | "AI đã biết tạo kiến thức mới, bạn sẽ dùng nó làm gì?" |
| Thẻ NGƯỜI VIẾT / AI SOẠN, badge 02/10 · 5/6 · 2024, dấu "CHƯA BÌNH DUYỆT" | Đồ họa HTML |
| Khung đỏ / vệt highlighter vàng / gạch chân đỏ | Lớp phủ SVG/CSS tự vẽ trên screenshot |

## Presenter
`/workspace/hinton-pipeline-docs/assets/presenter-video-novoice.mp4` (bản crop 9:16 `hf_v2/assets/presenter_full.mp4`, muted) — 4 nhịp full-frame.

## Font
Montserrat (biến thể variable, wght 900) — Google Fonts, SIL Open Font License 1.1 — `/usr/share/fonts/truetype/sand-box/google/Montserrat/Montserrat-VariableFont_wght.ttf`.

## Âm thanh — tự tạo 100%, không dùng sample/nhạc bên thứ ba
Tổng hợp theo thuật toán bằng Python/numpy (`lam-viec/synth_sfx_v3.py`, seed 101), mix/loudness/limiter bằng ffmpeg (`lam-viec/mix_v3.py`). Tự tạo → không cần license.
| File (`source/sfx/`) | Cách tạo |
|---|---|
| bgm_synth_120bpm.wav | Nền synth 120 BPM, vòng hợp âm Am–F–C–G: pad saw lệch tông + bass + arp pluck nốt móc + kick/hat nhẹ, có pump sidechain; 52.2s stereo |
| whoosh_a/b/c.wav | Noise qua bộ lọc band quét (300→7k / 600→9k / 200→5k Hz), envelope swell |
| ding.wav | Chuông cộng partial (1568/2349/3136/4704 Hz), tắt dần theo hàm mũ |
| pop.wav | Sine giảm cao độ (950→220 Hz) + click |
| marker.wav | Noise band-pass ngắn (tiếng bút dạ quang) |
| impact.wav | Sine trầm giảm cao độ + noise (khi cắt vào presenter / dấu mộc) |

Mix (`lam-viec/audio_v3/loudness.json`): VO −14.0 LUFS · BGM sau ducking ≈ −24.2 LUFS · bus SFX −21 LUFS · mix tổng ≈ −13.1 LUFS, true peak ≤ −0.8 dBFS. Cắt im lặng ở 51.60s (cắt đen).
