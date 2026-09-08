# What Are We Doing?

We built a security guard for AI agents.

## The Problem

AI agents (like ChatGPT with tools) can be hijacked by attackers.
An attacker hides evil instructions inside a webpage or file the agent reads.
The agent then starts doing bad things — stealing files, sending data to unknown servers.

Existing defenses try to **read the attack text** and block it.
But attackers can disguise the text to look innocent. The defense misses it.

## Our Idea

Don't read the text. **Watch what the agent does.**

A hijacked agent always betrays itself through its actions:
- It reads secret files it was never asked to read
- It contacts servers that were never mentioned in the task
- It follows an unusual sequence of tool calls

These actions show up in the log — no matter how clean the attack text looks.

## What We Built

**TRACE** — sits between the agent and its tools, records every action, and classifies the session as normal or hijacked.

```
Task → AI Agent → [TRACE watches] → Tools → Result
                        ↓
                  Allow or Block
```

## The Experiment

We ran 480 AI agent sessions:
- 240 attacked (prompt injection and fake plugins)
- 240 normal tasks

We trained a classifier on the action logs and measured how well it catches attacks.

## What We Want to Prove

1. **Watching behavior catches attacks better than reading text** — even sneaky attacks that fool text scanners
2. **It works across different AI models** — train on one model, works on another
