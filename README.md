# 🇯🇵 JLPT Path — Lộ trình học JLPT

[![Website](https://img.shields.io/badge/Website-jlptpath.com-blue?style=flat-square)](https://jlptpath.com)
[![Hugo](https://img.shields.io/badge/Hugo-0.146.0-ff4088?style=flat-square&logo=hugo)](https://gohugo.io)
[![Cloudflare Pages](https://img.shields.io/badge/Deploy-Cloudflare%20Pages-f38020?style=flat-square&logo=cloudflare)](https://pages.cloudflare.com)

Website học tiếng Nhật miễn phí theo lộ trình JLPT từ N5 đến N1, dành cho người Việt.

## ✨ Tính năng

- 📚 **110 bài học JLPT** — N5 (25), N4 (25), N3 (20), N2 (20), N1 (20)
- 📖 **200 bài luyện đọc** — 40 bài mỗi cấp độ, có bản dịch tiếng Việt và giải thích ngữ pháp
- 🎧 **Audio gốc từ giáo trình** — Minna no Nihongo (N5-N3), Shinkanzen Master (N2-N1)
- 📝 **Bài kiểm tra xếp lớp** — 30 câu hỏi, tự động đánh giá trình độ JLPT
- 🔍 **Tìm kiếm nhanh** — tìm bài học theo từ khóa
- 🌙 **Dark mode** — hỗ trợ giao diện tối
- 📱 **Responsive** — tương thích mọi thiết bị

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Static Site Generator | [Hugo](https://gohugo.io) v0.146.0 |
| Theme | [PaperMod](https://github.com/adityatelange/hugo-PaperMod) |
| Hosting | [Cloudflare Pages](https://pages.cloudflare.com) |
| Font | Be Vietnam Pro + Noto Sans JP |
| Audio | HTML5 `<audio>` player |

## 📁 Cấu trúc dự án

```
jlptpath/
├── content/
│   ├── jlpt/           # 110 bài học JLPT (N5-N1)
│   ├── reading/         # 200 bài luyện đọc
│   ├── placement-test.md
│   ├── about.md
│   └── ...
├── static/
│   └── audio/           # Audio files (N1-N5)
├── layouts/             # Custom layout overrides
├── assets/css/          # Custom CSS
├── hugo.yaml            # Hugo config
└── deploy.sh            # Deploy script
```

## 🚀 Chạy local

```bash
# Clone
git clone https://github.com/tqcuong-it/jlptpath.git
cd jlptpath

# Cài Hugo (v0.146.0+)
# https://gohugo.io/installation/

# Chạy dev server
hugo server -D

# Build production
hugo --minify
```

## 📦 Deploy

```bash
# Build + deploy lên Cloudflare Pages
./deploy.sh
```

## 📊 Nội dung

| Cấp độ | Bài học | Luyện đọc | Audio |
|--------|---------|-----------|-------|
| N5 🌱 | 25 bài | 40 bài | ✅ Minna no Nihongo |
| N4 📘 | 25 bài | 40 bài | ✅ Minna no Nihongo |
| N3 📙 | 20 bài | 40 bài | ✅ Minna no Nihongo |
| N2 📕 | 20 bài | 40 bài | ✅ Shinkanzen Master |
| N1 👑 | 20 bài | 40 bài | ✅ Shinkanzen Master |

## 👤 Tác giả

**Trần Quang Cương** — Software Engineer / BrSE tại Nhật Bản

- 🌐 [cuongtq.it](https://cuongtq.it)
- 📧 contact@cuongtq.it

## 📄 License

MIT License — xem file [LICENSE](LICENSE) để biết thêm chi tiết.
