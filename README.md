# Idea radar

A system for Claude that finds what your industry is talking about this week and hands
you content ideas with an angle that is yours.

Made by [Mad Hatter Films & Media](https://madhatter-films.com). It is a cut-down
version of the idea radar we run for our clients twice a week.

## What it does

1. **Setup (once, about ten minutes).** Claude interviews you: your field, who you want
   to reach, and what you believe. If you are not sure what you believe yet, it helps
   you find out. It then proposes three to six pillars to watch and saves a profile.
2. **Scan (whenever you want ideas).** Claude researches each pillar, opens and checks
   every story, and adds ideas to a spreadsheet. Each row has the story, the link, what
   happened, your angle, the belief it comes from, two hooks, the text for the screen,
   a format and why it is timely.

You end up with `~/idea-radar/ideas.csv`, which opens in Excel, Numbers or Google
Sheets. Pick a row, film it or write it. You can also hand a row back to Claude and ask
for a script.

## Install

You need Claude Code (in the terminal, or the Code tab of the Claude desktop app) with
web search available. It is not built for the ordinary Claude chat app, because your
profile and spreadsheet live in a folder on your computer.

**As a plugin (recommended, and you get updates).** In Claude Code, run these one at a
time:

```
/plugin marketplace add madhattermedia/idea-radar
```

```
/plugin install idea-radar@mad-hatter
```

**From the zip.** [Download idea-radar.zip](https://github.com/madhattermedia/idea-radar/releases/latest/download/idea-radar.zip),
unzip it, open a terminal in the unzipped `idea-radar` folder and run:

```bash
mkdir -p ~/.claude/skills && cp -R skills/radar-setup skills/radar-scan ~/.claude/skills/
```

Either way, start a new Claude session and say **"set up my idea radar"**.

## Use

- "Set up my idea radar" runs the interview.
- "Run my radar" runs a scan. A full scan takes a few minutes because every story is
  opened and checked.
- "Change my pillars" or "add a belief" updates your profile. You can also edit
  `~/idea-radar/profile.md` by hand.

In the spreadsheet, the Status and Notes columns are yours. Scans only ever add rows.

If your Claude app supports scheduled tasks, ask it to "run my radar every Monday and
Thursday at 7am" and the sheet fills itself.

## What it will not do

It will not invent a story, a statistic or a fact about your business. Where an idea
needs a detail only you know, it leaves a [gap in square brackets] for you to fill.

## Want it done for you?

We plan, film and edit this kind of content for founders and their teams.
[madhatter-films.com](https://madhatter-films.com)
