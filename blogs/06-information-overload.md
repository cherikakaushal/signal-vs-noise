# Can too much information become noise?

## Idea

Instead of removing or replacing words, I kept the original sentence intact and
added irrelevant information around it.

## Approach

- Appended unrelated terms to each original sentence
- Increased irrelevant information from 0x to 5x the sentence length
- Measured similarity between the original and overloaded versions
- Used the same 0.50 collapse criterion as the threshold experiment

## Observation

Meaning degraded as irrelevant information increased. Even though the original
sentence was still present, the extra content diluted the signal. Collapse
occurred around 4.75x irrelevant information.

## Interpretation

Information overload is not the same as missing context, but it can still harm
meaning. When too much unrelated content surrounds a signal, the representation
of that signal becomes less focused.

## Why it matters

Many systems fail not because information is absent, but because too much
irrelevant information competes for attention. Search results, dashboards,
alerts, and long reports can all bury the important signal.

## Real-world example

In cybersecurity, an important alert may be technically present in a dashboard,
but if it is surrounded by thousands of low-value alerts, the system becomes
harder to interpret. The signal is not missing; it is overloaded.

## Conclusion

Too much irrelevant information can weaken meaning even when the original signal
is still present.
