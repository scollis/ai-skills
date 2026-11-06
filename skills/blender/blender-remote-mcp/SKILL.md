---
name: blender-remote-mcp
description: >
  Use when driving Blender on the user's Mac through the Blender MCP connector (execute_blender_code): renders, headless jobs, file transfer, Blender 5.x API gotchas.
---

# Driving Blender remotely via the MCP connector

The connector runs Python inside the user's open GUI Blender session (`mcp__remote-devices__Blender__execute_blender_code`, assign a dict to `result`). Lessons from building the SERF/AMF2 farm scene, the KAWG airport scene and the C-SAPR2 / AWOS / Challenger 850 assets (Blender 5.2, Apple M3 Max, Metal).

## Hard limits and how to live with them
- **Every call must return in < 60 s.** A timeout does NOT cancel the work on the Mac; only re-run if the call is idempotent (polling is fine, building objects is not). Poll with short loops (`for k in range(12): sleep(4)`), never one long sleep.
- **Never render synchronously in the GUI.** Start renders async (timer + `bpy.ops.render.render('INVOKE_DEFAULT', write_still=True)`), then poll in later calls with `time.sleep(<=45)`. Keep a reusable text datablock (e.g. `render_async`) with `start_render(...)` and `poll_render(wait)`.
- **When the user is working in the GUI ("don't interrupt the studio"), do everything headless and never touch the open scene.** Pattern: write `build_x.py` / `update_vN.py` / `render_x.py` next to the .blend, then launch one chained shell command with `subprocess.Popen(['/bin/bash','-c', cmd], start_new_session=True)`: `nice -n 10 blender -b --factory-startup --python build.py > build.log 2>&1 && grep -q SAVED build.log && ((nice -n 5 blender -b asset.blend --python render.py > render.log 2>&1 &); sleep 3; ./watchdog.sh)`. Every script ends with a sentinel print (`SAVED`, `ALL DONE`) that the chain and the poller key on.
- **Memory watchdog:** the user's GUI Blender can hold 20-30 GB (LES clouds). Run `watchdog.sh` (kills `render_*` jobs when macOS `memory_pressure` free < 20 %) alongside every headless render. Nested geometry-node instancing (instances of instances, e.g. live tree-leaf GN) explodes memory: bake variants to plain meshes first.
- Versioned scene updates: `update_vN.py` copies the current file to `checkpoint_v(N-1).blend` before `save_as_mainfile`. Orphan node groups (only used by instancers) get dropped on save: give them `use_fake_user`.
- **Chain follow-up steps inside the job script** (e.g. encode the MP4 at the end of the render script). A separate bash watcher (`while kill -0 PID`) launched from Blender silently never ran.
- Use `render.use_overwrite=False` + `use_placeholder=True` so a killed/slept job resumes. Laptop lid closed = sleep = render paused (not lost).

## Develop in the cloud container, push once
- `pip install bpy --break-system-packages` in the container gives the same Blender (5.2.3) as the Mac. Build and debug-render there with Cycles CPU (900x560, 16-24 spp, ~15 s/view) and iterate freely; only push the finished script to the Mac.
- Pushing code to the Mac: there is usually no connected folder, so the script text must travel inside the execute_blender_code call. Send the raw source as `r'''...'''` (never re-type base64), write it, and verify with md5 against the local file. For later edits send a **line-diff patch**: `difflib.SequenceMatcher(None, old_lines, new_lines).get_opcodes()` -> JSON list of `[i1, i2, new_text]`, applied in reverse order on the Mac after asserting the old file's md5, then assert the new md5. A 48 KB script change becomes a ~5 KB call.
- Keep a local copy of exactly what the Mac has (or recover it from an earlier tool-results spill) so the patch base matches.
- For local runs, rewrite the output path via an env var (`sed` the OUTDIR line into `build_local.py`).

## Getting images and files across
- Images: on the Mac `sips -Z 900 -s format jpeg -s formatOptions 55 in out`, return base64 in `result`. Anything > ~50k chars spills to a tool-results JSON file; decode it with python (`json.load(...)['result'][key]` -> base64) and composite several views into one contact sheet with PIL before reading it.
- Big binaries (e.g. a 3.3 MB PDF): base64 in 1.5 M-char slices across several calls; each spills to a file; concatenate and decode locally.
- Preferred path when available: the device bridge (`device_stage_files` / `device_commit_files`), but only inside a *connected folder*; if none is connected, use the spill-file route above rather than prompting.
- The container's proxy blocks many sites (e.g. bombardier.com, mesonet.agron.iastate.edu). The Mac usually can reach them: download there with `urllib.request` (User-Agent header) and pull across.
- `plt.imread(png)` row 0 = NORTH (top); Blender `image.pixels` row 0 = SOUTH. Mixing them flips imagery maps.

## Blender 5.x API gotchas
- GN modifier inputs: `getattr(md.properties.inputs, socket.identifier).value = v` (not `md['Socket_2']`). Iterate `md.node_group.interface.items_tree` to map names -> identifiers.
- ShaderNodeMix (RGBA): sockets `Factor_Float`, `A_Color`, `B_Color`, out `Result_Color`. FunctionNodeRandomValue: `Min`, `Max`, `Value`.
- Sky: NISHITA removed; use MULTIPLE_SCATTERING. Adaptive subdivision lives on the SUBSURF modifier.
- `sequence_editor.strips` (not `.sequences`). Set `image_settings.media_type` before `file_format`.
- Layered actions: fcurves under `action.layers[].strips[].channelbags[].fcurves`.
- Motion blur position is `scene.render.motion_blur_position`.
- `result` must be a dict (a bare string errors).
- Drivers: SINGLE_PROP variables on a root empty's custom props (`az_deg`, `gear`, ...); `frame` works in simple expressions.
- Text objects: the object matrix must be right-handed (x = reading direction, y = up, z = normal toward the viewer) or the text renders mirrored. Viewer on the aircraft's right side looking -X sees the nose (+Y) on their right.
- Parenting: set `matrix_parent_inverse` deliberately; Stretch To aims local **Y**.

## Render planning
- Measure before committing: render ONE representative frame headless with final settings, time it, give the ETA.
- Reference timings (M3 Max, heavy instanced landscape + volume haze): 960x540 24-32 spp ~15-20 s; 1920x1080 96 spp ~35-45 s; 3840x2160 160 spp ~110 s/frame.
- Motion blur: shutter 0.2 for fast pans. Disable deform blur on huge GN objects.
- Encode: separate `--factory-startup` job with a VSE image strip -> FFMPEG H.264.

## Working habits
- Keep reusable helpers as text datablocks or sidecar .py files; keep geometry builders as standalone scripts so assets can be rebuilt deterministically.
- Save checkpoints before and after each major change; tell the user if their open file is unsaved.
- Subagents / asset builds never touch the GUI scene: build headless, save to `assets/<kind>/<NAME>/<name>.blend` with a `<NAME>_root` empty carrying a `note` prop (origin, props, placement), preview cameras in a separate `*_Preview` collection; append only the asset collection into scenes.
- After any terrain/height change, shift every non-conforming object by the height delta at its XY.
- Always look at a render (and a close-up of every new feature) before reporting a change done.