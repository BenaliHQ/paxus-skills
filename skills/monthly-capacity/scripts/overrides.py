"""
One-time bootstrap corrections — EMPTY BY DESIGN in the shipped skill.

These structures exist only to rebuild historical months from the old staff
scope spreadsheets. The monthly run reads everything it needs from the
CapacityIQ Data sheet, so in app mode every one of them is skipped.

Two reasons they stay empty here:

  1. Applying them in app mode would mask a genuinely new client — a client
     absent from the Clients tab must be FLAGGED, never silently corrected.
  2. They held staff pay-rate changes, a named person's unpaid-leave reason,
     departed employees, and client names. None of that belongs in a skill
     that syncs to the whole firm. The engine is shipped; the fuel stays in
     Drive.

Client name mappings that DO still apply going forward live in the sheet's
"Aliases" tab and are read by build_month.load_aliases().

If you ever need to rebuild history again, restore the populated copy from
the Capacity folder in Drive and run in bootstrap mode (app_path=None).
"""

# --- per-month daily-rate corrections: (person, period) -> hrs/working day ---
RATE_OVERRIDES = {}

# --- unpaid / uncoded time off: period -> {person: hours} -------------------
UNPAID_OFF = {}

# --- client identity (superseded by the sheet's Aliases tab) -----------------
QB_ALIASES = {}
CLIENT_RENAME = {}
CLIENT_MERGE = {}
CLIENT_DROP = set()

# --- business decisions carried by the sheet's Clients tab ------------------
CLIENT_STATUS = {}
CLIENT_BUDGET = {}
CLIENT_PENDING = {}

# --- roster corrections carried by the sheet's Assignments tab --------------
ROSTER_ADD = []
ROSTER_REPLACE = []

# --- staff carried by the sheet's Staff tab (status column) -----------------
STAFF_DROP = set()
STAFF_TBD_INTERN = set()
