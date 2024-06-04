import os
from exa_py import Exa
from langchain.agents import tool


class ExaSearchToolset:
    @tool
    def search(query: str):
        """Search for a webpage based on the query."""
        return ExaSearchToolset._exa().search(
            f"{query}", use_autoprompt=True, num_results=3
        )

    @tool
    def find_similar(url: str):
        """Search for webpages similar to a given URL.
        The url passed in should be a URL returned from `search`.
        """
        return ExaSearchToolset._exa().find_similar(url, num_results=3)

    @tool
    def get_contents(ids: str):
        """Get the contents of a webpage.
        The ids must be passed in as a list, a list of ids returned from `search`.
        """
        ids = eval(ids)

        contents = str(ExaSearchToolset._exa().get_contents(ids))
        contents = contents.split("URL:")
        contents = [content[:1000] for content in contents]
        return "\n\n".join(contents)

    def tools():
        # Return a list of tool methods from ExaSearchToolset
        # These methods can be dynamically accessed and executed
        # 1. each tool is self contained and can connect to the Exa client
        # 2. when an agent is called, by passing a list of functions,
        #    we can append the function details to the context. Thus,
        #    you only need to update the function docstring and all
        #    the agents will automatically get updated function details
        return [
            ExaSearchToolset.search,
            ExaSearchToolset.find_similar,
            ExaSearchToolset.get_contents,
        ]

    def _exa():
        # private method that creates a connection to the Exa API
        # The lazy stateless approach in this code involves creating a new instance of the `Exa` client within class methods each time it is needed. This ensures that the client is always initialized with the most current configuration, such as up-to-date API keys, enhancing flexibility and adaptability. By avoiding persistent state, the code minimizes the risk of using stale connections and simplifies resource management. This approach also facilitates easier testing, as each method call is independent and self-contained. Overall, the stateless pattern promotes scalability, reliability, and maintainability in the application.
        return Exa(api_key=os.environ.get("EXA_API_KEY"))
