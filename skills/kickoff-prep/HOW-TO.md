# Kickoff Prep — how to use it

For the lead running a new client's kickoff call. You use this twice: once before the
call, once after.

Everything it makes lands in the client's **Perm File** folder, so nothing lives on your
computer and anyone on the team can find it.

---

## Before the call

**1. Open Co-Work and point it at the client's Drive folder.**
Picking the folder is what gives it access — there's no login step and nothing to set up.

**2. Run `/kickoff-prep`.**

**3. Answer three quick questions.** It only asks what it can't find out for itself:

- Who's coming to the call, and when is it?
- Has anything come in since firm admin put the file together? *(This one matters — it
  keeps you from asking the client for something they already sent.)*
- Anything you already know you want to cover?

**4. It builds two documents.** A couple of minutes.

| Document | What it's for |
|---|---|
| **Kickoff Prep Notes** | Internal. Everything you need to know going in — billing, scope, who's who, the state of their books, what they're frustrated by, and anything our own records disagree on. **Don't share this or screenshare it.** |
| **Kickoff Call Agenda** | The eleven items you actually walk through with the client. Safe to have on screen. |

**5. Read the prep notes.** Once through is enough.

**6. Open QuickBooks and look at their accounts.** It will ask you to. This part isn't
optional and it isn't busywork — you'll see things the file can't tell you. Bring your
questions back to Co-Work and it adds them to the agenda.

**The skill is a head start, not a substitute for looking at the books yourself.**

**7. Open the agenda and run your call from it.**

---

## During the call

- Work down the eleven items in order.
- **Item 6 is a checklist** — tick each one off as the client gives it to you or commits
  to it. That's how you see what's still missing while you still have them on the phone.
- Type into the *Notes* space under any item. Anything you write there gets picked up
  afterward, so jot freely.

---

## After the call

**1. Download the Gemini notes as a Markdown file.** In the notes doc: **File → Download →
Markdown**.

**2. Upload that file to Co-Work and run `/kickoff-prep` again.**

You don't need the same conversation you used before the call, and there's nothing
different to type. Run the same `/kickoff-prep` — because you've given it a transcript, it
knows the call has happened and picks up from there. Starting a fresh Co-Work session is
completely fine; it reads what it needs from the client's folder.

**3. It does three things:**

- Fills your **prep notes** into the record of the call — what was answered, what's still
  open, and what the call never got to. Those are three different things and it keeps them
  separate.
- Marks every item you were collecting as **received**, **in flight**, or **still needed**.
- Drafts the **recap email** to the client.

**4. Read the recap email before you send it.** Especially any part where you told the
client you'd come back to them on something.

**5. Send it yourself.** The skill never sends email — it only drafts.

---

## Things worth knowing

**It won't stop because something's missing.** If firm admin's file is missing a piece —
billing figures, say — it builds anyway and lists what to ask her for. You can prep a whole
call without it.

**It will stop if the folder looks wrong.** If the client name in the folder doesn't match
the file inside it, it stops and asks. That's deliberate: it would rather build nothing
than build the wrong client's call sheet.

**Edit the documents freely.** They're yours. If you re-run the skill it backs up your
version first, so you won't lose notes.

**It never prices anything.** If a client asks for something outside the engagement — a tax
return, board meetings — it flags it for your controller and the firm owner, and writes the
recap so you're acknowledging the question without committing the firm. Don't add a price or
a start date yourself.

**It won't write down passwords.** Clients read logins out loud and Gemini captures them.
The record will say a credential was provided and where it went, never what it was.

**Don't trust the transcript on names.** Gemini garbles them and sometimes lists people who
weren't there. The skill checks names against the file, but glance at them.

---

## If something's not right

| What you're seeing | What to do |
|---|---|
| It says a document is missing | Ask firm admin for it — the message names the exact file |
| It stopped and asked about the folder | Check you picked the right client, then tell it to continue |
| A figure looks wrong | Trust the signed engagement over anything else, and tell your controller |
| It asked you to review QuickBooks but there's no file yet | Say so — for new QBO builds there's nothing to review, and it'll move on |
| Something reads oddly in the documents | Tell your controller. The wording is fixable and worth fixing once for everyone |

---

## The short version

Before: point it at the folder, answer three questions, read the prep notes, look at
QuickBooks, run the call off the agenda.

After: download the transcript, upload it to a fresh Co-Work session or the same one, read
the recap, send it yourself.
