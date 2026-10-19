# 06 Prototype brief: "Your next screening", from report to reminder

Summary: This is a clickable prototype of one flow. The ophthalmologist states an interval; the customer sees it in the report, opts in to a reminder from their optician, and months later receives that reminder in the optician's name and books.
It serves the 2-week test in `05`: can customers state the interval, do they recognise the optician as sender, and would they opt in?
All names and addresses are fictional and the screens are labelled as such. Every medical sentence is a template placeholder pending medical sign-off. The brief ends with a self-contained prompt for Claude Design.

Inputs used: `05-decision-memo.md`, `04-options.md` (option B), `03-insights.md`, `data/customer-journey.md`, `data/constraints.md` (re-read 2026-10-19), `CLAUDE.md`, `reviews/06-prototype-brief-review.md`.

---

## Scope and fictional data
- **Who sees it:** the interval field, the box and the opt-in apply to all non-referral customers. The pilot metric counts only customers aged 40+, and test participants are 40+.
- **Fictional data:**
  - Customer: Renate Muster, 64, preferred language German. Result: unremarkable. No consent at booking.
  - Optician: Optik Beispiel, Musterstraße 12, Musterstadt.
  - Ophthalmologist: Dr. M. Muster.
  - Screening date: 14 Nov 2026. Stated interval: 24 months, so the next screening is due around Nov 2028.
- **Label:** every screen carries a small "Prototyp – fiktives Beispiel / Prototype – fictional example" label.
- **Salutation:** full name only ("Guten Tag Renate Muster"). Booking collects no title or gender.

## The flow (screens in order)

| # | Screen | Actor | Purpose |
|---|---|---|---|
| 0 | Evaluation form: interval field | Ophthalmologist | Where the interval comes from. Optional field, empty by default |
| 1 | E-mail 3 "Your result is ready" | Mirantus (service) | The existing service e-mail. It names the optician but carries no result and no interval |
| 2 | Report page + PDF page 1 box | Customer | Shows the result sentence, the snapshot note and the interval |
| 3 | Reminder opt-in on the report page | Customer | Unticked checkbox |
| 4 | Confirmation | Customer | What will happen, roughly when, and from whom |
| 5 | Reminder e-mail, ~4 weeks before the interval ends | Optician (sent by Mirantus on its behalf) | Optician as sender, plus a booking link |
| 6 | Booking page, optician pre-selected | Customer | Picks a slot; the flow ends here |

### Screen 0: evaluation form (excerpt)
- **Label:** "Next screening recommended in"
- **Options:** — (not set) / 12 months / 24 months / 36 months / Not applicable (referral)
  - The option set is a placeholder pending sign-off by the evaluating ophthalmologists.
- **Helper:** "Optional. Shown to the customer in plain language on page 1 of the report."
- **Rule:** when the result is referral_recommended, "Not applicable (referral)" is selected automatically and screens 2–6 don't apply.

### Screen 1: e-mail 3 (service message, minimal change)
- **From:** [current sender of e-mail 3, unchanged]
- **Subject:** EN "Your result is ready" / DE "Ihr Ergebnis ist da"
- **Body:**
  - EN "Hello Renate Muster, the result of your eye screening at Optik Beispiel on 14 November 2026 is ready."
  - DE "Guten Tag Renate Muster, das Ergebnis Ihres Augen-Screenings bei Optik Beispiel vom 14. November 2026 ist da."
- **Button:** [View my result] / [Ergebnis ansehen]
- **Not included:** no result, no interval, no reminder, no marketing.

### Screen 2: "Your result at a glance" box
This is the box at the top of the report web view, also printed on PDF page 1. It follows `preferred_language`; the prototype has a DE/EN toggle.
- **Heading:** EN "Your result at a glance" / DE "Ihr Ergebnis auf einen Blick"
- **Result sentence** (template per result category, **[needs medical sign-off]**):
  - Unremarkable:
    - EN "Dr. M. Muster found no abnormalities in the images from your screening on 14 November 2026."
    - DE "Dr. M. Muster hat in den Aufnahmen Ihres Screenings vom 14. November 2026 keine Auffälligkeiten festgestellt."
  - Minor findings:
    - EN "Dr. M. Muster noted minor findings. Details are in your report."
    - DE "Dr. M. Muster hat kleinere Befunde notiert. Details finden Sie in Ihrem Bericht."
- **Snapshot note:**
  - EN "This screening shows your eyes as they are today. It does not replace an examination by an eye doctor."
  - DE "Dieses Screening zeigt den heutigen Zustand Ihrer Augen. Es ersetzt keine Untersuchung beim Augenarzt."
