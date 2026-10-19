import sys
from pathlib import Path
import fitz

orig_doc = fitz.open("content/Solow_model/solow1956.pdf")
print("Original total pages:", len(orig_doc))

fidelity_passes = 0
total_checked = 0

for part_idx in range(1, 5):
    manifest_path = Path(f"work/parts/part_{part_idx:02d}/part_manifest_{part_idx:02d}.json")
    import json
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    slice_doc = fitz.open(manifest["slice_path"])
    page_map = manifest["page_map"]
    
    for local_p_str, info in page_map.items():
        local_p = int(local_p_str)
        global_p = info["doc_page"]
        
        orig_page = orig_doc[global_p - 1]
        slice_page = slice_doc[local_p - 1]
        
        # Render pixmaps at 150 dpi
        pix_orig = orig_page.get_pixmap(dpi=150)
        pix_slice = slice_page.get_pixmap(dpi=150)
        
        assert pix_orig.width == pix_slice.width, f"Width mismatch: {pix_orig.width} vs {pix_slice.width}"
        assert pix_orig.height == pix_slice.height, f"Height mismatch: {pix_orig.height} vs {pix_slice.height}"
        
        # Byte comparison of samples
        if pix_orig.samples == pix_slice.samples:
            fidelity_passes += 1
        else:
            diff_count = sum(1 for a, b in zip(pix_orig.samples, pix_slice.samples) if a != b)
            print(f"Part {part_idx} local {local_p} (global {global_p}): {diff_count} differing sample bytes")
        total_checked += 1
    slice_doc.close()

orig_doc.close()
print(f"[+] Slice Fidelity Check: {fidelity_passes}/{total_checked} pages 100% pixel-identical ({(fidelity_passes/total_checked)*100:.1f}%)")
