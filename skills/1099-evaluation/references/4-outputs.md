# Step 4: Outputs

Entry: the file written. Exit: everything below in the conversation, and the tracker rows
added. Round amounts in prose to the nearest hundred; exact amounts stay in the sheet.

## 4.1 Client email (text to copy; a Gmail draft only if this session has the person's own Gmail tool)

To the bundle's client contact; copy the lead or controller who isn't sending it. Ask only
for vendors at $2,000+ with no W-9 on file and no email in QBO. Add questions for payees
that need one (a landlord's name, what a payment was for, labor vs parts).

> Subject: W-9s needed for <year> 1099s – <Client>
>
> Hi <first name>,
>
> We're getting a head start on <year> 1099s. The vendors below were paid for services this
> year, and we don't have a W-9 on file yet. Could you send us an email address for each
> one? We'll send each of them a secure W-9 request through Tax1099 so you don't have to
> chase it.
>
> - <Vendor>
>
> <Questions, numbered, one sentence each.>
>
> **Please send these by <the Quick Reference W-9 cut-off; Monday, January 11, 2027 for the 2026 tax year>.**
> If we don't have the information by then, we can't guarantee timely filing of the 1099s
> for these vendors. Thank you so much!

Never send. A Gmail draft made through an API leaves off the person's signature: append it
from Gmail `settings.sendAs` (the default one).

## 4.2 Financial Cents note (paste)

> **MM/DD/YYYY: 1099 evaluation**
> Team: <controller> (controller), <lead> (lead). The evaluation file is in Taxes > 1099 > <year>.
> It covers <n> bank-paid vendors, <n> of them over $2,000.
> - <n> vendors are ready for 1099s with W-9s on file (subtasks under Review and submit).
> - Asked <client contact> for emails / questions (subtasks under the request task).
> - QBO fixes: <one line>.
> - Check Tax1099 for W-9s already on file before requesting.
> W-9 cut-off: <date>.

## 4.3 FC subtasks — this exact format, every time

One code block per parent task, the parent's name in bold above it, one item per line, no
bullets, numbers or commas between items. Pasting a block into FC makes one subtask per line.

**Under "Request W-9s or email addresses from client":**
```
<Vendor>
<Vendor> – <short question>
```

**Under "Review and submit 1099s in Tax1099":**
```
<Vendor> – 1099-NEC
<Vendor> – 1099-MISC Box 1 Rents
```

The second list holds only vendors whose W-9 is on file and that need a 1099. Tell the person
to add vendors to it as W-9s confirm them.

## 4.4 QBO fix list

One line each, nothing posted: Track payments for 1099 to check (1099 vendors) or uncheck
(corporations, excluded vendors); TIN to enter from a W-9 in Drive (1099 vendors only); a
W-9 attached in QBO but not in Drive (save it to `Taxes > W-9`); payees to add to no-payee
bank payments. Skip anything only cosmetic for a vendor that gets no 1099.

## 4.5 Controller's tracker

If the tracker doesn't exist: create `<year> W-9 Request Trackers` in Admin > 1099s if
missing, then `google.sheet.create` named `Tax1099 W-9 Request Tracker – <Controller>`, tab
`Requests`, header row: Client | Vendor (name in Tax1099) | Vendor email | Heads-up email
sent | W-9 requested in Tax1099 | Status | W-9 received | Saved to Drive | QBO updated |
Notes. Bold and freeze the header.

Add one row per vendor that will need a Tax1099 request with `google.sheet.update` into the
first blank rows, not `google.sheet.append`: the Saved to Drive and QBO updated checkboxes
are pre-filled far down the sheet, so an append lands below them. Several runs write to the
same tracker on the same day, so read column A **right before** the write, not at setup,
and write into the first row where A is blank. Leave the checkbox columns alone. Each row: the
client, the vendor name as it will be entered in Tax1099, its email if known, Status "Not
requested", and a note with the 2026 amount and what's pending ("Email requested from
<contact> — pending"; when the client email is confirmed sent, "Asked <contact> for email
MM/DD/YYYY"). Never fill "W-9 requested in Tax1099" — that is the controller's date. Don't
add vendors whose W-9 is already on file.

## 4.6 Summary to the person

Short: the file link; counts (YES / CHECK / NO, watch list); then the flags, numbered,
each one line, most material first. Then the outputs above.
