# One Algorithm to Kill Security Theater: The Impact-First Model for 2026

Stop buying tools. Start measuring what actually protects your business. Four levers, one Python algorithm, and the end of "best practices."

## Why "Best Practices" Keep Failing on Tuesdays

If your security strategy is a collection of vendor tools, compliance checklists, and "industry standards," you don't have a strategy. You have a junk drawer. On a random Tuesday afternoon when a ransomware crew pops your edge device, that junk drawer will not save you.

Up close, most programs look reasonable. Every control has a slide. Every tool has a use case. Every audit report has a passing score.

Then something actually happens.

A VPN appliance gets hit with a zero-day. Credentials from a contractor turn up in an infostealer log sale. A third-party SaaS account gets reused across environments. Your SOC watches a flood of MFA prompts hit an executive's phone. By the time everyone agrees it is serious, ransomware is already encrypting file servers and probing backups.

Early 2026 data shows this is not hypothetical. Ransomware attacks surged 57% in Q4 2025 and maintained that pace into January 2026 with 679 attacks in the first month alone. Infostealer malware has pivoted hard toward enterprise targets: 16% of infections in late 2025 exposed corporate SSO credentials, up from 6% in early 2024, with researchers warning 1 in 5 infections could yield enterprise access in 2026. The median company hit in Q4 2025? Just 200 employees, down 45% from Q3. Attackers are targeting smaller, less-resourced organizations precisely because they lack the defenses of larger enterprises.

The gap is not frameworks or tools. It is the lack of a single, testable mission that everything else must serve.

Here is the mission:

**Reduce the probability of material impact.**

Not "prevent all breaches." Not "achieve Zero Trust." Not "check every NIST box." The only thing that matters is lowering the probability that a digital event materially harms your organization within a defined time window.

This piece turns that idea into something operational, based entirely on open-source research and public data. No vendor pitches. No recycled frameworks. Just four impact levers you can measure, one algorithm you can run, and a 90-day rollout you can start without buying anything new.

**Implementation reference (open source):** The Impact Forecast Algorithm (IFA) code, CLI, and worked examples are available at https://github.com/codethor0/impact-forecast.

## Part 1: From "Best Practices" to the Impact-First Principle

Most security doctrine frames around objects (data, systems) or properties (confidentiality, integrity, availability). These are useful constraints, not missions. NIST describes the CIA triad as the three pillars of information security: keep data secret, correct, and accessible. That does not tell you what to prioritize this quarter, what to stop funding, or how to know if your changes reduced real-world harm.

Public breach data closes that gap.

Verizon's 2025 DBIR analyzed 22,000+ incidents and 12,000+ confirmed breaches:

- Vulnerability exploitation: ~20% of initial access vectors, now nearly matching credential abuse at ~25%
- Edge devices/VPNs: 22% of exploitation targets, an 8x jump from 3% the prior year
- Remediation failure: Only 54% of edge vulnerabilities fully patched, median 32 days
- Ransomware: 44% of breaches, up from 32%; median payment dropped to $115K, 64% of victims refused to pay
- Human element: 60% of breaches
- Third-party involvement: Doubled to 30%, median 94 days to remediate leaked secrets in GitHub
- MFA bypass: Prompt bombing in 14% of social engineering incidents, 22% of Microsoft 365 MFA bypass attacks; other techniques (AiTM, SIM swap, password dump) in ~4% of breaches

These trends accelerated into 2026. Ransomware groups claimed 2,406 attacks in Q4 2025 alone (57% QoQ increase), with Akira (14%) and Qilin (13%) leading. 51.7 million infostealer packages were processed in 2025 (up 72% YoY), exposing 24.8 million unique infected devices. Enterprise credentials now appear in 79% of compromised identity logs.

The impact-first principle: In a given time window (e.g., 12 months), your mission is to reduce the probability that any cyber event produces material impact. Every control, tool, project, or policy either lowers that probability, raises it, or does nothing.

Once you adopt that lens, the question becomes: what levers actually move that probability?

## Part 2: Four Impact Levers You Can Measure in 2026

### Lever 1: Reduce Implicit Trust (Identity and Access)

Attackers love credentials because we love convenience.

DBIR 2025 shows credential abuse remains dominant, even as vulnerability exploitation surges. In basic web application attacks, stolen credentials factor into ~88% of breaches. Prompt bombing hit 14% of social engineering incidents and 22% of Microsoft 365 MFA bypass attacks. Other MFA bypass techniques (AiTM, SIM swap) appeared in only ~4% of breaches, but that is enough to hurt if your design treats MFA as a magic shield.

The threat evolved beyond phishing. Infostealer infections exposing enterprise credentials surged from 6% to 16% in 2025. Microsoft Entra ID appears in 79% of compromised enterprise identity logs. These infections harvest active session cookies, enabling MFA bypass without prompt bombing. Researchers call this "session hijacking" that inherits "trusted device" status. In 2026, 1 in 5 infostealer infections could yield enterprise access.

