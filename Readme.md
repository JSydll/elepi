# elePi - Embedded Linux Learning on a RaspberryPi

> Follow the elephant on its learning journey to the depths of Embedded Linux development!
> 
> We have the first **adventure** already waiting for you, with little **quests** that allow you to
> collect experience before stepping up your game.


## How it works

The main idea is that you can tinker with an actual system to learn in a focused, rewarding way.
Instead of being faced with tons of new things all at once, you will be directed to look only at
specific parts of the system. After proving your learning success, you can advance to the next
objective.

Larger topics, such as "Navigating the Linux Userspace", are addressed in so called **adventures**.
Each of those is comprised from a set of **quests** that need to be solved in a predefined sequence.
After you completed all quests from an adventure, you can proceed to the next, more demanding adventure
and its quests.

### Solving quests

There are different types of quests:

- **Fix Me**:
  _You'll find the system in a somewhat broken state and need to figure out what should be fixed._
- **Capture The Flag**:
  _You need to analyze and/or modify the system to expose the quest solution._
- **Discovery**:
  _You need to use a certain Linux feature to complete the quest._

In all cases, you'll eventually retrieve a **solution code** - a string of **128 hex numbers**.
This can then be used to complete the quest with the help of the `elepictl solve <code>` command,
which will automatically bring up the next quest for you.


## Getting started

What you'll need:

- RaspberryPi 4 and SD card
- USB-to-Serial adapter
- one of the published elePi adventures
- means to flash the adventure on the card

Then, start by flashing the adventure image on the SD card and connecting everything.

As soon as the system has booted, you can login with `root` and no password (**this will change**).

For help on the current quest, just run
```bash
elepictl info
```
You can get some hints by using the `hint` command or try out a potential solution code of the current
quest by passing it to `solve`.


## About the project

This project aims to create a curated, gamified learning experience for everyone interested
in Embedded Linux development. By solving small quests, one after another, they can gather
hands-on experience with increasingly difficult or complex use cases, improving the individual
_time invest_ and resulting capabilities to actually _apply_ the learnings in a real-life project.


## Contributing

Feel free - no, feel warmly welcomed! - to add new quests and/or adventures!

Check out the [development docs](./doc/development.md) for implementation guidance and simply
open up a PR on GitHub as soon as you're ready.

For the sake of authenticity, please sign your commits with your real contact details.
