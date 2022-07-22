import random
from operator import methodcaller

from typing_extensions import Self

FOUR_SPACES = "    "
TWO_SPACES = "  "


class Modifiers:
    """This class has different functions which introduce different types of bugs.

    All the functions should return Self so they can be chained to get the final
    output. The number of chained functions is determined by the difficulty.
    """

    def __init__(self, file_contents: list[str], difficulty: int = 1) -> None:
        self.file_contents = file_contents
        self.difficulty = difficulty

        self.modified_contents = file_contents

    @property
    def output(self) -> list[str]:
        """Returns the modified code, if any modifications have been done."""
        method_names = [
            func for func in dir(Modifiers) if callable(getattr(Modifiers, func)) and not func.startswith("__")
        ]
        methods = map(methodcaller, random.sample(method_names, self.difficulty))

        for method in list(methods):
            method(self)

        return self.modified_contents

    def remove_indentation(self) -> Self:
        """A code modifier that causes an IndentationError.

        This will reduce indentation from four spaces to two spaces.
        """
        line_numbers = []
        for num, line in enumerate(self.file_contents):
            if line.startswith(FOUR_SPACES):
                line_numbers.append(num)

        line_subset = random.sample(line_numbers, self.difficulty)
        for num in line_subset:
            self.modified_contents[num] = self.file_contents[num].replace(FOUR_SPACES, TWO_SPACES)

        return self

    def remove_end_colon(self) -> Self:
        """A code modifier that causes a SyntaxError.

        This will remove the colon after a function definition, loop, or if statement.
        """
        line_numbers = []
        for num, line in enumerate(self.file_contents):
            if line.endswith(":\n"):
                line_numbers.append(num)

        line_subset = random.sample(line_numbers, self.difficulty)
        for num in line_subset:
            self.modified_contents[num] = self.file_contents[num].replace(":", "")

        return self


if __name__ == "__main__":
    test_lines = ["def say_hello() -> str:\n", '    return "Hello!"\n', "\n"]

    modifiers = Modifiers(test_lines)

    print(modifiers.output)
