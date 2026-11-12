#!/usr/bin/env python3
"""Build the tour-7620 trailer from shots.json.

    python scripts/build_trailer.py                 # full 1080p render -> out/trailer_7620.mp4
    python scripts/build_trailer.py --quality draft # 960x540, fast, for a local check
    python scripts/build_trailer.py --only 09_panlong

Each segment renders to its own mp4 under out/segments/, then the segments are
joined with crossfades, letterboxed to 2.39:1 and laid over the music bed.

Source priority per shot slot (first that exists wins):
    shots/<slot>/clip.mp4        a real moving shot (Seedance / Kling / Veo ...)
    shots/<slot>/generated.png   an AI still (Workers AI flux, or any model)
    <src> from shots.json        the tour's own photo, Ken Burns move

Fonts: shots.json names the Noto CJK files the workflow installs; override with
TRAILER_FONT / TRAILER_FONT_BOLD (a file path, or a fontconfig family name).
"""
import json, os, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "out"
SEG = OUT / "segments"
FF = os.environ.get("FFMPEG", "ffmpeg")

def run(args):
    r = subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", *args])
    if r.returncode:
        sys.exit(f"ffmpeg failed: {' '.join(str(a) for a in args[:8])}...")

def esc(p):
    # drawtext wants the colon in a Windows drive letter escaped
    return str(p).replace("\\", "/").replace(":", "\\:")

def fontarg(spec):
    """'fontfile=...' for a path, 'font=...' for a fontconfig family name."""
    if spec and (os.path.exists(spec) or "/" in spec or "\\" in spec):
        return f"fontfile='{esc(spec)}'"
    return f"font='{spec}'"

def textfile(name, text):
    p = OUT / "txt" / f"{name}.txt"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(text.encode("utf-8"))
    return esc(p)

def is_video(path):
    return Path(path).suffix.lower() in {".mp4", ".mov", ".webm", ".mkv", ".m4v"}

# --- the look -----------------------------------------------------------------
# Teal shadows / amber highlights, slightly lifted blacks, soft vignette, grain:
# the Seedance clip's grade, toned down so real photographs still read as real.
GRADE = ("colorbalance=rs=-0.06:gs=0.0:bs=0.07:rm=0.0:gm=0.0:bm=0.02:rh=0.07:gh=0.02:bh=-0.07,"
         "eq=contrast=1.07:saturation=0.92:brightness=0.01,"
         "vignette=PI/4.6")
GRAIN = "noise=alls=5:allf=t"

def kenburns(dur, move, fps, W, H):
    """Ken Burns over a still, rendered at 2x then downscaled so the move is smooth."""
    frames = int(round(dur * fps))
    pre = f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2}"
    if move in ("panL", "panR", "up"):
        if move == "up":
            cw, ch = W*2, int(H*2*1.25)
        else:
            cw, ch = int(W*2*1.25), H*2
        pre = f"scale={cw}:{ch}:force_original_aspect_ratio=increase,crop={cw}:{ch}"
    z = {
        "in":   f"zoompan=z='1+0.12*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
        "out":  f"zoompan=z='1.12-0.12*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
        "panR": f"zoompan=z='1.0':x='(iw-{W*2})*on/{frames}':y='0'",
        "panL": f"zoompan=z='1.0':x='(iw-{W*2})*(1-on/{frames})':y='0'",
        "up":   f"zoompan=z='1.0':x='0':y='(ih-{H*2})*(1-on/{frames})'",
    }[move]
    z += f":d={frames}:s={W*2}x{H*2}:fps={fps}"
    return f"{pre},{z},scale={W}:{H}:flags=lanczos,{GRADE},{GRAIN},format=yuv420p"

def caption(text, font, H, scale):
    tf = textfile(f"cap_{abs(hash(text))}", text)
    fs = int(38 * scale)
    return (f"drawtext={fontarg(font)}:textfile='{tf}':fontsize={fs}:fontcolor=white@0.92:"
            f"shadowcolor=black@0.6:shadowx=2:shadowy=2:x={int(80*scale)}:y={H-int(95*scale)}:"
            f"alpha='if(lt(t,0.6),0,if(lt(t,1.4),(t-0.6)/0.8,1))'")

