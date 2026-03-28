# Active Context

## Current Status
- **Recent Fixes**:
  - Fixed TikTok regex in `downloader.py` allowing subdomains like `vt.tiktok.com` and `vm.tiktok.com`.
  - Overhauled `/yarisma` in `quiz.py` to add interactive language and genre selection menus using Pyrogram callbacks.
  - Rewrote quiz snippet downloader to use python `yt_dlp` API natively with `download_ranges` to fix the 60-second timeouts and output 0-byte invalid files.

## Recent Changes
- `downloader.py`: Updated `RE_MEDIA` to allow any subdomain before `tiktok.com`.
- `quiz.py`: Complete rewrite of `/yarisma` command. Added multiple song pools (`TR_POP`, `TR_ARABESK`, `EN_POP`), inline callback menus, and direct `yt_dlp` slice fetching.
- `callbacks.py`: Restructured help callback to safely handle missing locale keys
- `youtube.py`: Complete rewrite of download function with multi-format fallback loop

## Work in Focus
- Stability improvements across all command flows
- YouTube download reliability improvements
- Ensuring all features work end-to-end without crashes

## Next Steps
1. Test all help menu buttons to ensure no missing key errors
2. Verify YouTube download works with the new format fallback system
3. Test quiz feature with new song pool
4. Consider adding missing keys to other locale files (ar, de, etc.)
5. Test playlist play command in group chats

## Active Decisions & Patterns
- Use `.get()` with fallback for all locale key access in dynamic contexts
- YouTube download uses progressive format fallback: specific → general → best
- Quiz downloads use opus format with timeout protection
- All `play_not_found` calls include `.format(config.SUPPORT_CHAT)` argument
