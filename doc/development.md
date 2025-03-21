# Developing quests and adventures

## Upfront considerations

Adventures are essentially Yocto images for the RaspberryPi with a predefined
set of quests included (yet not installed). The quests should optimally share
a common theme or learning topic. See the currently [planned adventures](planned-adventures.md)
for more details.

Before adding a new adventure image, please consider adding your quest(s)
to one of the existing images.

To reduce waiting times when switching between quests, _all runtime dependencies_
_of all quests contained in an adventure are already installed in the corresponding_
_image_. Therefore, only data that is directly related to the individual quest is
installed or removed during runtime. This might need some special care when implementing
the quests, though.

## Creating quests

Each quest is shipped as a dedicated Yocto recipe. You only need to inherit the
`elepi-quest.bbclass` and define the key properties of your quest in form of the
following variables:

**Mandatory**:

- `QUEST_DESCRIPTION`: A text file explaining the goal of the quest and possible
  entrypoints. This will be shown when users call `elepictl info`. By default,
  the `elepi-quest.bbclass` assumes a file named `description.txt` to be present
  under `files`.

- `QUEST_VERIFICATION_KEY`: Path to the public key used to validate the quest's
  solution code (more on that below). By default, the `elepi-quest.bbclass` assumes
  a file named `verification.key` to be present under `files`. 

**Optional**:
- `QUEST_HINTS_DIR`: A directory path containing all hint files to be deployed.
  They will be revealed in the order they appear on the filesystem to the user
  on calls to `elepictl hint`. By default, the `elepi-quest.bbclass` assumes the
  directory `hints` to be present under `files`. If you don't want to give any hints,
  you can define the variable empty.

- `QUEST_SETUP_SCRIPTS`: A list of source paths to bash scripts to be executed in
  the package post-install step, for example to perform runtime-only preparations
  for the quest.

- `QUEST_CLEANUP_SCRIPTS`: A list of source paths to bash scripts to be executed 
  when the quest is removed again, to ensure no changes made during runtime are left.

### Limitations

There are some things to consider when implementing quests:

**Avoid package splitting**

Given quests are installed during runtime using solely their name as identifier,
they should be deployed in a single package. Note that some bitbake features come
with automatic package splitting - a notable example is the `module.bbclass` for
writing out-of-tree kernel modules. Splitting of packages is deactivated in the
`elepi-quest.bbclass` for this particular case.

**Do not assume reboots**

Some features like autoloading of kernel modules assume to be activated through a system
reboot. But as the waiting time between quests should be minimized, this usually does not
happen, so you may need to activate such features manually, e.g. in the `postinst` script.

**System or kernel configuration can only be adjusted for the whole adventure**

If your quest requires certain kernel or bootloader configuration, for example, this comes
into effect for all quests in this adventure. Either avoid such side-effects by writing
runtime `postinst`/`prerm` scripts or ensure no negative impact on other quests.

### Quest solution and verification

Solving a quest is done by verifying a solution code. Technically, this is achieved
using asymmetric keys and signatures - together with a shared token (aka message).

When implementing a quest, you need to do the following:

- create a private-public key pair (RSA, 512 bits),
- generate a signature on the token (with SHA1 hashing)
- deploy the public key on the device and 
- reveal the signature as hexadecimal string to the user on quest completion.

There is a [helper script](../tools/development/generate-quest-keys.sh) for key
and signature generation and the public key is what the `QUEST_VERIFICATION_KEY`
points to. How you reveal the signature is up to you - you could, for example,
spread fragments of the hex code across the system to make it more challenging.

Here is an (abbreviated) example of the output of the helper script:

```bash
<quest-name>.key:
-----BEGIN PRIVATE KEY-----
MIIBVgIBADANBgkqhkiG9w0BAQEFAASCAUAwggE8AgEAAkEA23TwrYyxENi/y16N
...
h1phuE+Cnu2EbVV+CMksW/DyM976wYZxAiAqLbANXVVGvnj/oQxCz+hL228Zp5Ar
Nm9ZyeGn4oDRDw==
-----END PRIVATE KEY-----

<quest-name>.verification.key:
-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBANt08K2MsRDYv8tejZweGf52F58lk6d4
3p8pOaUzounI9KumdLPy4c6gPaEv9sw4hN9ZjR3+H3kvB43armyz3LMCAwEAAQ==
-----END PUBLIC KEY-----

<quest-name>-solution.hex:
5fa953556ca6a33ab679c16add2d485eb30a03f5bbcab2f239367bd5a73e
86ca21410ef03ee7d648176cbbbf48ca5c6d108bea1b9027582d3f51b377
84d91881
```

The `QUEST_VERIFICATION_KEY` variable defaults to `${WORKDIR}/verification.key`,
so usually you only need to add your key to `SRC_URI`.