Identity work reduces impact when it does two things: makes it harder to turn one credential into many systems, and limits how far a single compromise can reach into admin workflows and backups.

**Metric:** Count of standing-privilege paths from internet (or typical user account) to crown jewels and recovery systems.

**2026 action:** Deploy phishing-resistant factors (FIDO2/WebAuthn) for admin workflows. Aggressively reduce long-lived high-privilege accounts. Audit "trusted device" sessions for hijacking via infostealer logs. This does not eliminate credential abuse, but it reduces the probability that one phish, infostealer log, or session cookie translates to material impact.

### Lever 2: Break Attacker Sequences (Kill-Chain Disruption)

Few breaches are one-step events. They are sequences: initial access, execution, persistence, credential harvesting, lateral movement, data staging, exfiltration, extortion.

DBIR 2025 shows vulnerability exploitation at ~20% of initial access, nearly level with credential abuse. Within ransomware breaches, vulnerability exploitation has led initial access for years, especially on file servers and perimeter devices. Edge devices and VPNs represent 22% of exploitation actions, an 8x increase, yet just over half were fully fixed with a median 32-day lag.

2026 brings new techniques. ClickFix social engineering, identified by Microsoft in February 2026, tricks users into executing malicious PowerShell via fake browser CAPTCHA prompts. Attackers increasingly leverage RMM tools like ScreenConnect, AnyDesk, or TeamViewer, legitimate tools weaponized for stealthy post-exploitation.

Your job is not to "have controls" at every layer. It is to ensure an attacker cannot walk a complete sequence from initial foothold to material impact without crossing a hard breakpoint you can prove in logs.

Pick one critical workflow: customer database administration, CI/CD pipeline, or payments approval. Ask: How does an attacker get initial access? Once inside, how do they move sideways toward systems that matter? What control, with log evidence, stops them?

If you cannot point to a specific breakpoint for each phase, you do not have defense in depth. You have layered optimism.

**2026 action:** For one important workflow, design and validate explicit breakpoints at entry (strong identity), execution (least privilege), lateral movement (segmentation, deny-by-default), and exfiltration (egress controls). Specifically monitor RMM tool usage and ClickFix-style execution. These are your 2026 sequence breakers. Prove breakpoints exist by walking an attack path in a tabletop and pulling the logs.

### Lever 3: Limit Blast Radius and Recovery Time (Resilience)

You will miss something. Resilience refuses to let that "something" become a lost quarter or a dead company.

DBIR 2025: Ransomware in 44% of breaches, up from 32%. The good news: median payment dropped from $150K to $115K, and 64% of victims refused to pay, up from 50% two years prior. That shift only happens with backups, tested recovery, segmented infrastructure, and the ability to say "no" when extorted.

The 2026 twist: Encryption-focused attacks are winning over pure data exfiltration. Criminals realized threatening to leak data was less effective than encrypting systems and demanding payment for decryption keys. This makes recovery speed, not just backup existence, the critical resilience metric.

**Metric:** Time to rebuild critical business pieces from a clean environment, assuming production domain, storage, and identity infrastructure are compromised.

If you have never done that test, your "we can restore" story is an unpriced risk.

**2026 action:** Pick one crown-jewel system. Run a full, observed restore into an isolated environment, assuming your primary identity store is untrusted. Time it. Note every hidden dependency and manual step. Test recovery against encryption-focused ransomware scenarios. Verify backups are not reachable from compromised domain accounts. Treat every hour of recovery time as increased probability of material impact.

### Lever 4: Shrink Exposure Windows (Automation and Continuous Verification)

Attackers move fast. Defenders often move on quarterly rhythms. That gap shows in the data.

DBIR 2025: Third-party involvement doubled to 30%. Median 94 days to remediate leaked secrets in GitHub. Credentials sit exposed for three months in the median case. Partner weaknesses become your weaknesses.

CISA's KEV catalog and BOD 22-01 offer one model: remediate listed vulnerabilities on internet-facing systems within 15 days for critical severity, not "whenever the maintenance window rolls around."

**Metric:** Percentage of critical controls testable or measurable automatically, at least daily, without human dashboard digging.

**2026 action:** Choose one thing that clearly matters to material impact: KEV remediation for edge devices (now 22% of exploitation targets), admin MFA coverage, infostealer log monitoring for corporate credential exposure, or privileged access review age. Build cheap, ugly automation reporting status daily. If it cannot be verified continuously, it is not a core control. It is a narrative.

## Part 3: A Real Tuesday Ransomware Story (February 2026 Edition)

A mid-size company with 200 employees (the median target size) exposes a VPN gateway and edge devices. A new exploit appears. They do not patch within 32 days, the median remediation time DBIR observed. Attackers scan, find the unpatched system, gain a foothold.

