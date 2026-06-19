---
created: 2026-06-19
tags: [research, inbox, auto-generated]
status: new
source: Two Minute Papers
source-type: Video
attention-score: 38
attention-tags: [standard]
blog-potential: low
published: 
video-url: https://www.youtube.com/watch?v=4wC8hnQawiA
---

# NVIDIA New AI Is An Efficiency Monster

## Zusammenfassung

Hmm, 30 billion parameters in a new open free AI model where images, video, and audio all work. Hmm, [clears throat] why? There are a bunch of other free systems around in this area like the amazing Gemma 4. So, what does this do better than those? Two words, throughput and cost efficiency....

## Quelle

- **Feed:** [Two Minute Papers](https://www.youtube.com/watch?v=4wC8hnQawiA)
- **Typ:** Video
- **Attention Score:** 38/100 (standard)
- **Blog-Potenzial:** LOW

## Vollstndiges Transkript

> Hmm, 30 billion parameters in a new open free AI model where images, video, and audio all work. Hmm, [clears throat] why? There are a bunch of other free systems around in this area like the amazing Gemma 4. So, what does this do better than those? Two words, throughput and cost efficiency. Okay, what does that mean in practice? Now, hold on to your papers, fellow scholars, because it processes almost 10 hours of video per hour. Whoo, that is nearly 10 times real time. That is insanely quick. Wow, almost three times faster than Gwen 3 Omni. And when processing documents, it gets up to seven times faster. To run it locally, you'll want something like this or a beefy desktop GPU. We're talking about 25 gigs of video memory, not something you run on your phone. And to run it in the cloud, I use Lambda. Okay, so how did they do that? Where's the magic sauce? Well, it does five things really well and one thing not so well. Dear fellow scholars, this is Two Minute Papers with Dr. Károly Zsolnai-Fehér. Well, one, member layers scale linearly with context length instead of quadratically. What does that mean? Well, it means you throw everything you got at it. The more documents you have, the longer video or audio you have, the bigger the advantage this one has. So, if you're running something online that processes those on a mass scale, this is going to be incredible. Two, when audio comes in, this side converts raw audio waves into tokens, but differently than elsewhere. Normally, you have a speech recognition model here. Those are often huge and expensive and strip away all emotion and tone from the input. But this one keeps all these data and still does the job well. So much cheaper than running a whole separate model like Whisper on top. Three, when you give it an image or video, many previous generation techniques smash it into a different aspect ratio. This one keeps it. Then, oh, look at this. Convolutions in 3D. Now we're talking. Many other techniques look at the vi...

*(Vollstndiges Transkript: 4717 Zeichen)*

## Nchste Schritte

- [ ] Review: Ist das Thema wirklich relevant? (Attention Score: 38)
- [ ] Nach knowledge/topics/ verschieben wenn etabliert
- [ ] Backlinks zu verwandten Notes hinzufgen

---
*Auto-generiert am 2026-06-19 15:35 — Inbox Note*