- **Interval line** (only if screen 0 was filled) **[needs medical sign-off]**:
  - EN "Dr. M. Muster recommends your next screening in **24 months** (around November 2028)."
  - DE "Dr. M. Muster empfiehlt Ihr nächstes Screening in **24 Monaten** (etwa November 2028)."
- **Location:**
  - EN "Your screening location: Optik Beispiel, Musterstraße 12, Musterstadt"
  - DE "Ihr Screening-Standort: Optik Beispiel, Musterstraße 12, Musterstadt"
- **Below the box:** EN [Download full report (PDF, German)] / DE [Vollständigen Bericht herunterladen (PDF, Deutsch)]

### Screen 3: reminder opt-in
Shown only if the customer has no valid consent **and** the optician has opted in to reminders. Never pre-ticked. The result page is complete without it.
- **Checkbox:**
  - EN "Yes, Optik Beispiel may remind me by e-mail when my next screening is due. I can unsubscribe at any time."
  - DE "Ja, Optik Beispiel darf mich per E-Mail erinnern, wenn mein nächstes Screening fällig ist. Ich kann mich jederzeit abmelden."
- **Link:** EN "How we use your e-mail address" / DE "Wie wir Ihre E-Mail-Adresse nutzen" (placeholder privacy note)
- **Button:** [Save] / [Speichern]
- **Legal note:** the opt-in assumes that the report page counts as part of delivering the "result ready" service message. Legal must confirm this in week 1. Only customers who open the report see it.

### Screen 4: confirmation
- **After ticking:**
  - EN "Done. Optik Beispiel plans to remind you by e-mail around October 2028. You can unsubscribe in every e-mail."
  - DE "Erledigt. Optik Beispiel wird Sie voraussichtlich im Oktober 2028 per E-Mail erinnern. Sie können sich in jeder E-Mail abmelden."
- **Already consented at booking** (screen 3 hidden), **pending legal sign-off on consent scope**:
  - EN "Optik Beispiel plans to remind you by e-mail around October 2028. [Manage]"
  - DE "Optik Beispiel wird Sie voraussichtlich im Oktober 2028 per E-Mail erinnern. [Verwalten]"
  - [Manage] opens a stub: EN "Reminder settings: [Stop reminders]" / DE "Erinnerungen: [Erinnerungen beenden]".
  - If legal finds that booking consent does not cover reminders in the optician's name, this state shows the screen 3 checkbox instead.
- **Not ticked:** no confirmation and no nudge.

### Screen 5: reminder e-mail
- **From:** "Optik Beispiel"
- **Reply-to:** none, or the Mirantus service address. The optician receives no replies unless it chooses to.
- **Subject:** EN "Your next eye screening at Optik Beispiel" / DE "Ihr nächstes Augen-Screening bei Optik Beispiel"
- **Body (EN):** "Hello Renate Muster, at your eye screening with us on 14 November 2026, Dr. M. Muster recommended your next screening around November 2028. If you'd like, you can book a 15-minute appointment here:" [Book at Optik Beispiel] "Kind regards, your team at Optik Beispiel · Musterstraße 12, Musterstadt"
- **Body (DE):** "Guten Tag Renate Muster, bei Ihrem Augen-Screening am 14. November 2026 in unserem Geschäft hat Dr. M. Muster Ihr nächstes Screening für etwa November 2028 empfohlen. Wenn Sie möchten, können Sie hier einen 15-minütigen Termin buchen:" [Termin bei Optik Beispiel buchen] "Viele Grüße, Ihr Team von Optik Beispiel · Musterstraße 12, Musterstadt"
- **Footer:**
  - EN "You're receiving this because you asked to be reminded. Sent by Mirantus on behalf of Optik Beispiel. [Unsubscribe]"
  - DE "Sie erhalten diese E-Mail, weil Sie um eine Erinnerung gebeten haben. Versendet von Mirantus im Auftrag von Optik Beispiel. [Abmelden]"
- **Sign-off required:** the interval sentence is repeated outside the report, so it needs medical/legal sign-off. Fallback wording: EN "the date noted in your report: November 2028" / DE "das in Ihrem Bericht genannte Datum: November 2028".
- **Not included:** no price, offers, urgency or health warnings.

### Screen 6: booking
- The existing booking page, with Optik Beispiel pre-selected and name and e-mail pre-filled.
- **Slots:** Mon 6 Nov 2028 09:00, Tue 7 Nov 2028 10:30, Thu 9 Nov 2028 16:00. Button [Book] / [Buchen].
- **Confirmation:**
  - EN "Booked: Tue 7 Nov 2028, 10:30 at Optik Beispiel."
  - DE "Gebucht: Di, 7. Nov. 2028, 10:30 bei Optik Beispiel."