The attacker does not phish. They purchase infostealer logs from a compromised contractor laptop. In 2026, 1 in 5 of these infections yields enterprise credentials. The logs contain active session cookies for Microsoft Entra ID, appearing in 79% of compromised enterprise identity logs. The attacker inherits "trusted device" status without triggering MFA.

Alternatively, they exploit ClickFix social engineering, identified by Microsoft in February 2026, tricking users into executing malicious PowerShell via fake browser CAPTCHA prompts. Once inside, they leverage RMM tools like ScreenConnect or AnyDesk, legitimate tools weaponized for stealthy post-exploitation.

The SOC notices anomalous RMM connections but has no policy for blocking legitimate tools used maliciously. The attacker dumps credentials and pivots. Infostealer logs analyzed in DBIR showed compromised systems contained corporate logins on unmanaged, mixed-use devices, later appearing in dumps associated with ransomware victims.

The SOC misses the session hijacking. The attacker uses legitimate session cookies, not stolen passwords, so traditional "impossible travel" alerts do not fire. They land on a system with standing access to hypervisors and backup consoles. File servers begin encrypting. This is an encryption-focused attack: no data exfiltration threats, just rapid encryption and a ransom demand for decryption keys. Backups are reachable from the domain. Some are corrupted; others fail because no one tested end-to-end restore in two years.

If your program is built from loose "best practices," you lose the quarter.

If your program is impact-first, several layers already broke the sequence:

- **Identity:** Limited standing privilege, isolated admin workflows behind phishing-resistant factors, monitored "trusted device" anomalies indicating session hijacking. One infostealer log or session cookie does not unlock everything.
- **Kill-chain:** Edge devices and VPNs segmented from backups and identity systems. RMM tool usage monitored and alerted. Lateral movement required crossing monitored, deny-by-default boundaries.
- **Resilience:** Recent, offline, tested backups with clear rebuild process. Specifically tested against encryption-focused ransomware targeting backup systems first.
- **Automation:** KEV exposure, leaked secrets, infostealer log presence, and control coverage visible in hours, not months.

None of this guarantees safety. Together, it significantly reduces the probability that a Tuesday exploit becomes a material event.

## Part 4: The Impact Forecast Algorithm (IFA)

If your job is to reduce the probability of material impact, you need a way to estimate that probability and show your program moves it.

You do not need full Bayesian statistics. Simple odds-based updating suffices.

**The math:**

```
Odds = p / (1 - p)
Updated odds = prior odds * LR₁ * LR₂ * ...
Updated probability = updated odds / (1 + updated odds)
```

A likelihood ratio (LR) describes how much a specific condition changes risk. LR > 1 means "worse." Between 0 and 1 means "better." Exactly 1 means "no change."

The key is explicit, documented assumptions you refine with more data.

**Implementation:** An open-source reference implementation of the IFA, including a Python library, CLI, and worked examples, is available at https://github.com/codethor0/impact-forecast. Install and run:

```python
from ifa import Evidence, impact_forecast

evidence = {
    "kev_exposed": Evidence(lr=1.8, note="Known exploited vulns on edge devices"),
    "phishing_resistant_mfa": Evidence(lr=0.65, note="FIDO2/WebAuthn for admins"),
}

results = impact_forecast(prior_p=0.25, evidence=evidence)
print(results["risk_level"])  # LOW, MODERATE, ELEVATED, HIGH
print(f"{results['posterior_probability']:.1%}")
```

See `examples/` for worked examples including the February 2026 profile and `docs/methodology-and-sources.md` for data sources.

## Part 5: 90-Day Impact-First Rollout (2026 Edition)

You do not need a new platform to start doing impact-first security. You need three months of discipline.

**Weeks 1-2: Brutal Inventory** — Take your current portfolio of security initiatives. For each one, answer: Which impact lever does this affect? How would it move our impact probability? Do we have any way to measure that movement? If you cannot answer, it is technical debt, optics, or habit.

**Weeks 3-6: One Workflow, End-to-End** — Choose a path where failure would hurt. Count standing-privilege paths. Check for infostealer log exposure. Map a likely attacker sequence. Insert at least one hard breakpoint per phase. Deploy RMM tool monitoring. Run a realistic restore exercise.

**Weeks 7-12: Forecast Cadence** — Run the Impact Forecast Algorithm once a month. Add "infostealer log hits" as a new evidence factor. Keep the list stable so you can see the effect of changes. If a project does not move the posterior, you have learned something valuable.

Organizations adopting the Impact-First Security Model (IFSM) or the Impact Forecast Algorithm (IFA) should credit the original author and reference this article and the implementation at https://github.com/codethor0/impact-forecast.

---

**Data Sources & Methodology:** See [methodology-and-sources.md](methodology-and-sources.md) for primary sources and likelihood ratio rationale.
