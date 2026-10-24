# Visual diagnostics and inspector overlays (reference design)

Functional specification for diagnostic overlay rendering and control behaviour.

This page specifies the **observable visual diagnostics behaviours** of a commercial wildlife burst-culling
application. In the reference application, these diagnostic views enable users and reviewers to visually inspect
the spatial and numeric evidence driving the automated culling recommendations.

Numeric values and thresholds mentioned here are **starting points to re-fit** on your own corpus.

---

## 1. Diagnostics rail and control behaviour

In the primary full-frame lightbox / inspector mode, a collapsible vertical control panel is anchored on the
side of the image stage:

1. **Drawer modes**:
   - **Expanded drawer**: Displays titled toggle buttons for each diagnostic overlay, an inline help popover,
     a collapse toggle, and batch action buttons (re-run evidence models, export diagnostic asset bundle).
   - **Collapsed rail**: Shrinks to a narrow bar displaying rotated vertical text and an active-count badge
     indicating how many overlays are currently enabled.
2. **Overlay categories**:
   - **Structural overlays**: Subject bounding box, subject segmentation mask, eye keypoints & head pose.
     Any combination of structural overlays may be active simultaneously.
   - **Analysis heatmaps**: Local sharpness (focus) heatmap and local sensor noise heatmap.
     These two heatmaps are **mutually exclusive** (enabling one deactivates the other), but either may be
     combined with any set of structural overlays.
3. **Availability gating**:
   - Controls are disabled and dimmed if the corresponding evidence was not detected (e.g. no animal detected,
     no eyes identified, or no valid foreground mask).
4. **Action triggers**:
   - **Regenerate evidence**: Forces a re-run of upstream detection, segmentation, and pose models on the
     current frame and refreshes the overlays.
   - **Export diagnostics bundle**: Packages individual rendered overlay layers, the original clean preview,
     and a JSON summary of scores and model outputs into a portable archive.

---

## 2. Structural diagnostic overlays

### 2.1 Subject box
- **Visual presentation**: A high-visibility bounding rectangle highlighting the detected primary subject,
  accompanied by a small badge indicating the estimated percentage of the frame area occupied by the subject
  (e.g., `subject 5%` or `subject 10%`).
- **Behavioural role**: Allows the reviewer to verify which animal was chosen as the primary subject and whether
  the model correctly bounded the creature versus surrounding foliage.

### 2.2 Subject mask
- **Visual presentation**: The background pixels outside the detected subject silhouette are darkened with a
  semi-transparent veil (approximately 50–60% opacity), causing the animal subject to visually pop out.
  The outer perimeter / boundary of the subject is delineated with a bright contrasting contour.
- **Behavioural role**: Shows whether fine appendages (beaks, wings, legs, tails) and boundaries were included
  in the subject analysis or clipped into the background.

### 2.3 Eyes and head orientation
- **Visual presentation**:
  - Each detected eye is indicated with a concentric circular target marker and an estimated crop boundary.
  - The primary (sharpest / highest confidence) eye displays an anchored status badge with a qualitative rating
    word (`soft`, `ok`, `sharp`) and the raw numerical sharpness variance metric.
  - Secondary eyes are rendered with reduced visual weight and opacity.
  - An optional point marker highlights corroborated anatomical features (e.g. beak tip).
  - A directional glyph centered between the eyes or on the snout indicates the 3D head orientation
    (e.g. facing camera, facing profile left, facing profile right, facing away, or pitching up/down).
- **Behavioural role**: Directly explains why an eye visibility criterion received a high or low score by
  revealing whether the eyes were detected, whether they were sharp, and whether the head orientation
  penalised the score.

---

## 3. Analysis diagnostic heatmaps

### 3.1 Focus (sharpness) heatmap
- **Visual presentation**:
  - A chromatic heatmap overlaid on the image, typically restricted to the foreground subject mask.
  - A 3-stop color gradient represents sharpness levels:
    - **Red**: Soft / out of focus.
    - **Amber / Yellow**: Intermediate / acceptable sharpness.
    - **Green**: Critically sharp / in focus.
  - An informational legend pill in the corner of the view displays:
    1. A summary description with the ratio of subject sharpness compared to background sharpness
       (e.g., `Focus · subject 2.3x sharper than background · saliency mask`).
    2. A gradient reference bar with labels `soft` and `sharp`.
- **Computation concept**:
  - The frame is divided into small regular spatial cells (e.g. 16×16 pixels).
  - High-frequency edge energy (e.g. discrete Laplacian variance) is calculated per cell.
  - Cell values are normalized into the gradient range and smoothly interpolated across the subject pixels.

### 3.2 Noise heatmap
- **Visual presentation**:
  - A chromatic heatmap overlaid on the image, weighted by the subject mask.
  - A 2-stop color gradient represents high-frequency noise intensity:
    - **Cyan / Blue**: Clean / low noise.
    - **Red**: Noisy / high sensor grain.
  - An informational legend pill displays the regional average noise standard deviation
    (e.g., `Noise · σ avg 1.6 · saliency mask`), with a gradient reference bar labeled `clean` and `noisy`.
- **Computation concept**:
  - The frame is divided into regular spatial cells (e.g. 20×20 pixels).
  - High-frequency noise standard deviation $\sigma$ is estimated per cell using robust wavelet differences
    or median absolute deviation (MAD).
  - Values are normalized over typical camera sensor noise floors and smoothly interpolated across subject pixels.

---

## 4. Diagnostic sidecar caching

To ensure responsive review navigation without noticeable lag:
- The spatial grids (focus variance grid, noise estimation grid, downsampled run-length encoded mask,
  and subject/background contrast ratio) are computed during initial background folder processing.
- These lightweight summaries are cached alongside thumbnail assets as compact JSON sidecars.
- The UI loads these precomputed grids lazily upon opening the lightbox or selecting a diagnostic layer,
  avoiding any redundant ONNX model evaluation during standard culling review.
