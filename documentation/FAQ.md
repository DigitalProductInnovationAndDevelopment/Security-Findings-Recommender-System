# Frequently Asked Questions

A compiled list of FAQs that may come in handy.

## Import ot found?

If you are getting an "import not found" error, it is likely because the base folder is always `src`. Always run the program from the `src` folder or use the commands inside the Makefile.

If you have something in `src/lib` and want to use it, import it as follows:

```python
import lib  # or
from lib import ...
```

# Why are env.docker and .env different?

If you are only running the program using Docker, then you only need to worry about `.env.docker`.

As the addresses tend to be different in a Docker environment compared to a local environment, you need different values to resolve the addresses.

For example, if you have your program outside Docker (locally) and want to access a database, you may use:

```
POSTGRES_SERVER=localhost
```

If you run your program inside Docker, then you must use:

```
POSTGRES_SERVER=db
```

# How can i add my own LLM Strategy?

There is a `BaseLLMService` that you can extend to create your own strategy. You can then use it as follows:

```python
class CustomService(BaseLLMService, LLMServiceMixin):
    #your methods

my_strategy = CustomService()  # instead of my_strategy = OLLAMAService()
llm_service = LLMServiceStrategy(my_strategy)

```

# What if my input data changes ?

We have a predefined structure that input must adhere to called `Content`. You can always adjust this to satisfy your input and convert it to a database model.

Inside the db model called `Findings`, there is a method `from_data` which can be modified to adapt the changes.
