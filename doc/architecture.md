# Introduction and goals

The primary goal of this project is to
> build a device to learn Embedded Linux in a hands-on, guided and fun manner.

Given it's widespread distribution, the RaspberryPi 4 SBC was pre-selected.

And to bring in both the guidance and fun factors, the projects follows a gamification
approach by breaking down partial learning objectives into a sequence of riddles (quests)
to be solved by the learner.

## Main user stories

As an **Embedded Linux learner**, I want to...
- follow a defined and reasonable learning path.
- start with the basics and dig deeper over time.
- use cheap or easily accessible hardware.
- focus on experimenting, i.e. avoid non-learning time such as waiting for downloads.
- start from a clean and reproducible state.
- be able to reset to the clean state if I mess up.

As a **contributor**, I want to...
- reuse a common build infrastructure.
- follow clear instructions on how to add new quests or adventures.
- know what I need to implement and in which format.
- be able to 'inject' new quests into an existing adventure.

## Requirements overview

The **learning device** shall...
- provide a commandline utility to get guidance on the currently active quest and adventure.
- persist the learner's progress, i.e. create a 'track record'.
- prevent 'cheating', i.e. hide away the persisted progress.
- allow to undo any changes introduced by the learner.
- skip already solved quests (e.g. after reboot).
- allow to deploy new releases of quests and adventures.
- allow to export/import the track record.

A **learning quest** shall...
- not have side-effects on another quest.
- be self-contained (for its deployment).
- leave no data on the system on removal or completion.
- be only be solvable in a specific order within the adventure.

The **build and development infrastructure** shall...
- support developer specific host environments.
- be based on an LTS release of Yocto.
- provide base class(es) to...
  - create learning adventures consisting of one to many quests.
  - ease up the specification of quest environment dependencies.
  - hide away quest identification and ordering.
  - create quest packages.
  - deploy an adventure image.

## Quality goals

The two major quality attributes are being **usable** and **operable/extendable**.

In terms of usability, low waiting times, enough guidance and an intuitive flow through
solving the quests are some of the aspects to consider.

The operability and extendability rather refers to the support provided for developers
of quests to extend the project.

## Stakeholders

As primary **users** of the device, the following target group is supposed:

> Students, young graduates or developers of unrelated fields entering the domain,
> preferring learning by doing and curated content (to safe time) over complete coverage,
> and coming with some basic computer / programming knowledge.

Besides, **contributors** should be attracted to add new quests and adventures.

---

**--- TO BE CONTINUED ---**
```
# Architecture constraints

# Context and scope
## Business context
## Technical context


# Solution strategy

# Building block view
## Whitebox overall system
## Level 2
## Level 3

# Runtime view

# Deployment view
## Infrastructure level 1
## Infrastructure level 2

# Cross-cutting concepts
```
---

# Architecture decisions

**[AD-001]** Quests are deployed using runtime package management, adventures via image updates

As long as a set of quests shares a common runtime environment as well as an overarching
learning topic, they can be installed in a shared system image using _runtime package management_.
Only iff the quest dependencies conflict or a different learning topic should be focused,
a conventional _full-image update_ is performed.

**[AD-002]** Runtime dependencies of quests are pre-installed

To reduce the complexity of managing runtime dependencies in the package management on the device,
all dependencies are pre-installed in the parent adventure image.
Installing the quest then only requires to deploy its internal state, no other packages.

**[AD-003]** Adventures ship all included quests

While downloading quests from an external source may provide more flexibility (especially on upstream
changes), it requires more infrastructure to be setup. Given memory space is not (yet) an issue,
an adventure image can contain all quest packages to be installed during runtime instead.

**[AD-004]** Using read-only rootfs by default

While it complicates the configuration of the system a bit, this feature not only resembles best practices
but also allows to remove any runtime changes relatively easily.

**[AD-005]** Each adventure resides in a dedicated Yocto layer

Depending on the learning goals to achieve within the adventure, a fundamentally different system layout,
bootloader and/or kernel configuration might be required. To allow this - even if it's supposedly not the
common case - a convention to create one layer per adventure is followed.

**[AD-006]** Quests shall only ship a single package

To reduce complexity during runtime package installation (most notably through the use of a straight-forward
package location algorithm, i.e. requiring packages to be named after their quests), only a single package
shall be built. For some cases, such as building kernel modules, this requires a non-default behavior regarding
package splitting.

---

**--- TO BE CONTINUED ---**
```
# Quality requirements
## Quality tree
## Quality scenarios

# Risks and technical debts
```

---

# Glossary

- **Adventure**:
  A set of tasks (quests) to be run through by the user in order to build up knowledge
  of a broader concept or technology area of the system.

- **Quest**:
  A single user facing task, made to allow learning one Embedded Linux specific thing
  while interacting with the system.