def source_for(seg):
    d = HERE / "shots" / seg["slot"]
    for name in ("clip.mp4", "clip.webm", "generated.png", "generated.jpg"):
        if (d / name).exists():
            return d / name
    return HERE / seg["src"] if seg.get("src") else d / "none"

def render_shot(seg, cfg, out, W, H, scale):
    fps = cfg["fps"]; dur = seg["dur"]
    src = source_for(seg)
    if not src.exists():
        sys.exit(f"missing source for {seg['slot']}: {src}")
    cap = caption(seg["caption"], cfg["font"], H, scale) if seg.get("caption") else None
    if is_video(src):
        vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
              f"fps={fps},{GRADE},{GRAIN},format=yuv420p")
        if cap: vf += "," + cap
        run(["-ss", "0", "-t", str(dur), "-i", str(src), "-an", "-vf", vf,
             "-c:v", "libx264", "-preset", "medium", "-crf", "18", str(out)])
    else:
        vf = kenburns(dur, seg.get("move", "in"), fps, W, H)
        if cap: vf += "," + cap
        run(["-loop", "1", "-framerate", str(fps), "-t", str(dur), "-i", str(src),
             "-vf", vf, "-t", str(dur), "-c:v", "libx264", "-preset", "medium",
             "-crf", "18", "-r", str(fps), str(out)])

def render_card(seg, cfg, out, idx, W, H, scale):
    fps = cfg["fps"]; dur = seg["dur"]
    lines = seg["lines"]; n = len(lines)
    lh = int(110 * scale)
    f = f"color=c=0x05080c:s={W}x{H}:d={dur}:r={fps},{GRAIN}"
    for i, line in enumerate(lines):
        tf = textfile(f"card{idx}_{i}", line)
        y = H/2 - (n*lh)/2 + i*lh - int(20*scale)
        f += (f",drawtext={fontarg(cfg['font_bold'])}:textfile='{tf}':fontsize={int(84*scale)}:"
              f"fontcolor=0xf4ead8@0.96:x=(w-text_w)/2:y={int(y)}:"
              f"alpha='if(lt(t,{0.3+i*0.35}),0,if(lt(t,{1.3+i*0.35}),(t-{0.3+i*0.35}),1))'")
    if seg.get("sub"):
        tf = textfile(f"card{idx}_sub", seg["sub"])
        f += (f",drawtext={fontarg(cfg['font'])}:textfile='{tf}':fontsize={int(36*scale)}:"
              f"fontcolor=0xc9b48a:x=(w-text_w)/2:y={int(H/2 + n*lh/2 + 10*scale)}:"
              f"alpha='if(lt(t,1.2),0,if(lt(t,2.0),(t-1.2)/0.8,1))'")
    f += f",fade=t=out:st={dur-0.5}:d=0.5,format=yuv420p"
    run(["-f", "lavfi", "-i", f, "-t", str(dur), "-c:v", "libx264", "-crf", "18",
         "-pix_fmt", "yuv420p", str(out)])

