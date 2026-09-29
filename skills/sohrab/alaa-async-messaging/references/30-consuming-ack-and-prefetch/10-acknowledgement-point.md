# The acknowledgement point

## The acknowledgement point

**A consumer acknowledges after its receipt row and its business effect have committed, and never before.**
This is the kit's own ordering contract for `mqkit`: receipt and business effect commit first, broker
acknowledgement second.

The reason is the crash window, and it is asymmetric:

- **Ack first, commit second.** A crash in the window loses the message. The broker has been told the work
  is done, no redelivery will occur, and nothing in the system records that the work is owed. This failure
  is silent and permanent.
- **Commit first, ack second.** A crash in the window redelivers the message. The handler runs a second
  time, the receipt row's uniqueness constraint recognises the duplicate, and the effect happens once. This
  failure is visible in the duplicate counter and is already made safe by the redelivery rule.

**Automatic acknowledgement is never enabled on a consumer that changes state.** Auto-ack acknowledges on
delivery, before the handler has run at all, so every message in flight during a crash is lost — it is the
ack-first window widened to the whole handler.
