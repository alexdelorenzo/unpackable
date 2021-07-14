# Unpackable: Object destructuring for Python
`unpackable` is a module that lets you use [Python's destructuring assignment](https://www.python.org/dev/peps/pep-3132/) to unpack an object's attributes.

## Use case
Consider [JavaScript's destructuring assignment](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment) feature that allows you to do the following:
```javascript
class User {
  constructor(id, email) {
    this.id = id;
    this.email = email;
  }
}

const user = new User(1, 'example@example.com')
const {id, email} = user;  // destructure
```

`unpackable` allows you to do something similar in Python:
```python
from dataclasses import dataclasses
from unpackable import Unpackable


@dataclass
class User(Unpackable):
  id: int
  email: str


user = User(1, 'example@example.com')
id, email = user  # destructure
```

`unpackable` can also unpack objects that don't subclass `Unpackable`:
```python
from dataclasses import dataclasses
from unpackable import unpack


@dataclass
class User:
  id: int
  email: str


user = User(1, 'example@example.com')
id, email = unpack(user)  # destructure
```

# Status
`unpackable` currently works with iterable objects, `dataclasses` and simple objects.

This is alpha software and is not ready for use beyond limited use cases like in [my `app_paths` project](https://github.com/alexdelorenzo/app_paths).

# Installation
## Requirements
 - Python 3.8+

## PyPI
```bash
python3 -m pip install unpackable
```

# Support
Want to support this project and [other open-source projects](https://github.com/alexdelorenzo) like it?

<a href="https://www.buymeacoffee.com/alexdelorenzo" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="60px" style="height: 60px !important;width: 217px !important;max-width:25%" ></a>

# License
See `LICENSE`. If you'd like to use this project with a different license, please get in touch.
