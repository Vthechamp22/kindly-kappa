import keyword
import random
from operator import methodcaller

from typing_extensions import Self

FOUR_SPACES = "    "
TWO_SPACES = "  "


class Modifiers:
    def __init__(self, file_contents: list[str], difficulty: int = 1) -> None:
        """This class has different functions which introduce different types of bugs.

        All the functions should return Self so they can be chained to get the final
        output. The number of chained functions is determined by the difficulty but
        they are randomly sampled across the entire codebase.

        Args:
            file_contents: The raw data received from the websocket.
            difficulty: The level of difficulty selected. Defaults to 1.
        """
        self.file_contents = file_contents[:-1]  # Removes the last "\n"
        self.difficulty = difficulty

        self.modified_contents = file_contents[:-1]

    @property
    def output(self) -> list[str]:
        """Returns the modified code, if any modifications have been done.

        Returns:
            Modified lines of code, in the same format as the input data.
        """
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

        Returns:
            The modifier instance.
        """
        line_numbers = []
        for num, line in enumerate(self.file_contents):
            if line.startswith(FOUR_SPACES):
                line_numbers.append(num)

        line_subset = random.sample(line_numbers, min(self.difficulty, len(line_numbers)))
        for num in line_subset:
            self.modified_contents[num] = self.modified_contents[num].replace(FOUR_SPACES, TWO_SPACES)

        return self

    def remove_end_colon(self) -> Self:
        """A code modifier that causes a SyntaxError.

        This will remove the colon after a function definition, loop, or if statement.

        Returns:
            The modifier instance.
        """
        line_numbers = []
        for num, line in enumerate(self.file_contents):
            if line.endswith(":\n"):
                line_numbers.append(num)

        line_subset = random.sample(line_numbers, min(self.difficulty, len(line_numbers)))
        for num in line_subset:
            self.modified_contents[num] = self.modified_contents[num].replace(":", "")

        return self

    def change_keyword(self) -> Self:
        """A code modifier that causes a SyntaxError.

        This will change any of the python keywords to "kappa".

        Returns:
            The modifier instance.
        """
        python_keywords = keyword.kwlist

        number_keyword_pairs = []
        for num, line in enumerate(self.file_contents):
            if any(key in line for key in python_keywords):
                number_keyword_pairs.extend([(num, key) for key in python_keywords if key in line])

        line_subset = random.sample(number_keyword_pairs, min(self.difficulty, len(number_keyword_pairs)))
        for num, key in line_subset:
            self.modified_contents[num] = self.modified_contents[num].replace(key, "kappa")

        return self

    def comment(self) -> Self:
        """A code modifier that could raise an error.

        This will comment out a line of code.

        Returns:
            The modifier instance.
        """
        total_lines = len(self.file_contents)

        line_subset = random.sample(range(total_lines), min(self.difficulty, total_lines))
        for num in line_subset:
            self.modified_contents[num] = f"# {self.modified_contents[num]}"

        return self


if __name__ == "__main__":
    test_lines = ["def say_hello() -> str:\n", '    return "Hello!"\n', "\n"]

    modifiers = Modifiers(test_lines)

    print(modifiers.output)
