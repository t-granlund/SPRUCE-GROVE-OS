"""Grove-owned spinner: on-brand art, seated as the default.

The runtime spinner belongs to the third-party ``puppy_spinner`` plugin, whose
default is a bouncing dog-face emoji. Rather than fork that plugin, this one
uses the extension points it already publishes:

* ``~/.spruce_grove/spinners.json`` -- user spinners load from there and win on
  name collision, so seeding it is the supported way to add art.
* the ``spinner_style`` config key -- which spinner is active.

Seeding is **additive and non-destructive**: it writes only grove's own two
names, never touches anyone else's entries, never overwrites an entry that
already exists, and never touches ``spinner_style`` once the user has set it.
A user who picks ``puppy`` keeps ``puppy`` on every future launch.
"""
