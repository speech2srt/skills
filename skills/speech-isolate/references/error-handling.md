# Error Handling

| Error | Action |
|-------|--------|
| Volume does not exist | Run: `modal volume create speech2srt-data` |
| Modal run failed (auth error) | Run `modal setup` to re-authenticate |
| Modal run failed (other) | Paste Modal error output verbatim to user |
| No audio files found in upload | Report "no audio files found" and list which files were skipped |
| Volume put failed (permission) | Verify Modal token is still valid: `modal token new` |
| Model download failed (HF) | Set `HF_TOKEN` environment variable for higher rate limits |
