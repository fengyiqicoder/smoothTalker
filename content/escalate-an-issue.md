---
title: Escalating an issue
category: work
tags: [escalation, skip-level, vendor, account manager, customer support, blocked, complaint]
triggers: [escalate to my manager, go over someone's head, escalate to skip level, escalate with a vendor, escalate a support ticket, my ticket is being ignored, ask to speak to a supervisor, escalation email, nobody is responding]
summary: Escalating to a manager, a skip-level, a vendor or a support tier without burning the person you go past, with the heads-up, the escalation email itself, and what to send when it is ignored.
updated: 2026-09-27
---
# Escalating an issue

## Goal
The decision-maker gets the facts, the impact and the one decision you need, in under a minute of reading. The person you escalated past hears it from you first and is not embarrassed.

## Structure
1. **Give the person a heads-up before you go around them.** One message: what you are escalating, why, and that it is about the timeline, not them.
2. **Subject line that states the ask and the deadline.** "Decision needed by Thu: vendor contract renewal."
3. **Facts.** What happened, with dates. No adjectives.
4. **Impact.** What it costs if unresolved: money, a date, a customer.
5. **What you have already tried.** Two or three lines. This is what earns the escalation.
6. **The specific decision you need, and by when.** One ask, one date.
7. **Close with your recommendation.** Make the yes easy.

## Principles
- Escalate the problem, not the person. "Open 11 days" is a fact. "Support is useless" is a fight.
- The heads-up is the whole difference between escalation and betrayal. Send it every time.
- A skip-level is the last resort inside your company. Try your manager first, and say in the email that you did.
- Give a real deadline tied to a real consequence. "By Thursday, because the release ships Friday" beats "ASAP".
- Keep it under 150 words. Escalation emails get read on phones between meetings.

## Examples

**Heads-up before escalating past a colleague:**
> Quick note so it doesn't come from someone else: I'm raising the API timeout issue with Lena today, because we're at day 11 and the client's go-live is Friday. Not a comment on you, I know your queue is stacked. I'll keep you copied.

**Escalation email to your manager:**
> Subject: Decision needed by Thu: Hollis go-live
> The Hollis integration has failed staging three times since the 14th (API timeouts, ticket #4471). Their go-live is Friday and the contract has a penalty clause if we miss it. I've worked with Ravi in platform daily and we've narrowed it to the auth service, but the fix needs a config change only Ops can make. I need you to approve Ops prioritising ticket #4471 today, ahead of the Q3 reporting work. My recommendation: approve, and I'll own communicating the slip on the reporting work.

**Skip-level, after your manager has not acted:**
> Hi Lena, I raised the Hollis go-live risk with Mark on the 16th and again on the 19th and I know he's stretched with the reorg. We're now two days from a contractual deadline and I need a decision on Ops priority that Mark hasn't been able to get. Could you either approve the priority change or tell me who can? Mark is copied. Details are in the thread below.

**Vendor account manager:**
> Hi Jordan, ticket #88210 has been open since 3 September with no update since the 10th. It's blocking our payroll export and our next run is the 27th. Your support team has asked for logs twice, which we've sent both times. Can you get an engineer assigned by end of day Wednesday and confirm here? If that's not possible, I need to know now so we can run payroll manually.

**Customer support escalation, as a customer:**
> This is my third contact about order #55120 (refund of $340, promised on 2 September). Case numbers so far: 55120-A and 55120-B. Please escalate this to a supervisor or the refunds team and confirm a date the refund will be issued. If I don't have a date by Friday, I'll raise a chargeback with my card provider.

**Escalating to a support tier, technical:**
> Requesting escalation to tier 2. Intermittent 502s on our production tenant since the 12th, roughly 3% of requests, reproduced with the curl command below. Impact: customer-facing checkout errors. Please assign an owner and share an ETA for first response.

**Closing the loop with the person you escalated past:**
> Update: Lena approved the Ops priority and the fix is in. I've made sure she knows the diagnosis was yours.

## Avoid
- Escalating without a heads-up. It will be found out, and it will be the thing remembered.
- Adjectives. "Unacceptable", "ridiculous", "shocking". They cost you credibility.
- Escalating with no ask. A complaint with no decision attached gets filed, not actioned.
- Copying half the company. Copy the people who can act and the one you went past.
- Threats you will not carry out. If you say chargeback, be ready to file it.
- Two problems in one email. One problem, one decision.

## If it goes badly

**The escalation is ignored:**
Wait one business day past your deadline, then reply on the same thread.
> Following up, the deadline I mentioned was yesterday. Are you the right person for this decision, or should I take it to someone else? Either answer helps.

**They say it is not a priority:**
> Understood. So I can plan, can you confirm in writing that we're accepting the [Hollis penalty / payroll delay] as the cost? I want to make sure that's a decision and not a default.

**The person you went past is upset:**
> I hear that it landed badly. I sent you the heads-up first because I didn't want you blindsided. I'd rather work this out with you than around you. Can we talk for ten minutes?
