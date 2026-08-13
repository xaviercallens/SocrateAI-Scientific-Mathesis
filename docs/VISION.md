# Vision — why Stream 0 exists

> *"…la mathesis universalis de Leibniz, le programme d'une notation formelle universelle au
> service de toutes les sciences, est littéralement la fiche de poste de ce stream 0."*
> — the repository's own description

Leibniz wanted two things, and they are usually remembered as one. The **characteristica
universalis** was a notation in which any thought could be written down exactly. The
**calculus ratiocinator** was a mechanical procedure for deciding whether what had been
written down followed. His slogan — *calculemus*, "let us calculate" — was the claim that
with both in hand, a disagreement becomes an arithmetic problem.

Three centuries later the second half arrived: Lean 4 and its kernel are a working *calculus
ratiocinator* for mathematics. The first half is still missing wherever a research program
spans more than one repository — which is exactly where SocrateAI lives.

## The concrete problem

Six streams run concurrently. They already share mathematics: the T-dual effective radius
`Reff(α,R) = max(R, α/R)` appears in Stream 1's Lean core as the geometric inspiration for a
Navier–Stokes cutoff, in Stream 4 as a rulial inversion, and in Stream 6 as the
`RulialInversionHook` that keeps a neural predictor off a singularity.

What they do **not** share is a way of saying *how well any of it is known*.

That gap has a measured consequence, not a hypothetical one. Stream 1 and Stream 5 both use
the letter **B** — one meaning "a program checked it in exact arithmetic", the other meaning
"a referee checked it in a journal". Artifacts already cross between those repositories.
The day a *claim* crosses with its letter attached, a citation becomes a computation and
nothing in either repository notices. `docs/TIER_CALCULUS.md` §1 has the quotations.

That is the whole job. Stream 0 is not a seventh scientific stream. It is the notation the
other six write their conclusions in, and the kernel that checks the writing.

## What Stream 0 actually ships

**A notation.** Five tiers in one linear order — `X < C < L < B < A` — plus an orthogonal
*evidence kind* that caps what a row may claim. The two axes were being conflated into one
letter, which is why the letter collided.

**A theorem about that notation.** A ledger is `Sound` when no claim is filed above anything
it directly cites. The kernel-verified result is that soundness then holds across the entire
**transitive** closure (`MX-A-0003`), so a Tier A claim's whole support set is Tier A
(`MX-A-0004`).

This is elementary mathematics, and that is the point. It is worth a kernel proof not because
it is hard but because it is *the property informal bookkeeping loses first*. Every stream
already checks the direct condition by eye when adding a row. None checks the closure — and
`B → B → L` is sound at every direct edge while still resting on literature.

**Three implementations that must agree.** The theorem in Lean; a Python reference checker;
an independent Rust checker with no shared dependency. Gate 3 runs the last two over an
enumerated corpus and fails the build if they disagree — *without adjudicating which is
right*, because that is a question for a human.

This is not belt-and-braces. It is the same discipline the streams apply to physics, turned
on the tooling: a result reproduced by one method is a result reported by one method.

## What Stream 0 refuses to be

**Not an oracle.** `Sound` is a consistency property of a *record*, not a soundness property
of the *science*. A ledger in which every row is Tier C is perfectly sound and completely
worthless. Whether a row deserves its tier is a human audit, unchanged by anything here.

**Not a license.** A green gate says a stream's records are internally consistent. It says
nothing about Navier–Stokes, K3 selection, or the universe (SPEC.md §7.9).

**Not an authority.** Stream 0 proposes; the streams dispose. The migration in
`docs/TIER_CALCULUS.md` §3 has been adopted by nobody, and Stream 0 will not file it as a
request until the observation behind it is Tier B — asking for a migration on the strength of
a Tier C reading would be the very error the document describes.

## The inversion worth stating plainly

Every other stream studies an object and records what it learns. Stream 0's object of study
**is the record**. That is why its first theorem is about ledgers rather than about geometry,
and why the ambition of the program is an argument for this discipline rather than an
exemption from it.

The streams are attempting a Millennium problem, a selection principle in the string
landscape, and a foundation model for physics. Programs that attempt things like that fail in
a characteristic way: not by making a false step, but by losing track of which steps were
verified — until a claim assembled from four provisional pieces is quoted as established, by
its own authors, in good faith, eighteen months later.

`calculemus` was never a promise that the calculation would succeed. It was a promise that
when it didn't, everyone would be able to see exactly where.