def render_title(seg, cfg, out, W, H, scale):
    fps = cfg["fps"]; dur = seg["dur"]; frames = int(dur*fps)
    plate = source_for(seg)
    if plate.exists() and not is_video(plate):
        base = ["-loop", "1", "-framerate", str(fps), "-t", str(dur), "-i", str(plate)]
        f = (f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},"
             f"zoompan=z='1+0.06*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
             f":d={frames}:s={W*2}x{H*2}:fps={fps},scale={W}:{H},{GRADE},"
             f"eq=brightness=-0.18,gblur=sigma=2")
    else:
        # Placeholder plate: deep blue-black gradient with drifting grain
        base = ["-f", "lavfi", "-i",
                f"gradients=s={W}x{H}:c0=0x0a1a2a:c1=0x02050a:c2=0x14263a:x0={W//2}:y0={H//3}:x1={W//2}:y1={H}:d={dur}:r={fps}"]
        f = f"noise=alls=22:allf=t+u,gblur=sigma=1.2,eq=contrast=1.1"
    big = textfile("title_big", seg["big"])
    f += (f",drawtext={fontarg(cfg['font_bold'])}:textfile='{big}':fontsize={int(190*scale)}:"
          f"fontcolor=0xe9c982:borderw=1:bordercolor=0x3a2a10:x=(w-text_w)/2:y=(h-text_h)/2-{int(110*scale)}:"
          f"alpha='if(lt(t,0.4),0,if(lt(t,1.6),(t-0.4)/1.2,1))'")
    for i, line in enumerate(seg["lines"]):
        tf = textfile(f"title_l{i}", line)
        f += (f",drawtext={fontarg(cfg['font'])}:textfile='{tf}':fontsize={int(50*scale)}:"
              f"fontcolor=0xf3e2c8:x=(w-text_w)/2:y={H//2 + int((100 + i*68)*scale)}:"
              f"alpha='if(lt(t,{1.8+i*0.4}),0,if(lt(t,{2.6+i*0.4}),(t-{1.8+i*0.4})/0.8,1))'")
    sub = textfile("title_sub", seg["sub"])
    f += (f",drawtext={fontarg(cfg['font'])}:textfile='{sub}':fontsize={int(32*scale)}:"
          f"fontcolor=white@0.8:x=(w-text_w)/2:y={H-int(80*scale)}:"
          f"alpha='if(lt(t,3.0),0,if(lt(t,3.8),(t-3.0)/0.8,1))'")
    f += f",fade=t=out:st={dur-1.2}:d=1.2,format=yuv420p"
    run([*base, "-t", str(dur), "-vf", f, "-c:v", "libx264", "-crf", "18", "-r", str(fps), str(out)])

def main():
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]
    quality = "final"
    if "--quality" in sys.argv:
        quality = sys.argv[sys.argv.index("--quality") + 1]
    cfg = json.loads((HERE / "shots.json").read_text(encoding="utf-8"))
    cfg["font"] = os.environ.get("TRAILER_FONT", cfg["font"])
    cfg["font_bold"] = os.environ.get("TRAILER_FONT_BOLD", cfg["font_bold"])
    FW, FH = cfg["size"]
    if quality == "draft":
        FW, FH = 960, 540
    scale = FW / 1920
    # active picture is 2.39:1; bars are added at the join
    W = FW
    H = int(round(FW / cfg.get("letterbox", 2.39) / 2)) * 2
    bar = (FH - H) // 2
    SEG.mkdir(parents=True, exist_ok=True)
    segs = []
    for i, seg in enumerate(cfg["segments"]):
        name = seg.get("slot") or f"{seg['type']}_{i:02d}"
        out = SEG / f"{i:02d}_{name}.mp4"
        segs.append((seg, out))
        if only and only != name and out.exists():
            continue
        print(f"render {i:02d} {seg['type']:6s} {name} ({seg['dur']}s)", flush=True)
        if seg["type"] == "shot": render_shot(seg, cfg, out, W, H, scale)
        elif seg["type"] == "card": render_card(seg, cfg, out, i, W, H, scale)
        elif seg["type"] == "title": render_title(seg, cfg, out, W, H, scale)

    xf = cfg["xfade"]
    inputs = []
    for _, out in segs: inputs += ["-i", str(out)]
    fc = []
    prev = "[0:v]"
    total = segs[0][0]["dur"]
    for i in range(1, len(segs)):
        offset = total - xf
        lab = f"[v{i}]"
        fc.append(f"{prev}[{i}:v]xfade=transition=fade:duration={xf}:offset={offset:.3f}{lab}")
        total = offset + segs[i][0]["dur"]
        prev = lab
    fc.append(f"{prev}pad={FW}:{FH}:0:{bar}:color=black,format=yuv420p[vout]")
    audio = HERE / cfg["audio"]
    if not audio.exists():
        sys.exit(f"no music bed at {audio}; run scripts/make_bgm.py first")
    fc.append(f"[{len(segs)}:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=1.5,"
              f"afade=t=out:st={total-4:.3f}:d=4[aout]")
    final = OUT / ("trailer_7620.mp4" if quality != "draft" else "trailer_7620_draft.mp4")
    run([*inputs, "-i", str(audio), "-filter_complex", ";".join(fc),
         "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", f"{total:.3f}", str(final)])
    print(f"wrote {final}  ({total:.1f}s, {len(segs)} segments, picture {W}x{H} in {FW}x{FH})")

if __name__ == "__main__":
    main()
