# Frequently Asked Questions

A compiled list of frequently asked questions that may come in handy.

## Import not found?

If you are encountering an "import not found" error, it is likely because the base folder is always `src`. Make sure to run the program from the `src` folder or use the commands inside the Makefile.

If you have something in `src/lib` and want to use it, import it as shown below:

```python
import lib  # or
from lib import ...
```

# Why use POST call to retrieve recommendations and aggregated recommendations?

For these calls, we require a JSON type body with at least `{}`. This allows us to handle nested filters such as `task_id` and `severity` inside the filters. Using query parameters and GET calls would be less suitable for this purpose. However, one can modify the pathname, like changing `get-`, to make it more convenient.

# Why are env.docker and .env different?

If you are running the program exclusively using Docker, then you only need to concern yourself with `.env.docker`.

Since the addresses can differ between a Docker environment and a local environment, you need different values to resolve the addresses.

For example, if your program is outside Docker (locally) and you want to access a database, you may use:

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
`VulnerablityReport` also has `create_from_flama_json` that must be adjusted accordingly to make sure the Generation side also works.

# Does it make sense to Mock LLM?

While we don't strive for accuracy, it would still make sense to mock LLM methods to ensure that methods for finding and interacting properly with LLM class methods work correctly. Nevertheless, it is still difficult to extract meaningful test outputs based on only prompts as input.
