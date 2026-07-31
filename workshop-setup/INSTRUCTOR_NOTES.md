# Instructor Notes — SignalFlow 101 · .conf26

This document is for the instructor. Attendees do not need to read this.

---

## Before the Conference (1–2 weeks out)

- [ ] Provision Splunk Show workshop instance
- [ ] Confirm realm, ingest token, API token, and participant alias distribution method (QR / URL)
- [ ] Generate participant aliases:
      ```
      python workshop-setup/generate_participant_aliases.py --count 200
      ```
- [ ] Run the live Splunk O11y smoke test:
      ```
      python workshop-setup/smoke_test_o11y.py
      ```
- [ ] Run `workshop-setup/build_dashboards.py` to create Fleet and Apdex dashboards
- [ ] Record the dashboard URLs and fill in the placeholders in `docs/EXERCISE_GUIDE.md`
- [ ] Generate participant aliases from `participant-001` through expected room capacity
- [ ] Confirm SignalFlow REST/SSE execution works from Codespaces
- [x] Confirm Apdex bucket counting uses latency values (`rollup='latest'`) rather than count rollups
- [ ] Verify detector URL format: `https://app.{REALM}.observability.splunkcloud.com/#/detector/v2/{id}`
- [ ] Confirm SignalFlow REST/SSE response parsing with real workshop data
- [ ] Run the chaos bot for 30 minutes and verify it appears correctly in the Fleet Dashboard
- [ ] Do a full dry run of all three exercises end-to-end, timed

## Day Before

- [ ] Start the chaos bot on a machine that will remain running through the workshop:
      ```
      python chaos-bot/chaos_bot.py
      ```
- [ ] Verify chaos-bot metrics are flowing in the O11y Fleet Dashboard
- [ ] Confirm Apdex score for chaos-bot is Poor (~0.50–0.55)
- [ ] Confirm Apdex scores for normal (clean) metrics are Excellent (~0.95+)
- [ ] Prepare credential distribution (print sheets / QR code slide ready)
- [ ] Test Codespace launch from a fresh GitHub account to verify attendee experience

## Day Of — Before Attendees Arrive

- [ ] Chaos bot is running and anomalous in the dashboard
- [ ] Fleet Dashboard and Apdex Dashboard are visible and loading
- [ ] Credential sheets / QR codes ready for distribution
- [ ] Slide deck loaded and presenting correctly
- [ ] Spare laptop with exercise doc open as instructor reference

## Workshop Timing

| Time  | Activity |
|-------|----------|
| 0:00  | Intro, SignalFlow framing, workshop overview |
| 0:10  | Credential setup — everyone opens Codespace and configures .env |
| 0:20  | **Checkpoint 1** — confirm everyone's metric visible in O11y |
| 0:22  | Exercise 2 begins |
| 0:35  | **Checkpoint 2** — discuss chaos-bot finding |
| 0:37  | Exercise 3 begins |
| 0:50  | **Checkpoint 3** — Apdex scores, chaos-bot confirmed |
| 0:52  | Demo: programmatic dashboard creation (instructor runs, attendees watch) |
| 0:55  | Take-home overview, repo resources, what's next |
| 0:58  | Q&A |

## Chaos Bot Parameters

The bot sends as `participant-000` with:
- Satisfied latency: 180-280ms (25% of requests)
- Tolerating latency: 650-900ms (55% of requests)
- Frustrated latency: 1400-2000ms (20% of requests, above 1200ms frustrated threshold)
- This produces Apdex ~0.50-0.55 (Poor) vs attendees at ~0.95+ (Excellent)

## If Things Go Wrong

**Codespace won't launch:** Direct attendees to the Google Colab fallback link in the appendix of the exercise guide.

**Metrics not appearing in O11y:** Check the `.env` credentials. The most common issue is a typo in the realm (e.g. `us1` vs `us0`).

**SignalFlow computation returns no data:** The 1-minute and 5-minute windows need data to fill. Wait a minute and try again.

**Chaos-bot not visible:** Confirm the bot is running, the `participant_id` dimension is exactly `participant-000`, and the Fleet Dashboard filter is set correctly.

## Post-Workshop

- [ ] Export and save any interesting dashboard screenshots for the slide deck
- [ ] Note any exercise steps that caused confusion for future refinement
- [ ] Shut down Splunk Show instance per Splunk Show decommission process
- [ ] Push final repo state to `github.com/splunk/signalflow101-conf26`
