# Compensation Window Protocol

Version: v1.3

Definitions:

    debt word:
        A finite sequence a_0, a_1, ..., a_k where a_i = v2(3n_i + 1)

    escape threshold:
        log2(3)

    bad window:
        a contiguous window whose average debt is below log2(3)

    maximal bad window:
        a bad window that is not extended by one adjacent block while remaining bad

    recovery window:
        the shortest following window such that the combined average from the start
        of the bad window to the end of the recovery window reaches log2(3)

A bad window is recovered when:

    average(debt[bad_start : recovery_end]) >= log2(3)

The finite certificate records whether every detected maximal bad window in the selected frontier is recovered.
