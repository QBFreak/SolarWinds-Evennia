# SolarWinds-Evennia

This is a fresh attempt at my SolarWinds MUD concept, this time with the
Evennia engine: https://github.com/evennia/evennia/.

## So what in the heck _is_ SolarWinds?

I've had an idea for a MUD for a couple of years now. It would focus on space
exploration and resource gathering. The world would be infinite or
near-infinite, and much of it procedurally generated.

I initially tried to start this project with the
[TinyMARE](http://mare.qbfreak.net/TinyMARE/WhatIsTinyMARE)
[engine](https://github.com/klynastor/tinymare), however it just wasn't made to
scale as big as I wanted. I found myself doing terrible things like trying to
hack on a secondary SQLite database. Even then, it still wasn't enough.

Later, I tried to use an engine a friend was writing, but it wasn't mature
enough nor was it likely to be any time soon. I finally resigned myself to
writing my own engine in Python, which turned out to be a larger undertaking
than I envisioned.

While on that quest, I stumbled across [Evennia](http://www.evennia.com/) and
it appeared to be exactly what I was searching for. Coding with Evennia has
been a big change for me, I'm used to building the game entirely in softcode,
with the hardcode of the engine spirited away where mere mortals (anyone who
isn't the engine developer) cannot easily access it, and any changes are
A Big Deal. Evennia on the other hand requires all coding activities take place
offline, and then the engine is simply restarted to apply the changes. It even
maintains player connections while this takes place. What I like the most about
it is the fact that it will work with large databases. I can configure it for
a MySQL backend and then create a truly massive world that encompasses many
solar systems with no problems. As a bonus, all the coding is done in Python,
something I'm fairly familiar with, and far less finicky than the TinyMARE
softcode parser. I have high hopes for this incarnation of SolarWinds.
I think I might have finally found the proper tools to construct my vision.

## The code

This is the base Evennia setup, with my modifications. There's a lot of code
and doc in the repo that came with Evennia. Some of the changes of note that
I've made are listed below:


| Directory | Contains |
|---|---|
| [typeclasses](typeclasses) | Changes to how Evennia works |
| [world](world) | Features I've added myself |
