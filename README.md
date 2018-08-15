README
    Last Updated: 8/15/18
    Author: Jonathan Moran

Project title: Greedy Kart
    This script takes in character/kart/wheels/glider stats from Mario Kart 8
    Deluxe for the Nintendo Switch, and uses a recursive greedy algorithm to
    determine the best Mario Kart character/kart/wheels/glider combination,
    given a user-defined ordering of attribute preferences (acceleration, speed,
    handling, etc.).

Motivation:
    Read the "Annoying Non-perfection of Mario Kart" post from my Medium --
    https://medium.com/@jflmoran

Built with:
    -Python

Functions:
    `def import_table(csvName):`
    - Import Data Table: reads in CSV table data to our internal data structures.
        * Arguments:
            * /csvName/ - String of CSV file name
        * Returns:
            * /l/ - List of Modifiers

    `def combine_modifiers(characters, karts, wheels, gliders):`
    - Combine Modifier Attributes: takes our imported data tables, and creates a
      list of every possible Modifier combination of the four different modifiers
      (character, kart, wheels, glider), with summed attributes.
        * Arguments:
            * /characters; karts; heels; gliders/ - Four different lists of
              Modifiers, representing each type of Modifier.
        * Returns:
            * /combos/ - List of all possible combinations of Modifiers with
              updated attributes.

    `def recursive_priority(tiedCombos, sortedCombos, optKeys, layersDeep):`
    - Recursive Prioritization: a greedy recursive function that sorts by each
      attribute prioritization, and recurses to the next priority when there are
      ties.
        * Arguments:
            * /tiedCombos/ - List of Modifier combinations representing all
              combinations at first, then all combinations tied at a certain
              attribute
                * /sortedCombos/ - initially an empty list, but is filled with
                  ordered lists of tied Modifier combos
                * /optKeys/ - List of lists of single or grouped/summed
                  prioritized attributes
                * /layersDeep/ - Number counter to know how deep into our
                  recursion we are
        * Recursive Base Cases:
            * /BCO/: if the tiedCombos List holds only one Modifier, and thus
              contains no more tied combos, append it to our sortedCombos list
            * /BC1/: if the recursion counter equals the length of our attribute
              optimization list,  and thus meaning we have completed all our
              optimizations, append the tiedCombos list = to our sortedCombos
              list
        * Returns:
            * /sortedCombos/  - Finished list of lists of tied Modifier combos,
              in order of the defined attribute preferences

    `def print_data(combos, priorities, csvName):`
    - Export Data Table: Prints sorted data to a CSV file.
        * Arguments:
            * /combos/ - List of lists of tied Modifier combos
            * /priorities/ - List of prioritized Attributes
            * /csvName/ - String of name of CSV output file
        * Returns: N/A

Tests:
    - included in kart.py