## Edge cases (states)
- **a. No interval set:** no interval line, no opt-in, no confirmation.
- **b. Minor findings:** the minor-findings result sentence is shown.
- **c. Already consented at booking:** screen 4's "already consented" state is shown (pending legal sign-off).
- **d. Optician not opted in:** no checkbox and no confirmation. **d overrides c.** The box still shows.
- **e. Referral recommended:** no box and no opt-in. The existing referral section is unchanged.
- **f. Unsubscribe from screen 5:**
  - EN "You won't receive further reminders from Optik Beispiel."
  - DE "Sie erhalten keine weiteren Erinnerungen von Optik Beispiel."
- **g. Optician leaves the programme before the reminder date:** the reminder is suppressed, with no Mirantus-branded substitute. Not built in the prototype.

## Moderator order for the 2-week test
1. On screen 3, record the opt-in decision without prompting.
2. After screens 2–4, ask: "When should you come back, and why?"
3. On screen 5, show the sender first and ask "Who sent this?". Only then reveal the footer.

## Deliberately left out
- Optician opt-in form and any optician-facing screen.
- SMS/WhatsApp/app.
- Full report translation.
- Risk-factor questions.
- Chain and mobile-unit variants.
- Prices and offers.
- Any generic "come every year" message.

## Copy rules applied
- The interval appears only in the ophthalmologist's name, and only if she set it.
- No diagnosis beyond the evaluation template; no treatment advice; no fear, urgency or red.
- The reminder carries the optician's name and goes only to customers with consent.
- Opt-in boxes are never pre-ticked and never required.
- The service e-mail stays a service message.

---

## Prompt for Claude Design (paste as is)

