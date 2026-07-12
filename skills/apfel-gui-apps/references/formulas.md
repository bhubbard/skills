# apfelpad formula reference

Full list of `=name(args)` formulas apfelpad supports, grouped as in the app's own docs. Smart quotes, anonymous shortcuts, and auto-quoting (`=apfel(hello world)` auto-adds quotes) all work.

## On-device AI + math

| Formula | Does |
|---|---|
| `=apfel(prompt, seed?)` | On-device LLM call via `apfel --serve`. Same seed → same output. |
| `=(prompt, seed?)` | Anonymous shortcut for `=apfel(...)` — `=(hello)` canonicalises to `=apfel("hello")`. |
| `=math(expression)` | Arithmetic with US-style annotation, e.g. `=math($1,250 + $750)`, `=math(2m + 500k)`. |

## Dates and time

| Formula | Does |
|---|---|
| `=date(offset?)` | ISO 8601. `=date(+4)` four days ahead, `=date(-7)` a week ago. |
| `=weeknum(offset?)` | ISO calendar week, with offset. |
| `=month()` / `=day()` / `=time()` | Locale-aware month/weekday name, `HH:mm` time. |

## Text (Google Sheets–style, pure Swift)

`=upper(text)` `=lower(text)` `=trim(text)` `=len(text)` (grapheme count) `=concatenate(a, b, …)` `=substitute(t, f, r)` (first occurrence) `=split(t, d, i?)` `=if(cond, then, else)` (empty/0/false/no are falsy) `=sum(n1, n2, …)` `=average(n1, n2, …)`

## Document references and reactive variables

| Formula | Does |
|---|---|
| `=ref(@#anchor)` | Insert the text of a named heading section. `@#` = section reference. |
| `=count(@#anchor?)` | Word count of the whole doc or a named section. |
| `=input(name, type, default?)` | Declare a reactive variable; bind with `@name` elsewhere. |
| `=show(@name)` | Echo the current value of a bound variable. |
| `=clip()` | Current clipboard contents (text only). |
| `=file(path)` | Read a local text file, max 1 MB. |

## Logical

`=AND(e1, e2, …)` `=OR(e1, e2, …)` `=NOT(expr)` `=IFERROR(value, fallback)` `=SWITCH(expr, c1, v1, …, [def])` `=IFS(c1, v1, …)` `=TRUE()` / `=FALSE()`

## Extended text

`=LEFT` / `=RIGHT` / `=MID` (MID is 1-indexed, Google Sheets convention) `=FIND` (case-sensitive, 1-indexed) / `=SEARCH` (case-insensitive) `=REPT(text, n)` `=PROPER(text)` (title-case) `=CLEAN(text)` (strip control chars) `=EXACT(a, b)` `=CHAR(n)` / `=CODE(s)` `=TEXTJOIN(delim, ignore_empty, …)` `=VALUE(text)` / `=TEXT(value, [fmt])` (fmt: `0`, `0.00`, `0%`)

## Extended math

`=MAX` / `=MIN` / `=PRODUCT` `=ABS` / `=SQRT` / `=INT` / `=SIGN` `=EVEN` / `=ODD` / `=FACT` `=LN` / `=LOG10` / `=EXP` / `=LOG(v, [base])` `=MOD` / `=POWER` (alias `=POW`) `=GCD` / `=LCM` / `=COMBIN` `=ROUND` / `=ROUNDUP` / `=ROUNDDOWN` `=CEILING` / `=FLOOR` `=PI()` / `=RAND()` / `=RANDBETWEEN(lo, hi)`

## Extended date/time

`=NOW()` (`YYYY-MM-DD HH:mm`) `=YEAR()` `=WEEKDAY()` (1=Sunday…7=Saturday) `=HOUR` / `=MINUTE` / `=SECOND`

## Info / type-checking

`=ISNUMBER(value)` `=ISTEXT(value)` `=ISBLANK(value)` `=TYPE(value)` (returns `number`, `text`, or `blank`)

## Composition examples

```
=upper(=ref(@#intro))                              → HELLO WORLD
=upper(=trim(=lower("   HELLO   ")))                → HELLO  (three levels deep)
=concatenate(=upper("a"), "-", =lower("B"))         → A-b
=if(=math(5*5), "big", "small")                     → big  (25 is truthy)
=sum(=len("abc"), =len("de"), =math(10))            → 15
=apfel(=concatenate("summarize: ", =ref(@#intro)))  → AI reads the intro section
```

## Worked example: reactive freelance calculator

```markdown
=input("hours", number, "120")
=input("rate", number, "95")
=input("tax_rate", number, "20")
=input("discount", number, "0")

## Project Estimate

| Item | Value |
|------|-------|
| Hours | =show(@hours) |
| Subtotal | =concatenate("$", =math(@hours * @rate)) |
| Discount | =concatenate(@discount, "%") |
| After discount | =concatenate("$", =math(@hours * @rate * (100 - @discount) / 100)) |
| Tax | =concatenate("$", =math(@hours * @rate * @tax_rate / 100)) |
| **Total** | =concatenate("$", =math(@hours * @rate * (100 + @tax_rate) / 100)) |

This document has =count() words.
```

Typing a new value into the `hours` input field instantly re-evaluates Subtotal, Tax, Total, and every `=show` echo downstream. Full example: https://github.com/Arthur-Ficial/apfelpad/blob/main/Examples/Calculator.md
