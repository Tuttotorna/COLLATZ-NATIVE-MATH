# Refined Collapse Taxonomy

v0.6 refines the collapse taxonomy.

A cheap regeneration chain can fail through:

    terminal_descent
    post_chain_overcompensation
    delayed_compensation
    debt_spike
    soft_debt_break
    failed_regeneration
    weak_regeneration
    shadow_exhaustion
    end_of_chain_without_escape

The classifier uses priority order.

This is important because multiple flags can be true.

For example, an episode can show both:

    debt_spike
    post_chain_overcompensation

The primary cause is the highest-priority detected mechanism.

---

## Native interpretation

The collapse of a cheap regeneration chain can happen in different ways:

    it overpays compression immediately
    it pays compression gradually
    it fails to regenerate cheaply
    it regenerates, but not enough
    it exhausts shadow
    it terminates
    it breaks chain continuity

A future proof path would need to show that every infinite positive trajectory must eventually hit at least one of these collapse mechanisms.

The CRC target becomes:

    no infinite cheap regeneration chain can avoid the refined collapse taxonomy forever.
