---
title: Situation router (which playbook to open)
category: core
tags: [meta, routing, index, decision-tree]
triggers: [which playbook, I'm not sure what this is, help me with a message, I need to send something, what do I say here, not sure how to respond]
summary: A decision tree from the user's situation to the one or two playbook ids to open. Use when the triggers of the individual entries do not match cleanly.
updated: 2026-09-27
---
# Situation router

Answer three questions, then open the entry named. When two branches apply, open both and blend. Entry ids are the file names without `.json`.

## Question 1: Is the user replying to something, or starting?

**Replying to a pasted message:** open `05-reply-to-a-pasted-message` first, then continue below with what the message is asking for.

**Starting the conversation:** continue below.

## Question 2: What is the user trying to do?

### Say no
- To an invitation, event, wedding, trip: `decline-invitation` (as the host saying no plus-ones, no kids, or cutting the list: `wedding-and-event-host-messages`)
- To a favour, loan, request for time or help: `decline-request`
- To a client asking for more work, a change, a rush: `say-no-to-client-scope`
- To a customer asking for a refund, exception, custom order, feature: `say-no-to-a-customer-request` (refunds specifically: `handle-refund-request`)
- To a job offer, or telling a candidate no: `decline-offer-or-candidate`
- To a meeting, a "quick call", a recurring sync: `decline-meeting-or-protect-time`
- To a boss's ask (stay late, take on more, an unrealistic deadline): `push-back-on-boss`
- To a romantic advance or a second date, early dating: `romantic-let-down`
- To an ex who wants to talk or get back together: `respond-to-an-ex-or-breakup-message`
- To a relative's pressure (marriage, kids, money, career): `family-pressure-and-nosy-questions`
- To a repeated intrusion on time, space, or feelings: `set-boundary`

### Ask for something
- Money owed to the user: `chase-late-payment` (between friends: `money-between-friends`)
- A favour, a small ask: `ask-for-favor`
- Help at work, or handing work to someone: `ask-colleague-for-help-or-delegate`
- More time on a deadline: `ask-for-extension`
- Time off, sick day, leave: `ask-for-time-off-or-sick-leave`
- An introduction or referral: `request-intro-or-referral`
- A reference, recommendation, testimonial from a person: `ask-for-reference-or-recommendation`
- A review or testimonial from customers: `ask-for-review-or-testimonial`
- A better price or a waived fee, as the buyer: `ask-for-a-discount-as-a-customer`
- Higher pay or a higher price, as the seller or employee: `negotiate-price-or-salary` (a raise or promotion in your current job: `ask-for-a-raise-or-promotion`)
- Someone to stop or change a behaviour: `ask-to-change-behavior` (a roommate, or chores, bills and guests in a shared home: `roommate-and-shared-living`; a neighbour, or escalating to the building or council: `neighbour-disputes`)
- A decision from a group: `group-chat-coordination`
- Someone to fix a problem they caused (landlord, contractor, shop): `landlord-tenant-and-service-providers` or `complain-as-customer`
- A co-parent to agree a swap, a handover time or a shared cost: `co-parenting-and-ex-logistics`
- A decision from someone senior, or a stuck problem unstuck: `escalate-an-issue`

### Apologise or own something
- Personal: `apologize`
- At work: `admit-mistake-at-work`
- As a business, in public: `public-apology-from-a-business`
- For being late, flaking, cancelling: `handle-no-show-or-lateness` (moving a plan in advance: `cancel-or-reschedule`)

### Deliver news
- Bad news to a person: `deliver-bad-news`
- News to a team the user manages (someone leaving or joining, a reorg, layoffs, a missed target, a new policy): `team-announcements-as-a-manager`
- Personal news, good or hard: `share-personal-news`
- A price increase or policy change to customers: `price-increase-and-customer-announcements`
- An order problem: `shipping-delay-or-out-of-stock`
- Resigning or leaving a group: `leave-or-quit-gracefully`
- Moving out of a rental, ending a lease early, or a landlord not renewing: `give-notice-to-a-landlord-or-tenant`
- Availability while away: `out-of-office-and-away-messages`

### Respond to heat
- Angry customer: `respond-to-angry-customer`; public negative review: `respond-to-negative-review`
- Criticism aimed at the user: `respond-to-criticism`
- Passive-aggressive tone: `respond-to-passive-aggressive`
- An argument in progress: `de-escalate-argument`
- Unsolicited advice: `respond-to-unsolicited-advice`
- A disagreement the user wants to voice: `disagree-without-conflict`
- A message that might be a scam or a hacked account: `suspicious-or-scam-message`

### Connect or warm up
- First message to a stranger, cold email, a pitch: `first-message-to-stranger`, `cold-outreach`
- Introducing yourself: `introduce-yourself`
- Small talk, keeping a chat alive: `small-talk`
- Someone the user has not spoken to in a long time: `reconnect-after-silence`
- Dating, from asking out to the text after date one: `ask-someone-out-and-early-dating`
- Thanks, praise, receiving praise: `give-and-receive-compliments` (a thank-you note or card for a gift, host, mentor or favour: `thank-you-notes`)
- A recruiter wrote: `respond-to-recruiter`; after a rejection: `respond-to-job-rejection`

### Support someone
- A death: `condolences-and-support`
- Someone just told the user about a diagnosis or health scare: `respond-to-difficult-health-news`
- A hard time that is not a death: `check-in-on-someone-struggling`

### Follow up
- No reply yet: `follow-up-unanswered`; a client who went silent: `handle-being-ghosted-by-client`
- After an interview or meeting: `follow-up-after-interview-or-meeting`

### Give feedback
- To a colleague or report: `give-feedback-to-colleague`
- To a friend, partner, family: `give-feedback-kindly`
- Something embarrassing they have not noticed (food in teeth, body odour, a typo in their post): `tell-someone-something-awkward`

### Sell or serve
- A DM asking about a product: `reply-to-customer-inquiry-dm`; adding to an order without pushing: `upsell-without-pushiness`
- The first message after someone buys, books or signs up: `customer-onboarding-and-welcome`
- A brand reaching out to a creator: `creator-brand-deal-reply`

### End something
- A relationship: `respond-to-an-ex-or-breakup-message` (only a few dates in: `romantic-let-down`)
- A conversation that will not end: `end-conversation-gracefully`

## Question 3: What is the temperature?

If the user is angry, hurt, or writing at night, first offer the one-line pause from `respond-to-criticism` ("I don't want to answer this while I'm upset, I'll reply tomorrow") and then the drafts. If the other person is in a different culture or language, also open `mixed-language-and-cultural-notes`. If nothing above fits, build the message from `01-principles` and say which principles you used.
