# apfel one-liners (tested on a real Mac)

Reference these verbatim before inventing a new `apfel` shell pattern — they cover the common categories: live system info, git, clipboard round-trips, watch-and-announce, web/text, and quick lookups. Swap the prompt text as needed; the piping pattern is what matters.

## Live system info

```bash
ps aux | sort -k 3 -nr | head -5 | awk '{print $11, $3"%"}' | apfel "which app is using the most CPU"
lsof -iTCP -sTCP:LISTEN -n -P | head -15 | apfel "list which apps own which ports as a table"
df -h | apfel "which volume is fullest, one sentence"
vm_stat | apfel "explain my memory usage in plain english, one sentence"
du -sh */ 2>/dev/null | sort -rh | head -5 | apfel "which folders are eating most disk, one sentence"
ls -laS | head -10 | apfel "what are the biggest files here, just file names"
lsof -i -nP 2>/dev/null | grep ESTABLISHED | awk '{print $1, $9}' | head -10 | apfel "which apps are talking to the internet right now, short answer"
pmset -g batt | apfel "battery health and percent, one line"
```

## Git

```bash
git log --oneline -20 | apfel "summarize what I have been working on"
git log --oneline -5 | apfel "write a one-line release note based on these commits"
```

## Clipboard round-trips

```bash
pbpaste | apfel "fix grammar" | pbcopy
pbpaste | apfel "translate to japanese" | pbcopy
pbpaste | apfel "summarize in 3 bullets"
pbpaste | apfel "extract just the action items as a clean bullet list, no other text" | pbcopy
```

## Watch and announce (long-running, speaks when done)

```bash
sleep 1800 && apfel "tell me cheerfully my long task just finished, one short sentence" | say

until [ -e ~/Downloads/Report.pdf ]; do sleep 5; done
apfel "tell me my download just landed, one cheerful sentence" | say

while pgrep -q ffmpeg; do sleep 5; done
apfel "tell me cheerfully that my video encoding is done, one short sentence" | say

# half-hourly spoken standup
while sleep 1800; do
  git log --since="30 min ago" --oneline | apfel "summarize my last 30 minutes of work in one cheerful sentence" | say
done

# battery warning below 20%
while sleep 900; do
  P=$(pmset -g batt | grep -oE "[0-9]+%" | head -1 | tr -d %)
  [ "$P" -lt 20 ] && apfel "battery just dropped to $P percent, write one short sentence that is friendly but super urgent telling me to plug in NOW" | say
done

# poll a URL until it's live, then celebrate out loud
until curl -sf https://staging.example.com/health >/dev/null; do sleep 30; done
apfel "tell me cheerfully that my deploy is live and the URL is responding, one short sentence" | say
```

## Web and text

```bash
echo "hey can u send me docs asap" | apfel "rephrase politely"
curl -sI https://github.com | apfel "explain what happens at this URL in one sentence, based on the HTTP headers"
curl -s https://news.ycombinator.com | grep titleline | sed "s/<[^>]*>//g" | apfel "summarize hacker news today in one cheerful sentence" | say
echo '{"name":"alice","plan":"pro","credits":42}' | apfel "explain this JSON in one sentence"
```

## Quick lookups

```bash
apfel "what is 15% tip on 87.50, just the number"
apfel "regex for a valid email address, just the regex"
apfel "give me one find command that lists files larger than 100MB, just the bash command"
apfel "explain the command tar -xzvf file.tar.gz in one sentence"
apfel "git command to uncommit but not unedit my last commit, just the command"
apfel "explain this regex in one sentence: ^\d{3}-\d{4}$"
apfel "convert 'Sat Apr 27 2026 11:30' to ISO 8601 (YYYY-MM-DDTHH:MM:SS), reply only with the converted string"
apfel -f README.md "summarize in 3 bullets"
```

## Shell scripts bundled with apfel itself

Install apfel first, then grab individual scripts from `demo/` in the apfel repo: `cmd` (natural language → shell command), `oneliner` (plain English → pipe chain), `mac-narrator` (narrates system activity), `explain` (explain a command/error/snippet), `wtd` (what's this directory — instant project orientation), `gitsum` (summarize recent commits).