```
Build a clickable, mobile-first prototype (390px wide, also fine on desktop) of one customer flow for "mira", an eye-screening service offered at opticians. EVERYTHING IS FICTIONAL. Put a small persistent grey label on every screen: "Prototyp – fiktives Beispiel / Prototype – fictional example".

Style: calm, clean, trustworthy health style. White background, one muted teal accent, large readable type (min 17px body) for customers aged 40–70. No stock photos. No red, no warning icons. Add a small DE/EN toggle top-right that switches all customer-facing text. German is the default.

Fictional data:
- customer Renate Muster (always addressed by full name, no Mr/Ms)
- optician "Optik Beispiel, Musterstraße 12, Musterstadt"
- ophthalmologist "Dr. M. Muster"
- screening date 14 November 2026
- recommended interval 24 months (around November 2028)

Screens (link them in order with the buttons named):

0. "Evaluation form (ophthalmologist view)", desktop-style panel.
   - Field "Next screening recommended in", options: — (not set), 12 months, 24 months, 36 months, Not applicable (referral).
   - Helper: "Optional. Shown to the customer in plain language on page 1 of the report."
   - Note: "Not applicable (referral)" is preselected automatically for referral results.
   - Button [Submit evaluation] → screen 1.

1. E-mail. Sender shown as "[current mira sender]".
   - Subject: EN "Your result is ready" / DE "Ihr Ergebnis ist da".
   - Body: EN "Hello Renate Muster, the result of your eye screening at Optik Beispiel on 14 November 2026 is ready." / DE "Guten Tag Renate Muster, das Ergebnis Ihres Augen-Screenings bei Optik Beispiel vom 14. November 2026 ist da."
   - Button [View my result] / [Ergebnis ansehen] → screen 2.

2. "Report page". Top card titled EN "Your result at a glance" / DE "Ihr Ergebnis auf einen Blick", containing:
   - EN "Dr. M. Muster found no abnormalities in the images from your screening on 14 November 2026." / DE "Dr. M. Muster hat in den Aufnahmen Ihres Screenings vom 14. November 2026 keine Auffälligkeiten festgestellt."
   - EN "This screening shows your eyes as they are today. It does not replace an examination by an eye doctor." / DE "Dieses Screening zeigt den heutigen Zustand Ihrer Augen. Es ersetzt keine Untersuchung beim Augenarzt."
   - Highlighted line: EN "Dr. M. Muster recommends your next screening in 24 months (around November 2028)." / DE "Dr. M. Muster empfiehlt Ihr nächstes Screening in 24 Monaten (etwa November 2028)."
   - EN "Your screening location: Optik Beispiel, Musterstraße 12, Musterstadt" / DE "Ihr Screening-Standort: Optik Beispiel, Musterstraße 12, Musterstadt"
   - Below the card, a link: EN [Download full report (PDF, German)] / DE [Vollständigen Bericht herunterladen (PDF, Deutsch)].

3. On the same page under the card, an UNTICKED checkbox:
   - EN "Yes, Optik Beispiel may remind me by e-mail when my next screening is due. I can unsubscribe at any time." / DE "Ja, Optik Beispiel darf mich per E-Mail erinnern, wenn mein nächstes Screening fällig ist. Ich kann mich jederzeit abmelden."
   - Small link: EN "How we use your e-mail address" / DE "Wie wir Ihre E-Mail-Adresse nutzen".
   - Button [Save] / [Speichern] → screen 4.
   - The page must look complete without ticking.

4. Inline confirmation:
   - EN "Done. Optik Beispiel plans to remind you by e-mail around October 2028. You can unsubscribe in every e-mail." / DE "Erledigt. Optik Beispiel wird Sie voraussichtlich im Oktober 2028 per E-Mail erinnern. Sie können sich in jeder E-Mail abmelden."
   - Then a small grey label: EN "— 23 months later —" / DE "— 23 Monate später —".
   - Button [Show reminder] / [Erinnerung zeigen] → screen 5.

5. E-mail from "Optik Beispiel": optician name as sender, a small plain wordmark "Optik Beispiel", NOT the mira logo.
   - Subject: EN "Your next eye screening at Optik Beispiel" / DE "Ihr nächstes Augen-Screening bei Optik Beispiel".
   - Body EN: "Hello Renate Muster, at your eye screening with us on 14 November 2026, Dr. M. Muster recommended your next screening around November 2028. If you'd like, you can book a 15-minute appointment here:"
   - Button [Book at Optik Beispiel] → screen 6.
   - Sign-off EN: "Kind regards, your team at Optik Beispiel · Musterstraße 12, Musterstadt".
   - Body DE: "Guten Tag Renate Muster, bei Ihrem Augen-Screening am 14. November 2026 in unserem Geschäft hat Dr. M. Muster Ihr nächstes Screening für etwa November 2028 empfohlen. Wenn Sie möchten, können Sie hier einen 15-minütigen Termin buchen:"
   - Button DE: [Termin bei Optik Beispiel buchen].
   - Sign-off DE: "Viele Grüße, Ihr Team von Optik Beispiel · Musterstraße 12, Musterstadt".
   - Small footer EN: "You're receiving this because you asked to be reminded. Sent by Mirantus on behalf of Optik Beispiel. Unsubscribe" / DE: "Sie erhalten diese E-Mail, weil Sie um eine Erinnerung gebeten haben. Versendet von Mirantus im Auftrag von Optik Beispiel. Abmelden".
   - Make the footer collapsible: hidden until "Show details" / "Details anzeigen" is tapped.
   - Tapping Unsubscribe shows: EN "You won't receive further reminders from Optik Beispiel." / DE "Sie erhalten keine weiteren Erinnerungen von Optik Beispiel."

6. "Booking".
   - Optik Beispiel preselected; name and e-mail prefilled.
   - Three slots: Mon 6 Nov 2028 09:00, Tue 7 Nov 2028 10:30, Thu 9 Nov 2028 16:00.
   - Button [Book] / [Buchen] → confirmation: EN "Booked: Tue 7 Nov 2028, 10:30 at Optik Beispiel." / DE "Gebucht: Di, 7. Nov. 2028, 10:30 bei Optik Beispiel."

Add a "States" switcher for the test moderator: a visually separate grey bar at the bottom. It changes screens 2–4:
 a) No interval set: hide the interval line, the checkbox and the confirmation.
 b) Minor findings: replace the first sentence with EN "Dr. M. Muster noted minor findings. Details are in your report." / DE "Dr. M. Muster hat kleinere Befunde notiert. Details finden Sie in Ihrem Bericht."
 c) Already consented at booking: hide the checkbox and show EN "Optik Beispiel plans to remind you by e-mail around October 2028. Manage" / DE "Optik Beispiel wird Sie voraussichtlich im Oktober 2028 per E-Mail erinnern. Verwalten". "Manage/Verwalten" opens a small panel: EN "Reminder settings" with button [Stop reminders] / DE "Erinnerungen" with button [Erinnerungen beenden].
 d) Optician not opted in: hide the checkbox AND any reminder confirmation. This overrides c.
 e) Referral recommended: hide the whole "at a glance" card and the checkbox; show a neutral grey placeholder "Referral section (unchanged)".

Strict copy rules:
- Use the text exactly as given. The medical sentences are placeholders awaiting medical sign-off; do not reword them.
- Do not add health warnings, urgency, prices, offers, discounts, "every year" messages or any other medical statements.
- Do not pre-tick any checkbox.
```
