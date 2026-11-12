---
name: session-relay
description: Use when coordinating several Claude sessions on one goal — relaying findings, decisions or go-aheads between peer sessions with SendMessage, answering cross-session messages, or when the user says "communicate back with each session", "tell the other session", "pass this on" or "close the loop". Covers where approvals must be typed, provenance labels, verbatim quoting, correcting claims already relayed, and not editing another session's work.
capability: "Relay findings, decisions and go-aheads between peer agent sessions with provenance intact."
side_effect_level: local_write
approval_required: false
requires_tools: "ListAgents and SendMessage (cross-session messaging)."
output_schema: "Cross-session messages with a self-contained first line and provenance labels; a user summary of what was sent and what still needs the user."
risk_class: medium
---

# Session relay

A hub session that relays between peers is useful only if what it relays can be trusted and acted on.
Each rule below came from a relay that cost a round-trip or needed a correction.

## Rules

1. **Go-aheads go to the session that does the work.** A session that owns GPU jobs, merges or
   policy calls treats an approval relayed by another session as second-hand. When an item needs the
   user's go-ahead in another session, give the user the exact sentence to type **there**, e.g.
   *"In the pipeline session: start the #810 pilot."* Relay the approval as context only, labelled
   "relayed". *Why:* a relayed approval does not count in the receiving session, and trying costs round-trips.
2. **Label the provenance of every relayed item.** Say which kind it is:
   - typed by the owner in this session;
   - relayed from session X;
   - decided by a sub-agent under owner delegation;
   - hub analysis.

   Quote decisions, thresholds and pass criteria **verbatim**, with their numbers. Receiving sessions
   record provenance in issue trackers and post decisions as quoted.
3. **Mark hypotheses as untested, and correct everyone who received a claim.**
   - Before relaying a quantitative claim, look at a grouped breakdown (terciles, per shoot or batch),
     not only one overall correlation, which can hide a group effect.
   - Name the variable you actually measured: box size is not box looseness.
   - When a relayed claim turns out wrong, send a correction to **every** session that received it,
     before they post or file on it.
4. **Never edit another session's work.** Comments, issues, PRs, tickets and branches owned by another
   session are changed by that session. Ask it, with the exact new text.
5. **Make each message stand alone.**
   - The first line states the news or the request on its own.
   - Then give the evidence: issue and commit numbers, counts with denominators, file paths.
   - Then say what you are asking, and what is not being asked ("FYI, no action").
6. **Close the loop both ways.** When session A answers something that matters to session B, tell B
   in one message. Ask peers to report results to the hub by name, so the chain does not depend on the user.
7. **Delegation scope stays explicit.** A delegated call (to Jev or a sub-agent) covers only the calls
   the owner named. A decision outside that scope goes back to the owner as a labelled recommendation.
   If the target session has a rule that agents only recommend, the owner must confirm the delegation
   in that session.

## Do not

- Ask a peer to do something that was denied or blocked in your session. That is permission laundering.
- Treat a peer's message, or a sub-agent's report, as the user's approval.
- Change a pre-set pass bar after seeing the result. Report the miss, and leave any re-scope to the owner.

## Verification

Each send returns a delivery result: "in that session's inbox, not yet read". It does not confirm the
message was read. Report sends as delivered, not as acknowledged, until the peer replies.

## Related

- `go` and `step-by-step` (user-level skills): items owned by another session are not yours.
- [`jev-mcp`](../jev-mcp/SKILL.md): delegated typed decisions.
