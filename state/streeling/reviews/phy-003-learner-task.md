# PHY-003 learner transfer task

Give this sheet without PHY-003's answer blocks or its reviewer brief. The numbers below are a new **ideal-sampling thought experiment**, not a measurement of GA's guitar engine.

A test engineer proposes a four-second **native** mono guitar render at 32,000 samples per second. Separately, they propose generating a continuous 19,000 Hz sine and sampling it at 32,000 Hz *without an anti-alias filter* to validate their analysis script. They also have an older GAS-001 native WAV at 44.1 kHz and want to make a claim about the browser worklet.

Answer in your own words:

1. What is the 32 kHz Nyquist frequency, and how many mono samples are in the proposed four-second render?
2. At what in-band frequency would the deliberately unfiltered 19 kHz sine appear after 32 kHz sampling? Show the arithmetic.
3. Can either native WAV establish the sample rate used by an arbitrary browser AudioWorklet session? Name the measurement and provenance you would record.
4. Design one controlled comparison that could distinguish a predicted alias from a fixed in-band tone in a GA render. Hold at least two relevant conditions constant and name an observation that weakens the alias hypothesis.
5. State clearly which of your answers are mathematical predictions and which, if any, prove that GA currently emits an alias.

The reviewer will retain your unedited response and score it against the five criteria in the review brief. There is no recorded learner result yet.
